/*
 * ======================================================                    *
 *  Project      : widgets                                                   *
 *  File         : neon_navbar.dart                                          *
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

import 'package:flutter/material.dart';

class NeonNavbar extends StatefulWidget {
  final int currentIndex;
  final Function(int) onItemSelected;

  const NeonNavbar({
    super.key,
    required this.currentIndex,
    required this.onItemSelected,
  });

  @override
  State<NeonNavbar> createState() => _NeonNavbarState();
}

class _NeonNavbarState extends State<NeonNavbar>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _glowAnimation;
  late Animation<Color?> _colorAnimation;

  final List<NavItem> _navItems = [
    NavItem(icon: Icons.home_rounded, label: 'Inicio'),
    NavItem(icon: Icons.camera_alt_rounded, label: 'Cámara'),
    NavItem(icon: Icons.info_rounded, label: 'Info'),
  ];

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2000),
    )..repeat(reverse: true);

    _glowAnimation = Tween<double>(begin: 8.0, end: 15.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    _colorAnimation = ColorTween(
      begin: Colors.blueAccent.withOpacity(0.7),
      end: Colors.cyanAccent.withOpacity(0.9),
    ).animate(_controller);
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          height: 70,
          margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                const Color(0xFF1a1a2e).withOpacity(0.95),
                const Color(0xFF16213e).withOpacity(0.95),
              ],
            ),
            borderRadius: BorderRadius.circular(35),
            border: Border.all(
              color: _colorAnimation.value!,
              width: 1.5,
            ),
            boxShadow: [
              BoxShadow(
                color: _colorAnimation.value!.withOpacity(0.6),
                blurRadius: _glowAnimation.value,
                spreadRadius: 1,
              ),
              BoxShadow(
                color: Colors.black.withOpacity(0.3),
                blurRadius: 10,
                spreadRadius: 2,
              ),
            ],
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(35),
            child: Row(
              children: _navItems.asMap().entries.map((entry) {
                final index = entry.key;
                final item = entry.value;
                final isSelected = widget.currentIndex == index;
                
                return Expanded(
                  child: Material(
                    color: Colors.transparent,
                    child: InkWell(
                      onTap: () => widget.onItemSelected(index),
                      borderRadius: BorderRadius.circular(35),
                      splashColor: Colors.cyanAccent.withOpacity(0.2),
                      highlightColor: Colors.blueAccent.withOpacity(0.1),
                      child: Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              item.icon,
                              color: isSelected 
                                  ? Colors.white 
                                  : Colors.blueAccent.withOpacity(0.5),
                              size: isSelected ? 26 : 24,
                            ),
                            const SizedBox(height: 4),
                            Text(
                              item.label,
                              style: TextStyle(
                                color: isSelected 
                                    ? Colors.white 
                                    : Colors.blueAccent.withOpacity(0.7),
                                fontSize: isSelected ? 12 : 11,
                                fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                );
              }).toList(),
            ),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}

class NavItem {
  final IconData icon;
  final String label;

  NavItem({required this.icon, required this.label});
}