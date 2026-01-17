/*
 * ======================================================                    *
 *  Project      : camera                                                    *
 *  File         : camera_body.dart                                          *
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
import '../../state/camera_controller.dart';
import 'camera_activate_button.dart';
import 'camera_preview_box.dart';
import 'prediction_panel.dart';

class CameraBody extends StatelessWidget {
  final Animation<double> pulse;
  const CameraBody({super.key, required this.pulse});

  @override
  Widget build(BuildContext context) {
    final logic = context.watch<CameraLogic>();

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text("Traducción en Tiempo Real",
              style: TextStyle(
                  color: Colors.white,
                  fontSize: 28,
                  fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          const Text(
            "Activa la cámara y muestra las señas para obtener la traducción.",
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.white70),
          ),
          const SizedBox(height: 40),
          if (!logic.cameraVisible)
            CameraActivateButton(
              onTap: logic.initCamera,
              pulse: pulse,
            )
          else if (logic.controller != null)
            Expanded(
              child: Column(
                children: [
                  CameraPreviewBox(controller: logic.controller!),
                  const SizedBox(height: 20),
                  PredictionPanel(text: logic.predictionText),
                  const SizedBox(height: 20),
                  const Text(
                    "Enfoca tus manos en el centro",
                    style: TextStyle(color: Colors.white70),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
