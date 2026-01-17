/*
 * ======================================================                    *
 *  Project      : state                                                     *
 *  File         : camera_controller.dart                                    *
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

import 'dart:convert';
import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class CameraLogic extends ChangeNotifier {
  CameraController? controller;
  bool cameraVisible = false;
  bool isSending = false;
  bool loopActive = false;
  String predictionText = "Esperando detección...";

  Future<void> initCamera() async {
    final cameras = await availableCameras();
    controller = CameraController(
      cameras.first,
      ResolutionPreset.medium,
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.jpeg,
    );
    await controller!.initialize();
    cameraVisible = true;
    loopActive = true;
    notifyListeners();
    startLoop();
  }

  void disposeAll() {
    loopActive = false;
    controller?.dispose();
  }

  Future<void> startLoop() async {
    while (loopActive) {
      if (isSending || controller == null) {
        await Future.delayed(const Duration(milliseconds: 300));
        continue;
      }
      try {
        isSending = true;
        final pic = await controller!.takePicture();
        await Future.delayed(const Duration(milliseconds: 200));
        await sendFrame(File(pic.path));
        await Future.delayed(const Duration(milliseconds: 1500));
      } catch (_) {
        await Future.delayed(const Duration(seconds: 1));
      } finally {
        isSending = false;
      }
    }
  }

  Future<void> sendFrame(File file) async {
    try {
      final req = http.MultipartRequest(
        'POST',
        Uri.parse('https://interprete.jnaa-ri-yee.com/predict/'),
      );
      req.files.add(await http.MultipartFile.fromPath(
        'file',
        file.path,
        contentType: MediaType('image', 'jpeg'),
      ));

      final res = await req.send();
      final body = await res.stream.bytesToString();

      if (res.statusCode == 200) {
        final jsonResp = json.decode(body);
        predictionText =
            "Seña detectada: ${jsonResp['prediction']} (${(jsonResp['confidence'] * 100).toStringAsFixed(1)}%)";
      } else {
        predictionText = "Error del servidor (${res.statusCode})";
      }
    } catch (_) {
      predictionText = "Error de conexión con el servidor";
    } finally {
      if (await file.exists()) await file.delete();
      notifyListeners();
    }
  }
}
