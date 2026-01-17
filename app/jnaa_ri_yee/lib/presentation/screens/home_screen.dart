/*
 * ======================================================                    *
 *  Project      : screens                                                   *
 *  File         : home_screen.dart                                          *
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
import '../widgets/animated_background.dart';
import '../widgets/neon_navbar.dart';
import '../widgets/home/home_title.dart';

import 'camera_screen.dart';
import 'info_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen>
    with SingleTickerProviderStateMixin {
  int _selectedIndex = 0;
  late AnimationController glowController;

  final screens = [
    const SizedBox.shrink(),
    const CameraScreen(),
    const InfoScreen(),
  ];

  @override
  void initState() {
    super.initState();
    glowController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    glowController.dispose();
    super.dispose();
  }

  void onNav(int i) => setState(() => _selectedIndex = i);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          const AnimatedBackground(),
          IndexedStack(
            index: _selectedIndex,
            children: [
              HomeTitle(glowController: glowController),
              ...screens.sublist(1), // Ahora todo son Widgets
            ],
          ),
        ],
      ),
      bottomNavigationBar: NeonNavbar(
        currentIndex: _selectedIndex,
        onItemSelected: onNav,
      ),
    );
  }
}
