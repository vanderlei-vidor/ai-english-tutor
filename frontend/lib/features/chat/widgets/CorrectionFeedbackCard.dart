import 'dart:ui';
import 'package:flutter/material.dart';

class CorrectionFeedbackCard extends StatelessWidget {
  final String correction;
  final String explanation;
  final String example;

  const CorrectionFeedbackCard({
    super.key,
    required this.correction,
    required this.explanation,
    required this.example,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(24),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
        child: Container(
          margin: const EdgeInsets.only(top: 10),
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(24),
            gradient: LinearGradient(
              colors: [
                Colors.redAccent.withOpacity(0.12),
                Colors.deepPurpleAccent.withOpacity(0.05),
              ],
            ),
            border: Border.all(color: Colors.redAccent.withOpacity(0.3), width: 1.2),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.25),
                blurRadius: 25,
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "❌ AI Feedback",
                style: TextStyle(
                  color: Colors.redAccent,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  shadows: [Shadow(color: Colors.redAccent, blurRadius: 10)],
                ),
              ),
              const SizedBox(height: 14),
              Text(
                "✅ Correction:\n$correction",
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500),
              ),
              if (explanation.isNotEmpty) ...[
                const SizedBox(height: 10),
                Text("📘 Explanation:\n$explanation", style: const TextStyle(color: Colors.white70)),
              ],
              if (example.isNotEmpty) ...[
                const SizedBox(height: 10),
                Text("💡 Example:\n$example", style: const TextStyle(color: Colors.white70)),
              ],
            ],
          ),
        ),
      ),
    );
  }
}