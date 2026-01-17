/*
 * ======================================================                    *
 *  Project      : widgets                                                   *
 *  File         : animated_background.dart                                  *
 *  Team         : Equipo Jña'a Ri Y'ë'ë                                     *
 *  Developer    : Axel Eduardo Urbina Secundino                             *
 *  Created      : 2025-10-30                                                *
 *  Last Updated : 2026-01-16 22:01                                          *
 * ======================================================                    *
 *                                                                           *
 *  License:                                                                 *
 * © 2026 Equipo Jña'a Ri Y'ë'ë                                              *
 *                                                                           *
 * Este software y su código fuente son propiedad exclusiva                  *
 * del equipo Jña'a Ri Y'ë'ë.                                                *
 *                                                                           *
 * Uso permitido únicamente para:                                            *
 * - Evaluación académica                                                    *
 * - Revisión técnica                                                        *
 * - Convocatorias, hackatones o concursos                                   *
 *                                                                           *
 * Queda prohibida la copia, modificación, redistribución                    *
 * o uso sin autorización expresa del equipo.                                *
 *                                                                           *
 * El software se proporciona "tal cual", sin garantías.                     *
 */

import 'dart:math';
import 'package:flutter/material.dart';


class AnimatedBackground extends StatefulWidget {
  const AnimatedBackground({super.key});

  @override
  State<AnimatedBackground> createState() => _AnimatedBackgroundState();
}

class _AnimatedBackgroundState extends State<AnimatedBackground>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  final List<_Particle> _particles = [];
  final Random _random = Random();

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 20),
    )..repeat();

    for (int i = 0; i < 120; i++) {
      _particles.add(
        _Particle(
          position: Offset(_random.nextDouble(), _random.nextDouble()),
          color: _randomBlueColor(_random),
          speed: 0.5 + _random.nextDouble() * 1.0,
          size: 2 + _random.nextDouble() * 3,
        ),
      );
    }
  }

  Color _randomBlueColor(Random random) {
    final hue = 200 + random.nextInt(60); 
    final saturation = 0.7 + random.nextDouble() * 0.3;
    final lightness = 0.4 + random.nextDouble() * 0.3;
    return HSLColor.fromAHSL(1.0, hue.toDouble(), saturation, lightness)
        .toColor();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox.expand(
      child: AnimatedBuilder(
        animation: _controller,
        builder: (_, __) {
          return Stack(
            fit: StackFit.expand,
            children: [
              Container(color: Colors.black),
              CustomPaint(
                foregroundPainter:
                    _ParticlePainter(_particles, _controller.value),
                child: const SizedBox.expand(),
              ),
            ],
          );
        },
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}

class _Particle {
  final Offset position; 
  final Color color;
  final double speed;
  final double size;

  _Particle({
    required this.position,
    required this.color,
    required this.speed,
    required this.size,
  });
}

class _ParticlePainter extends CustomPainter {
  final List<_Particle> particles;
  final double progress;

  _ParticlePainter(this.particles, this.progress);

  @override
  void paint(Canvas canvas, Size size) {
    final Paint paint = Paint()
      ..maskFilter = MaskFilter.blur(BlurStyle.normal, 6.0)
      ..blendMode = BlendMode.plus;

    for (final p in particles) {
      final dx = (p.position.dx * size.width) +
          40 * sin(progress * 2 * pi * p.speed + p.position.dy * 2 * pi);
      final dy = (p.position.dy * size.height) +
          40 * cos(progress * 2 * pi * p.speed + p.position.dx * 2 * pi);

      final oscill = sin(progress * 2 * pi * p.speed);
      final scale = 1.0 + 0.35 * oscill;
      final opacity = (0.5 + 0.5 * (oscill * 0.6 + 0.4)).clamp(0.4, 1.0);

      paint.color = p.color.withOpacity(opacity);
      canvas.drawCircle(Offset(dx, dy), p.size * scale, paint);

      final Paint core = Paint()
        ..color = p.color.withOpacity((opacity + 0.8).clamp(0.6, 1.0))
        ..style = PaintingStyle.fill;
      canvas.drawCircle(Offset(dx, dy), (p.size * 0.5) * scale, core);
    }
  }

  @override
  bool shouldRepaint(covariant _ParticlePainter oldDelegate) => true;
}
