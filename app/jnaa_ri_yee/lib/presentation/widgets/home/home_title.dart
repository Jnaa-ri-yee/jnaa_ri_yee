/*
 * ======================================================                    *
 *  Project      : home                                                      *
 *  File         : home_title.dart                                           *
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

import 'dart:ui';
import 'package:flutter/material.dart';

class HomeTitle extends StatelessWidget {
  final AnimationController glowController;
  const HomeTitle({super.key, required this.glowController});

  void showDialogMeaning(BuildContext context) {
    showGeneralDialog(
      context: context,
      barrierDismissible: true,
      barrierColor: Colors.black.withOpacity(0.8),
      transitionDuration: const Duration(milliseconds: 400),
      pageBuilder: (_, a1, __) => BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 8, sigmaY: 8),
        child: ScaleTransition(
          scale: CurvedAnimation(parent: a1, curve: Curves.easeOutBack),
          child: const _MeaningDialog(),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: GestureDetector(
        onTap: () => showDialogMeaning(context),
        child: AnimatedBuilder(
          animation: glowController,
          builder: (_, __) {
            final v = glowController.value;
            return Opacity(
              opacity: 0.5 + v * 0.5,
              child: Text(
                "jñ'a ri y'ë'ë",
                style: TextStyle(
                  fontSize: 44,
                  fontWeight: FontWeight.bold,
                  color: Colors.cyanAccent,
                  shadows: [
                    Shadow(blurRadius: 25 * v, color: Colors.cyanAccent),
                    const Shadow(blurRadius: 15, color: Colors.purpleAccent),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

class _MeaningDialog extends StatelessWidget {
  const _MeaningDialog();

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.black.withOpacity(0.85),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(mainAxisSize: MainAxisSize.min, children: const [
          Text("Significado de jñ'a ri y'ë'ë",
              textAlign: TextAlign.center,
              style: TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                  color: Colors.white)),
          SizedBox(height: 20),
          Text(
            "• jñ'a: hablar\n• ri: tiempo presente\n• y'ë'ë: mano\n\n“La mano que habla”",
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.white70, fontSize: 18),
          ),
        ]),
      ),
    );
  }
}
