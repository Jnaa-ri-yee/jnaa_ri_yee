# ======================================================                     *
#  Project      : deep                                                       *
#  File         : simple_hybrid_model.py                                     *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 16:33                                           *
# ======================================================                     *
#                                                                            *
#  License:                                                                  *
# © 2026 Equipo Jña'a Ri Y'ë'ë                                               *
#                                                                            *
# Este software y su código fuente son propiedad exclusiva                   *
# del equipo Jña'a Ri Y'ë'ë.                                                 *
#                                                                            *
# Uso permitido únicamente para:                                             *
# - Evaluación académica                                                     *
# - Revisión técnica                                                         *
# - Convocatorias, hackatones o concursos                                    *
#                                                                            *
# Queda prohibida la copia, modificación, redistribución                     *
# o uso sin autorización expresa del equipo.                                 *
#                                                                            *
# El software se proporciona "tal cual", sin garantías.                      *

"""
Modelo híbrido: CNN + Landmarks
Optimizado para clasificación de señas.
"""

import torch
import torch.nn as nn
from torchvision import models


class SimpleHybridModel(nn.Module):
    """
    Modelo híbrido que combina features visuales (CNN) con landmarks.
    
    Arquitectura:
        - Visual Branch: CNN pre-entrenada (EfficientNet, ResNet, etc.)
        - Landmark Branch: MLP para procesar landmarks de MediaPipe
        - Fusion: Concatenación de features
        - Classifier: Capas densas para clasificación final
    """
    
    def __init__(
        self,
        num_classes: int,
        backbone: str = 'efficientnet_b0',
        use_landmarks: bool = True,
        pretrained: bool = True,
        dropout: float = 0.5
    ):
        """
        Args:
            num_classes: Número de clases a predecir
            backbone: Arquitectura CNN ('efficientnet_b0', 'resnet18', 'mobilenet_v2')
            use_landmarks: Si usar landmarks de MediaPipe
            pretrained: Si usar pesos pre-entrenados en ImageNet
            dropout: Tasa de dropout
        """
        super().__init__()
        
        self.num_classes = num_classes
        self.use_landmarks = use_landmarks
        self.backbone_name = backbone
        
        # ==================== VISUAL BRANCH ====================
        self.visual_backbone, visual_features = self._create_backbone(
            backbone, pretrained
        )
        
        # ==================== LANDMARK BRANCH ====================
        if use_landmarks:
            landmark_dim = 126  # 2 manos × 21 puntos × 3 coords (x, y, z)
            
            self.landmark_processor = nn.Sequential(
                nn.Linear(landmark_dim, 256),
                nn.BatchNorm1d(256),
                nn.ReLU(inplace=True),
                nn.Dropout(dropout * 0.6),
                
                nn.Linear(256, 128),
                nn.BatchNorm1d(128),
                nn.ReLU(inplace=True),
                nn.Dropout(dropout * 0.6)
            )
            
            total_features = visual_features + 128
        else:
            total_features = visual_features
        
        # ==================== CLASSIFIER ====================
        self.classifier = nn.Sequential(
            nn.Linear(total_features, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout * 0.8),
            
            nn.Linear(256, num_classes)
        )
        
        # Inicializar pesos del classifier
        self._init_weights()
    
    def _create_backbone(self, backbone: str, pretrained: bool):
        """Crea el backbone CNN."""
        
        if backbone == 'efficientnet_b0':
            model = models.efficientnet_b0(pretrained=pretrained)
            features_dim = 1280
            # Remover classifier
            model.classifier = nn.Identity()
        
        elif backbone == 'resnet18':
            model = models.resnet18(pretrained=pretrained)
            features_dim = 512
            # Remover capa final
            model.fc = nn.Identity()
        
        elif backbone == 'resnet34':
            model = models.resnet34(pretrained=pretrained)
            features_dim = 512
            model.fc = nn.Identity()
        
        elif backbone == 'mobilenet_v2':
            model = models.mobilenet_v2(pretrained=pretrained)
            features_dim = 1280
            model.classifier = nn.Identity()
        
        else:
            raise ValueError(
                f"Backbone '{backbone}' no soportado. "
                f"Usa: efficientnet_b0, resnet18, resnet34, mobilenet_v2"
            )
        
        return model, features_dim
    
    def _init_weights(self):
        """Inicializa pesos del classifier."""
        for m in self.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
    
    def forward(self, image, landmarks=None):
        """
        Forward pass.
        
        Args:
            image: Tensor [batch_size, 3, 224, 224]
            landmarks: Tensor [batch_size, 126] (opcional)
        
        Returns:
            logits: Tensor [batch_size, num_classes]
        """
        # Procesar imagen
        visual_features = self.visual_backbone(image)
        
        # Combinar con landmarks si están disponibles
        if self.use_landmarks and landmarks is not None:
            # Verificar que landmarks no sean todos ceros (no se detectaron manos)
            landmarks_valid = landmarks.abs().sum(dim=1) > 0
            
            if landmarks_valid.any():
                landmark_features = self.landmark_processor(landmarks)
                features = torch.cat([visual_features, landmark_features], dim=1)
            else:
                # Si no hay landmarks válidos, usar solo visual features
                # Padding con ceros
                batch_size = visual_features.size(0)
                landmark_padding = torch.zeros(
                    batch_size, 128, 
                    device=visual_features.device
                )
                features = torch.cat([visual_features, landmark_padding], dim=1)
        else:
            features = visual_features
        
        # Clasificar
        output = self.classifier(features)
        return output
    
    def get_feature_extractor(self):
        """
        Retorna el modelo sin el classifier para extraer features.
        Útil para transfer learning o ensemble.
        """
        class FeatureExtractor(nn.Module):
            def __init__(self, parent_model):
                super().__init__()
                self.visual_backbone = parent_model.visual_backbone
                self.landmark_processor = parent_model.landmark_processor if parent_model.use_landmarks else None
                self.use_landmarks = parent_model.use_landmarks
            
            def forward(self, image, landmarks=None):
                visual_features = self.visual_backbone(image)
                
                if self.use_landmarks and landmarks is not None:
                    landmark_features = self.landmark_processor(landmarks)
                    features = torch.cat([visual_features, landmark_features], dim=1)
                else:
                    features = visual_features
                
                return features
        
        return FeatureExtractor(self)
