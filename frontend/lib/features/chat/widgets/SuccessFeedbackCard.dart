import 'dart:ui';
import 'package:flutter/material.dart';

class SuccessFeedbackCard extends StatelessWidget {
  const SuccessFeedbackCard({super.key});

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
                Colors.greenAccent.withOpacity(0.15),
                Colors.white.withOpacity(0.02),
              ],
            ),
            border: Border.all(color: Colors.greenAccent.withOpacity(0.4), width: 1.2),
            boxShadow: [
              BoxShadow(
                color: Colors.greenAccent.withOpacity(0.1),
                blurRadius: 20,
              ),
            ],
          ),
          child: const Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                "✅ Excellent!",
                style: TextStyle(
                  color: Colors.greenAccent,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  shadows: [Shadow(color: Colors.greenAccent, blurRadius: 8)],
                ),
              ),
              SizedBox(height: 8),
              Text(
                "Your sentence is correct. Keep going! 🚀",
                style: TextStyle(color: Colors.white70, fontSize: 14),
              ),
            ],
          ),
        ),
      ),
    );
  }
}