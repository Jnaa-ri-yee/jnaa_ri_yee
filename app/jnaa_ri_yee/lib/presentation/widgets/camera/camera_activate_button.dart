/*
 * ======================================================                    *
 *  Project      : camera                                                    *
 *  File         : camera_activate_button.dart                               *
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

class CameraActivateButton extends StatelessWidget {
  final VoidCallback onTap;
  final Animation<double> pulse;

  const CameraActivateButton({
    super.key,
    required this.onTap,
    required this.pulse,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: pulse,
      builder: (_, __) => Transform.scale(
        scale: 1.0 + pulse.value * 0.1,
        child: ElevatedButton.icon(
          onPressed: onTap,
          icon: const Icon(Icons.camera_alt, color: Colors.white),
          label: const Text("Activar Cámara",
              style: TextStyle(color: Colors.white, fontSize: 18)),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.transparent,
            padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 18),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(30),
              side: const BorderSide(color: Colors.cyanAccent, width: 2),
            ),
          ),
        ),
      ),
    );
  }
}
