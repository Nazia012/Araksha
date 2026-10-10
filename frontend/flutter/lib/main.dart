import 'package:flutter/material.dart';
import 'screens/camera_capture_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const PrescriptionInspectorApp());
}

class PrescriptionInspectorApp extends StatelessWidget {
  const PrescriptionInspectorApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Prescription & DDI Inspector',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        primaryColor: const Color(0xFF0284C7),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF0284C7),
          secondary: Color(0xFF38BDF8),
          surface: Color(0xFF1E293B),
          background: Color(0xFF0F172A),
        ),
        fontFamily: 'Inter',
      ),
      home: const CameraCaptureScreen(),
    );
  }
}
