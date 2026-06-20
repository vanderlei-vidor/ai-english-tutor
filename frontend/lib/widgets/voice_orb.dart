import 'dart:math';
import 'package:flutter/material.dart';

// 🛑 Substituindo Strings por um Enum seguro e performático
enum VoiceOrbState { idle, listening, thinking, speaking }

// 🌌 Modelo fortemente tipado para as partículas
class OrbParticle {
  final double size;
  final double offset;
  final double angle;
  final double opacity;

  OrbParticle({
    required this.size,
    required this.offset,
    required this.angle,
    required this.opacity,
  });
}

class VoiceOrb extends StatefulWidget {
  final VoiceOrbState state;
  final double soundLevel;

  const VoiceOrb({super.key, required this.state, required this.soundLevel});

  @override
  State<VoiceOrb> createState() => _VoiceOrbState();
}

class _VoiceOrbState extends State<VoiceOrb> with TickerProviderStateMixin {
  late AnimationController _controller;
  late AnimationController _waveController;
  late List<OrbParticle> particles;
  final Random _random = Random();

  @override
  void initState() {
    super.initState();

    // 🛠️ PONTO 1: Reduzido o offset de voo das partículas para orbitarem mais perto
    particles = List.generate(12, (index) {
      return OrbParticle(
        size: 1.5 + _random.nextDouble() * 3.5,
        offset: 55 + _random.nextDouble() * 65, // Antes era 80 + 100
        angle: _random.nextDouble() * pi * 2,
        opacity: 0.2 + _random.nextDouble() * 0.5,
      );
    });

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _waveController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    _waveController.dispose();
    super.dispose();
  }

  double _getScale(VoiceOrbState state) {
    switch (state) {
      case VoiceOrbState.listening:
        return 1.25;
      case VoiceOrbState.thinking:
        return 1.1;
      case VoiceOrbState.speaking:
        return 1.35;
      case VoiceOrbState.idle:
      default:
        return 1.0;
    }
  }

  Color _getColor(VoiceOrbState state) {
    switch (state) {
      case VoiceOrbState.listening:
        return Colors.lightBlueAccent;
      case VoiceOrbState.thinking:
        return Colors.cyanAccent;
      case VoiceOrbState.speaking:
        return Colors.deepPurpleAccent;
      case VoiceOrbState.idle:
      default:
        return const Color(0xFF334155);
    }
  }

  @override
  Widget build(BuildContext context) {
    final currentColors = _getColor(widget.state);
    final baseScale = _getScale(widget.state);

    return AnimatedBuilder(
      animation: Listenable.merge([_controller, _waveController]),
      builder: (context, child) {
        final audioBoost = (widget.soundLevel / 50).clamp(0.0, 0.5);
        final pulse = 1 + (_controller.value * 0.08) + audioBoost;

        return Transform.scale(
          scale: baseScale * pulse,
          child: Transform.rotate(
            angle: _controller.value * 0.15,
            child: Stack(
              alignment: Alignment.center,
              children: [
                
                // 🌌 1. FLOATING PARTICLES
                ...List.generate(12, (index) {
                  final particle = particles[index];
                  final dx = cos(particle.angle) * particle.offset;
                  final dy = sin(particle.angle) * particle.offset;
                  final movement = sin((_controller.value * pi) + index);

                  return Transform.translate(
                    offset: Offset(dx + movement * 2, dy + movement * 2),
                    child: Opacity(
                      opacity: particle.opacity,
                      child: Container(
                        width: particle.size,
                        height: particle.size,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: currentColors,
                          boxShadow: [
                            BoxShadow(color: currentColors, blurRadius: 8),
                          ],
                        ),
                      ),
                    ),
                  );
                }),

                // 🌌 2. ENERGY WAVES
                () {
                  final extraWave = widget.state == VoiceOrbState.speaking ? 0.5 : 0.0;
                  final waveScale = 1 + (_waveController.value * 1.4) + extraWave;
                  final waveOpacity = (1 - _waveController.value) * 0.4;

                  return Transform.scale(
                    scale: waveScale,
                    child: Container(
                      // 🛠️ PONTO 2: Reduzido de 140 para 100
                      width: 100,
                      height: 100,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(
                          color: currentColors.withOpacity(waveOpacity),
                          width: 2.5,
                        ),
                      ),
                    ),
                  );
                }(),

                // 🌌 3. MAIN ORB
                Container(
                  // 🛠️ PONTO 3: Reduzido de 140 para 100
                  width: 100,
                  height: 100,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: RadialGradient(
                      colors: [
                        currentColors.withOpacity(0.95),
                        currentColors.withOpacity(0.5),
                        Colors.black,
                      ],
                      stops: const [0.2, 0.6, 1],
                    ),
                    boxShadow: [
                      // Suavizado o tamanho dos brilhos para casar com o tamanho novo
                      BoxShadow(
                        color: currentColors.withOpacity(0.65),
                        blurRadius: 35,   // Antes 50
                        spreadRadius: 10, // Antes 15
                      ),
                      BoxShadow(
                        color: Colors.white.withOpacity(0.12),
                        blurRadius: 18,   // Antes 25
                        spreadRadius: -6,  // Antes -8
                      ),
                    ],
                  ),
                  child: Center(
                    child: Container(
                      // 🛠️ MIOLO INTERNO: Reduzido de 40 para 28 para ficar proporcional
                      width: 28,
                      height: 28,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: Colors.white.withOpacity(0.25),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.white.withOpacity(0.4),
                            blurRadius: 15,
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}