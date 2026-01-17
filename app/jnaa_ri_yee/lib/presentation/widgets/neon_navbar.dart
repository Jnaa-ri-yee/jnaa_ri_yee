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

  double _indicatorPosition = 0.0;
  final bool _isDragging = false;

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

    WidgetsBinding.instance.addPostFrameCallback((_) {
      setState(() {
        _indicatorPosition = widget.currentIndex.toDouble();
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          height: 80,
          margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 15),
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                Colors.black.withOpacity(0.8),
                Colors.black.withOpacity(0.6),
              ],
            ),
            borderRadius: BorderRadius.circular(40),
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
          child: Stack(
            children: [
              
              LayoutBuilder(builder: (context, constraints) {
                final segmentWidth = constraints.maxWidth / _navItems.length;
                final left = segmentWidth * _indicatorPosition + segmentWidth / 2 - 25;

                return AnimatedPositioned(
                  duration: _isDragging 
                      ? Duration.zero 
                      : const Duration(milliseconds: 400),
                  curve: Curves.elasticOut,
                  left: left,
                  top: 10,
                  child: Container(
                    width: 50,
                    height: 50,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          _colorAnimation.value!,
                          Colors.blueAccent.withOpacity(0.8),
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: _colorAnimation.value!.withOpacity(0.8),
                          blurRadius: _glowAnimation.value * 1.5,
                          spreadRadius: 2,
                        ),
                      ],
                    ),
                    child: Icon(
                      _navItems[widget.currentIndex].icon,
                      color: Colors.white,
                      size: 24,
                    ),
                  ),
                );
              }),

              
              Row(
                children: List.generate(_navItems.length, (index) {
                  final isSelected = widget.currentIndex == index;
                  return Expanded(
                    child: GestureDetector(
                      onTap: () => _onItemTapped(index),
                      behavior: HitTestBehavior.opaque,
                      child: SizedBox(
                        height: double.infinity,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              _navItems[index].icon,
                              color: isSelected 
                                  ? Colors.white 
                                  : Colors.blueAccent.withOpacity(0.5),
                              size: isSelected ? 28 : 24,
                            ),
                            const SizedBox(height: 4),
                            Text(
                              _navItems[index].label,
                              style: TextStyle(
                                color: isSelected 
                                    ? Colors.white 
                                    : Colors.blueAccent.withOpacity(0.7),
                                fontSize: isSelected ? 12 : 10,
                                fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  );
                }),
              ),
            ],
          ),
        );
      },
    );
  }

  void _onItemTapped(int index) {
    setState(() {
      _indicatorPosition = index.toDouble();
    });
    widget.onItemSelected(index);
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
