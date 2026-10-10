"""
Database Module for Prescription & Drug Interaction Inspector
Supports SQLite (default zero-config) and PostgreSQL (via DATABASE_URL in docker-compose).
"""

import os
import sqlite3
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("prescription_inspector.db")

DATABASE_PATH = os.environ.get(
    "SQLITE_DB_PATH",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ddi_store.db")
)
DATABASE_URL = os.environ.get("DATABASE_URL", "")


def get_db_connection():
    """
    Returns a database connection.
    If DATABASE_URL begins with postgresql:// or postgres://, psycopg2/asyncpg can be used,
    otherwise defaults to local SQLite.
    """
    if DATABASE_URL.startswith("postgres"):
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
            return conn
        except ImportError:
            logger.warning("psycopg2 not installed; falling back to SQLite database.")

    # Ensure parent dir exists for SQLite
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(seed_if_empty: bool = True):
    """
    Initializes database tables and seeds top 100 DDIs and RxNorm entries.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    is_postgres = DATABASE_URL.startswith("postgres")

    # Table: drug_interactions
    create_interactions_sql = """
    CREATE TABLE IF NOT EXISTS drug_interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug_a TEXT NOT NULL,
        drug_b TEXT NOT NULL,
        severity TEXT NOT NULL,
        mechanism TEXT NOT NULL,
        recommendation TEXT NOT NULL,
        evidence_level TEXT DEFAULT 'Clinical Study'
    );
    """
    if is_postgres:
        create_interactions_sql = """
        CREATE TABLE IF NOT EXISTS drug_interactions (
            id SERIAL PRIMARY KEY,
            drug_a VARCHAR(100) NOT NULL,
            drug_b VARCHAR(100) NOT NULL,
            severity VARCHAR(20) NOT NULL,
            mechanism TEXT NOT NULL,
            recommendation TEXT NOT NULL,
            evidence_level VARCHAR(100) DEFAULT 'Clinical Study'
        );
        """

    cursor.execute(create_interactions_sql)

    # Table: rxnorm_medications
    create_medications_sql = """
    CREATE TABLE IF NOT EXISTS rxnorm_medications (
        rxcui TEXT PRIMARY KEY,
        generic_name TEXT NOT NULL,
        brand_names TEXT NOT NULL,
        drug_class TEXT NOT NULL,
        common_dosages TEXT,
        description TEXT
    );
    """
    if is_postgres:
        create_medications_sql = """
        CREATE TABLE IF NOT EXISTS rxnorm_medications (
            rxcui VARCHAR(50) PRIMARY KEY,
            generic_name VARCHAR(150) NOT NULL,
            brand_names TEXT NOT NULL,
            drug_class VARCHAR(150) NOT NULL,
            common_dosages TEXT,
            description TEXT
        );
        """

    cursor.execute(create_medications_sql)
    conn.commit()

    if seed_if_empty:
        # Check interaction count
        cursor.execute("SELECT COUNT(*) FROM drug_interactions;")
        count = cursor.fetchone()[0] if not is_postgres else cursor.fetchone()["count"]

        if count == 0:
            from app.data.interactions_seed import INTERACTIONS_SEED
            from app.data.rxnorm_catalog import RXNORM_CATALOG

            logger.info("Seeding top 100 Drug Interactions into database...")
            for item in INTERACTIONS_SEED:
                cursor.execute(
                    """
                    INSERT INTO drug_interactions (drug_a, drug_b, severity, mechanism, recommendation, evidence_level)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """ if not is_postgres else """
                    INSERT INTO drug_interactions (drug_a, drug_b, severity, mechanism, recommendation, evidence_level)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        item["drug_a"].lower().strip(),
                        item["drug_b"].lower().strip(),
                        item["severity"],
                        item["mechanism"],
                        item["recommendation"],
                        item.get("evidence_level", "Clinical Reference"),
                    )
                )

            logger.info("Seeding RxNorm Catalog into database...")
            for name, med in RXNORM_CATALOG.items():
                brands_str = ",".join(med.brand_names)
                dosages_str = ",".join(med.common_dosages)
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO rxnorm_medications (rxcui, generic_name, brand_names, drug_class, common_dosages, description)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """ if not is_postgres else """
                    INSERT INTO rxnorm_medications (rxcui, generic_name, brand_names, drug_class, common_dosages, description)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (rxcui) DO NOTHING;
                    """,
                    (
                        med.rxcui,
                        med.generic_name.lower().strip(),
                        brands_str,
                        med.drug_class,
                        dosages_str,
                        med.description,
                    )
                )

            conn.commit()
            logger.info("Database seeding successfully completed.")

    cursor.close()
    conn.close()


def query_drug_interactions(drugs: List[str]) -> List[Dict[str, Any]]:
    """
    Deterministic DDI Engine Query.
    Executes the exact SQL:
    SELECT drug_a, drug_b, severity, mechanism, recommendation 
    FROM drug_interactions 
    WHERE (drug_a IN (:drugs) AND drug_b IN (:drugs)) 
       OR (drug_b IN (:drugs) AND drug_a IN (:drugs));
    """
    if not drugs or len(drugs) < 2:
        return []

    # Clean and lowercase input medication names
    cleaned_drugs = list({d.lower().strip() for d in drugs if d and d.strip()})
    if len(cleaned_drugs) < 2:
        return []

    conn = get_db_connection()
    cursor = conn.cursor()
    is_postgres = DATABASE_URL.startswith("postgres")

    # Build placeholders
    placeholder = "%s" if is_postgres else "?"
    placeholders = ",".join([placeholder] * len(cleaned_drugs))

    # Deterministic query
    sql = f"""
    SELECT drug_a, drug_b, severity, mechanism, recommendation, evidence_level 
    FROM drug_interactions 
    WHERE ((drug_a IN ({placeholders}) AND drug_b IN ({placeholders})) 
       OR (drug_b IN ({placeholders}) AND drug_a IN ({placeholders})))
       AND drug_a != drug_b;
    """

    # Parameters: passed 4 times for the 4 IN clauses
    params = cleaned_drugs * 4

    cursor.execute(sql, params)
    rows = cursor.fetchall()

    results: List[Dict[str, Any]] = []
    seen_pairs = set()

    for row in rows:
        if is_postgres:
            drug_a = row["drug_a"]
            drug_b = row["drug_b"]
            severity = row["severity"]
            mechanism = row["mechanism"]
            recommendation = row["recommendation"]
            evidence = row.get("evidence_level", "Clinical Reference")
        else:
            drug_a = row["drug_a"]
            drug_b = row["drug_b"]
            severity = row["severity"]
            mechanism = row["mechanism"]
            recommendation = row["recommendation"]
            evidence = row["evidence_level"] if "evidence_level" in row.keys() else "Clinical Reference"

        # Deduplicate symmetric pairs like (A, B) and (B, A)
        pair_key = tuple(sorted([drug_a, drug_b]))
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)

        results.append({
            "drug_a": drug_a,
            "drug_b": drug_b,
            "pair": f"{drug_a.capitalize()} + {drug_b.capitalize()}",
            "severity": severity,
            "mechanism": mechanism,
            "recommendation": recommendation,
            "evidence_level": evidence
        })

    cursor.close()
    conn.close()
    return results


def search_rxnorm_medications(query: str, limit: int = 15) -> List[Dict[str, Any]]:
    """
    Searches the RxNorm database for autocomplete matching generic or brand names.
    """
    if not query or len(query.strip()) < 1:
        return []

    q = f"%{query.lower().strip()}%"
    conn = get_db_connection()
    cursor = conn.cursor()
    is_postgres = DATABASE_URL.startswith("postgres")

    sql = """
    SELECT rxcui, generic_name, brand_names, drug_class, common_dosages, description
    FROM rxnorm_medications
    WHERE generic_name LIKE ? OR brand_names LIKE ?
    LIMIT ?;
    """ if not is_postgres else """
    SELECT rxcui, generic_name, brand_names, drug_class, common_dosages, description
    FROM rxnorm_medications
    WHERE generic_name ILIKE %s OR brand_names ILIKE %s
    LIMIT %s;
    """

    cursor.execute(sql, (q, q, limit))
    rows = cursor.fetchall()

    results = []
    for r in rows:
        if is_postgres:
            results.append({
                "rxcui": r["rxcui"],
                "generic_name": r["generic_name"],
                "brand_names": [b.strip() for b in r["brand_names"].split(",") if b.strip()],
                "drug_class": r["drug_class"],
                "common_dosages": [d.strip() for d in r["common_dosages"].split(",") if d.strip()],
                "description": r["description"]
            })
        else:
            results.append({
                "rxcui": r["rxcui"],
                "generic_name": r["generic_name"],
                "brand_names": [b.strip() for b in r["brand_names"].split(",") if b.strip()],
                "drug_class": r["drug_class"],
                "common_dosages": [d.strip() for d in r["common_dosages"].split(",") if d.strip()],
                "description": r["description"]
            })

    cursor.close()
    conn.close()
    return results
