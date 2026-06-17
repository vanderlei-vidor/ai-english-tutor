import 'dart:ui';
import 'package:flutter/material.dart';

class ExerciseCard extends StatelessWidget {
  final String exercise;

  const ExerciseCard({super.key, required this.exercise});

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
                Colors.cyanAccent.withOpacity(0.12),
                Colors.blueAccent.withOpacity(0.05),
              ],
            ),
            border: Border.all(color: Colors.cyanAccent.withOpacity(0.4), width: 1.2),
            boxShadow: [
              BoxShadow(
                color: Colors.cyanAccent.withOpacity(0.08),
                blurRadius: 15,
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "🎯 Practice Challenge",
                style: TextStyle(
                  color: Colors.amber,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  shadows: [Shadow(color: Colors.amber, blurRadius: 8)],
                ),
              ),
              const SizedBox(height: 10),
              Text(
                exercise,
                style: const TextStyle(color: Colors.white, fontSize: 15, height: 1.3),
              ),
            ],
          ),
        ),
      ),
    );
  }
}