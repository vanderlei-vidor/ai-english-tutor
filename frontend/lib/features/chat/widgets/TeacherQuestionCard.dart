import 'dart:ui';
import 'package:flutter/material.dart';

class TeacherQuestionCard extends StatelessWidget {
  final String question;

  const TeacherQuestionCard({
    super.key,
    required this.question,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(24),
      child: BackdropFilter(
        filter: ImageFilter.blur(
          sigmaX: 15,
          sigmaY: 15,
        ),
        child: Container(
          margin: const EdgeInsets.only(top: 10),
          padding: const EdgeInsets.all(18),

          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(24),

            gradient: LinearGradient(
              colors: [
                Colors.blueAccent.withOpacity(0.14),
                Colors.cyanAccent.withOpacity(0.05),
              ],
            ),

            border: Border.all(
              color: Colors.blueAccent.withOpacity(0.35),
              width: 1.2,
            ),

            boxShadow: [
              BoxShadow(
                color: Colors.blueAccent.withOpacity(0.12),
                blurRadius: 20,
              ),
            ],
          ),

          child: Column(
            crossAxisAlignment:
                CrossAxisAlignment.start,

            children: [
              const Text(
                "🤔 Teacher Question",
                style: TextStyle(
                  color: Colors.lightBlueAccent,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 10),

              Text(
                question,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 15,
                  height: 1.3,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}