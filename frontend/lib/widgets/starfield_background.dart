import 'dart:math';
import 'package:flutter/material.dart';

class StarfieldBackground extends StatefulWidget {
  const StarfieldBackground({super.key});

  @override
  State<StarfieldBackground> createState() => _StarfieldBackgroundState();
}

class _StarfieldBackgroundState extends State<StarfieldBackground>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<StarData> stars = [];

  @override
  void initState() {
    super.initState();

    // Controle da animação (20 segundos para um ciclo completo)
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 20),
    )..repeat();

    generateStars();
  }

  void generateStars() {
    final random = Random();
    // DICA: Se o celular ASUS continuar lento, mude 80 para 40 aqui.
    for (int i = 0; i < 80; i++) {
      stars.add(
        StarData(
          x: random.nextDouble(),
          y: random.nextDouble(),
          size: random.nextDouble() * 3 + 1,
          speed: random.nextDouble() * 0.002 + 0.0005,
          opacity: random.nextDouble() * 0.6 + 0.1,
        ),
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return CustomPaint(
          painter: StarfieldPainter(
            stars: stars,
            animationValue: _controller.value,
          ),
          size: Size.infinite,
        );
      },
    );
  }
}

class StarData {
  double x;
  double y;
  double size;
  double speed;
  double opacity;

  StarData({
    required this.x,
    required this.y,
    required this.size,
    required this.speed,
    required this.opacity,
  });
}

class StarfieldPainter extends CustomPainter {
  final List<StarData> stars;
  final double animationValue;

  StarfieldPainter({
    required this.stars,
    required this.animationValue,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint();

    for (final star in stars) {
      // Cálculo da posição vertical (Loop infinito de 0.0 a 1.0)
      double animatedY = (star.y + animationValue * star.speed * 100) % 1.0;

      final position = Offset(
        star.x * size.width,
        animatedY * size.height,
      );

      // Cores: Estrelas maiores tendem ao azul, menores ao branco
      final starColor = star.size > 3
          ? Colors.blue.withOpacity(star.opacity)
          : Colors.white.withOpacity(star.opacity);

      paint.color = starColor;

      // Efeito de Glow (Brilho) para estrelas de destaque
      if (star.size > 2.5) {
        paint.maskFilter = const MaskFilter.blur(BlurStyle.normal, 2);
        canvas.drawCircle(position, star.size * 1.5, paint);
        paint.maskFilter = null; 
      }

      canvas.drawCircle(position, star.size, paint);
    }
  }

  @override
  bool shouldRepaint(covariant StarfieldPainter oldDelegate) {
    // Só repinta se o frame da animação mudar
    return oldDelegate.animationValue != animationValue;
  }
}