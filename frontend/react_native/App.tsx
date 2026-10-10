import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ScrollView,
  TextInput,
  ActivityIndicator,
  SafeAreaView,
  Alert,
} from 'react-native';

const API_BASE_URL = 'http://10.0.2.2:8000'; // Or 'http://localhost:8000'

interface Token {
  text: string;
  confidence: number;
}

export default function App() {
  const [screen, setScreen] = useState<'camera' | 'review' | 'report'>('camera');
  const [tokens, setTokens] = useState<Token[]>([
    { text: 'Warfrin 5mg', confidence: 0.72 }, // <80% flag
    { text: 'Aspirin 81mg', confidence: 0.94 },
  ]);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [checkedChecklist, setCheckedChecklist] = useState<{ [key: number]: boolean }>({});

  const handleCapture = (presetTokens?: Token[]) => {
    if (presetTokens) {
      setTokens(presetTokens);
    }
    setScreen('review');
  };

  const handleEditToken = (index: number) => {
    const current = tokens[index];
    Alert.prompt ? (
      Alert.prompt('Edit Medication Token', 'Correct OCR transcription', [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Save',
          onPress: (text?: string) => {
            if (text) {
              const updated = [...tokens];
              updated[index] = { text: text.trim(), confidence: 1.0 };
              setTokens(updated);
            }
          },
        },
      ], 'plain-text', current.text)
    ) : null;
  };

  const handleRemoveToken = (index: number) => {
    setTokens(tokens.filter((_, i) => i !== index));
  };

  const handleSearchRxNorm = async (q: string) => {
    setSearchQuery(q);
    if (!q.trim()) {
      setSearchResults([]);
      return;
    }
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/drugs/lookup?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      setSearchResults(data.results || []);
    } catch (e) {
      console.log('Search error', e);
    }
  };

  const handleAddMed = (med: any) => {
    setTokens([...tokens, { text: med.generic_name, confidence: 1.0 }]);
    setSearchQuery('');
    setSearchResults([]);
  };

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/prescriptions/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tokens: tokens.map((t) => ({ text: t.text, confidence: t.confidence })),
          confidence_cutoff: 0.8,
        }),
      });
      const data = await res.json();
      setReport(data);
      setScreen('report');
    } catch (e) {
      Alert.alert('Error', 'Failed to communicate with backend service.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* 1. Camera View Screen */}
      {screen === 'camera' && (
        <View style={styles.content}>
          <Text style={styles.headerTitle}>Prescription Scanner</Text>
          <View style={styles.cameraBox}>
            <View style={styles.cropGuide}>
              <Text style={styles.cropText}>Align Prescription within Crop Frame</Text>
              <View style={styles.sampleSnippet}>
                <Text style={styles.sampleText}>Rx: Warfrin 5mg (72% OCR)</Text>
              </View>
              <View style={styles.sampleSnippet}>
                <Text style={styles.sampleText}>Rx: Aspirin 81mg (94% OCR)</Text>
              </View>
            </View>
          </View>

          <Text style={styles.sectionHeader}>Instant Test Presets:</Text>
          <TouchableOpacity
            style={styles.presetButton}
            onPress={() =>
              handleCapture([
                { text: 'Warfrin 5mg', confidence: 0.72 },
                { text: 'Aspirin 81mg', confidence: 0.94 },
              ])
            }
          >
            <Text style={styles.presetTitle}>Severe Bleed Risk (Warfarin + Aspirin)</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.presetButton}
            onPress={() =>
              handleCapture([
                { text: 'Sildenafil 50mg', confidence: 0.95 },
                { text: 'Nitroglycerin 0.4mg', confidence: 0.9 },
              ])
            }
          >
            <Text style={styles.presetTitle}>Severe Vasodilator Risk (Sildenafil + Nitrates)</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.actionButton} onPress={() => handleCapture()}>
            <Text style={styles.actionButtonText}>Capture & Review Tokens</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* 2. OCR Token Review Chips Screen */}
      {screen === 'review' && (
        <ScrollView style={styles.content}>
          <Text style={styles.headerTitle}>Review OCR Tokens</Text>
          <Text style={styles.subtitle}>
            Google ML Kit confidence under 80% flagged in amber. Tap to edit.
          </Text>

          <View style={styles.chipsContainer}>
            {tokens.map((t, idx) => {
              const isUncertain = t.confidence < 0.8;
              return (
                <TouchableOpacity
                  key={idx}
                  style={[styles.chip, isUncertain && styles.uncertainChip]}
                  onPress={() => handleEditToken(idx)}
                >
                  <Text style={[styles.chipText, isUncertain && styles.uncertainChipText]}>
                    {t.text} ({(t.confidence * 100).toFixed(0)}%)
                  </Text>
                  <TouchableOpacity onPress={() => handleRemoveToken(idx)}>
                    <Text style={styles.chipRemove}>✕</Text>
                  </TouchableOpacity>
                </TouchableOpacity>
              );
            })}
          </View>

          <Text style={styles.sectionHeader}>Add / Search RxNorm:</Text>
          <TextInput
            style={styles.input}
            placeholder="Search medicine (e.g., Coumadin, Advil)..."
            placeholderTextColor="#64748B"
            value={searchQuery}
            onChangeText={handleSearchRxNorm}
          />

          {searchResults.map((m, idx) => (
            <TouchableOpacity key={idx} style={styles.searchResultItem} onPress={() => handleAddMed(m)}>
              <Text style={styles.searchResultTitle}>{m.generic_name.toUpperCase()}</Text>
              <Text style={styles.searchResultSub}>{m.drug_class}</Text>
            </TouchableOpacity>
          ))}

          <TouchableOpacity
            style={[styles.actionButton, { marginTop: 24 }]}
            onPress={handleAnalyze}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.actionButtonText}>Verify DDIs & Consult Gemma 4</Text>
            )}
          </TouchableOpacity>
        </ScrollView>
      )}

      {/* 3. Final Interaction Report Screen */}
      {screen === 'report' && report && (
        <ScrollView style={styles.content}>
          <View
            style={[
              styles.riskBanner,
              report.risk_color === 'red'
                ? styles.bannerRed
                : report.risk_color === 'amber'
                ? styles.bannerAmber
                : styles.bannerGreen,
            ]}
          >
            <Text style={styles.riskTitle}>RISK LEVEL: {report.risk_level.toUpperCase()}</Text>
            <Text style={styles.riskSub}>
              {report.verified_ddis.length} interaction pairs deterministically verified.
            </Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.cardTitle}>Gemma 4 Plain-Language Summary</Text>
            <Text style={styles.cardBody}>{report.patient_summary}</Text>
          </View>

          <Text style={styles.sectionHeader}>Verified Drug Interactions</Text>
          {report.interaction_flags?.map((f: any, idx: number) => (
            <View key={idx} style={styles.card}>
              <Text style={styles.interactionPair}>{f.pair}</Text>
              <Text style={styles.severityTag}>{f.severity.toUpperCase()}</Text>
              <Text style={styles.cardBody}>{f.explanation}</Text>
              <View style={styles.actionBox}>
                <Text style={styles.actionText}>{f.action_for_pharmacist}</Text>
              </View>
            </View>
          ))}

          <Text style={styles.sectionHeader}>Ask Your Pharmacist Checklist</Text>
          {report.pharmacist_checklist?.map((item: string, idx: number) => (
            <TouchableOpacity
              key={idx}
              style={styles.checkItem}
              onPress={() =>
                setCheckedChecklist((prev) => ({ ...prev, [idx]: !prev[idx] }))
              }
            >
              <Text style={[styles.checkText, checkedChecklist[idx] && styles.checkedText]}>
                {checkedChecklist[idx] ? '☑' : '☐'} {item}
              </Text>
            </TouchableOpacity>
          ))}

          <Text style={styles.disclaimer}>{report.disclaimer}</Text>

          <TouchableOpacity style={styles.actionButton} onPress={() => setScreen('camera')}>
            <Text style={styles.actionButtonText}>Scan Another Prescription</Text>
          </TouchableOpacity>
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  content: { padding: 16 },
  headerTitle: { fontSize: 22, fontWeight: 'bold', color: '#fff', marginBottom: 8 },
  subtitle: { fontSize: 13, color: '#94A3B8', marginBottom: 16 },
  sectionHeader: { fontSize: 15, fontWeight: 'bold', color: '#CBD5E1', marginTop: 16, marginBottom: 8 },
  cameraBox: { height: 260, backgroundColor: '#1E293B', borderRadius: 16, justifyContent: 'center', alignItems: 'center', marginBottom: 16 },
  cropGuide: { width: '85%', height: '80%', borderWidth: 2, borderColor: '#38BDF8', borderRadius: 12, padding: 12 },
  cropText: { color: '#94A3B8', fontSize: 12, textAlign: 'center', marginBottom: 12 },
  sampleSnippet: { backgroundColor: '#0F172A', padding: 8, borderRadius: 6, marginBottom: 6 },
  sampleText: { color: '#F1F5F9', fontSize: 12 },
  presetButton: { backgroundColor: '#1E293B', padding: 12, borderRadius: 10, marginBottom: 8 },
  presetTitle: { color: '#38BDF8', fontWeight: 'bold', fontSize: 13 },
  actionButton: { backgroundColor: '#0284C7', padding: 15, borderRadius: 12, alignItems: 'center', marginVertical: 12 },
  actionButtonText: { color: '#fff', fontWeight: 'bold', fontSize: 15 },
  chipsContainer: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 16 },
  chip: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#1E293B', paddingVertical: 8, paddingHorizontal: 12, borderRadius: 10, borderWidth: 1, borderColor: '#334155' },
  uncertainChip: { borderColor: '#F59E0B', backgroundColor: 'rgba(245, 158, 11, 0.15)' },
  chipText: { color: '#fff', fontSize: 13, marginRight: 6 },
  uncertainChipText: { color: '#FDE68A', fontWeight: 'bold' },
  chipRemove: { color: '#94A3B8', fontSize: 14, fontWeight: 'bold' },
  input: { backgroundColor: '#1E293B', color: '#fff', padding: 12, borderRadius: 10, borderWidth: 1, borderColor: '#334155', marginBottom: 8 },
  searchResultItem: { backgroundColor: '#1E293B', padding: 10, borderRadius: 8, marginBottom: 4 },
  searchResultTitle: { color: '#fff', fontWeight: 'bold', fontSize: 13 },
  searchResultSub: { color: '#94A3B8', fontSize: 11 },
  riskBanner: { padding: 16, borderRadius: 12, marginBottom: 16, borderWidth: 1.5 },
  bannerRed: { backgroundColor: 'rgba(239, 68, 68, 0.15)', borderColor: '#EF4444' },
  bannerAmber: { backgroundColor: 'rgba(245, 158, 11, 0.15)', borderColor: '#F59E0B' },
  bannerGreen: { backgroundColor: 'rgba(16, 185, 129, 0.15)', borderColor: '#10B981' },
  riskTitle: { fontSize: 16, fontWeight: '900', color: '#fff' },
  riskSub: { color: '#E2E8F0', fontSize: 12, marginTop: 4 },
  card: { backgroundColor: '#1E293B', padding: 14, borderRadius: 12, marginBottom: 12, borderWidth: 1, borderColor: '#334155' },
  cardTitle: { color: '#38BDF8', fontWeight: 'bold', fontSize: 13, marginBottom: 6 },
  cardBody: { color: '#CBD5E1', fontSize: 13, lineHeight: 18 },
  interactionPair: { color: '#fff', fontWeight: 'bold', fontSize: 14 },
  severityTag: { color: '#EF4444', fontWeight: 'bold', fontSize: 11, marginVertical: 4 },
  actionBox: { backgroundColor: '#0F172A', padding: 8, borderRadius: 6, marginTop: 8 },
  actionText: { color: '#38BDF8', fontSize: 12 },
  checkItem: { backgroundColor: '#1E293B', padding: 12, borderRadius: 8, marginBottom: 6 },
  checkText: { color: '#E2E8F0', fontSize: 13 },
  checkedText: { textDecorationLine: 'line-through', color: '#64748B' },
  disclaimer: { color: '#64748B', fontSize: 11, fontStyle: 'italic', marginVertical: 12, textAlign: 'center' },
});
