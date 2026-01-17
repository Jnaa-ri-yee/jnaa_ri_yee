/*
 * ======================================================                    *
 *  Project      : screens                                                   *
 *  File         : camera_screen.dart                                        *
 *  Team         : Equipo Jña'a Ri Y'ë'ë                                     *
 *  Developer    : Axel Eduardo Urbina Secundino                             *
 *  Created      : 2025-10-30                                                *
 *  Last Updated : 2026-01-16 22:02                                          *
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

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../widgets/animated_background.dart';
import '../state/camera_controller.dart';
import '../widgets/camera/camera_body.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController pulseCtrl;
  late Animation<double> pulse;

  @override
  void initState() {
    super.initState();
    pulseCtrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);
    pulse = CurvedAnimation(parent: pulseCtrl, curve: Curves.easeInOut);
  }

  @override
  void dispose() {
    pulseCtrl.dispose();
    context.read<CameraLogic>().disposeAll();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => CameraLogic(),
      child: Stack(
        children: [
          const AnimatedBackground(),
          CameraBody(pulse: pulse),
        ],
      ),
    );
  }
}
