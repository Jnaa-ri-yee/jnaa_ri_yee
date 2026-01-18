# ======================================================                     *
#  Project      : core                                                       *
#  File         : auto_config_generator.py                                   *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:34                                           *
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
Genera automáticamente configuraciones de entrenamiento basadas en el dataset.
"""

from typing import Dict  # ← AGREGAR ESTA LÍNEA
from pathlib import Path
import yaml

class AutoConfigGenerator:
    """Genera configuraciones automáticas para entrenamiento."""
    
    def __init__(self, dataset_report: Dict):
        self.report = dataset_report
        self.config = {}
    
    def generate(self) -> Dict:
        """Genera configuración completa automáticamente."""
        
        self.config = {
            'dataset': self._generate_dataset_config(),
            'model': self._generate_model_config(),
            'training': self._generate_training_config(),
            'augmentation': self._generate_augmentation_config(),
            'features': self._generate_features_config()
        }
        
        return self.config
    
    def _generate_dataset_config(self) -> Dict:
        """Configuración del dataset."""
        return {
            'path': self.report['dataset_path'],
            'type': self.report['dataset_type'],
            'num_classes': self.report['total_classes'],
            'class_names': self.report['classes'],
            'split_ratio': {
                'train': 0.7,
                'val': 0.15,
                'test': 0.15
            },
            'batch_size': self._calculate_batch_size(),
            'num_workers': 4
        }
    
    def _generate_model_config(self) -> Dict:
        """Configuración del modelo basada en tipo de datos."""
        dataset_type = self.report['dataset_type']
        num_classes = self.report['total_classes']
        
        if dataset_type == 'image':
            return {
                'type': 'hybrid',
                'architecture': 'cnn_landmark_fusion',
                'backbone': 'efficientnet_b0',
                'use_landmarks': True,
                'num_classes': num_classes,
                'pretrained': True
            }
        elif dataset_type == 'video':
            return {
                'type': 'hybrid',
                'architecture': 'two_stream_lstm',
                'spatial_backbone': 'resnet18',
                'temporal_model': 'lstm',
                'use_landmarks': True,
                'num_classes': num_classes,
                'sequence_length': 30
            }
        else:  # mixed
            return {
                'type': 'hybrid',
                'architecture': 'multi_modal',
                'image_backbone': 'efficientnet_b0',
                'video_backbone': 'r3d_18',
                'use_landmarks': True,
                'num_classes': num_classes
            }
    
    def _generate_training_config(self) -> Dict:
        """Configuración de entrenamiento."""
        total_samples = self.report['distribution']['total_files']
        
        return {
            'epochs': self._calculate_epochs(total_samples),
            'learning_rate': 0.001,
            'optimizer': 'adamw',
            'scheduler': 'cosine_annealing',
            'loss': 'cross_entropy',
            'metrics': ['accuracy', 'f1_score', 'precision', 'recall'],
            'early_stopping': {
                'patience': 10,
                'min_delta': 0.001
            },
            'checkpointing': {
                'save_best': True,
                'save_frequency': 5
            }
        }
    
    def _generate_augmentation_config(self) -> Dict:
        """Configuración de augmentación."""
        dataset_type = self.report['dataset_type']
        
        base_aug = {
            'image': {
                'resize': [224, 224],
                'horizontal_flip': 0.5,
                'rotation': 15,
                'brightness': 0.2,
                'contrast': 0.2,
                'normalization': {
                    'mean': [0.485, 0.456, 0.406],
                    'std': [0.229, 0.224, 0.225]
                }
            }
        }
        
        if dataset_type == 'video':
            base_aug['video'] = {
                'temporal_sampling': 'uniform',
                'num_frames': 30,
                'temporal_jitter': True
            }
        
        return base_aug
    
    def _generate_features_config(self) -> Dict:
        """Configuración de extracción de features."""
        return {
            'landmarks': {
                'enabled': True,
                'hands': True,
                'pose': True,
                'face': False  # Opcional para expresiones
            },
            'engineered_features': {
                'geometric': True,
                'statistical': True,
                'temporal': self.report['dataset_type'] in ['video', 'mixed']
            }
        }
    
    def _calculate_batch_size(self) -> int:
        """Calcula batch size óptimo."""
        total_samples = self.report['distribution']['total_files']
        
        if total_samples < 100:
            return 8
        elif total_samples < 1000:
            return 16
        elif total_samples < 10000:
            return 32
        else:
            return 64
    
    def _calculate_epochs(self, total_samples: int) -> int:
        """Calcula número de epochs recomendado."""
        if total_samples < 100:
            return 100
        elif total_samples < 1000:
            return 50
        else:
            return 30
    
    def save(self, output_path: str):
        """Guarda la configuración generada."""
        config_path = Path(output_path) / 'auto_generated_config.yaml'
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        
        print(f"Configuración guardada en: {config_path}")
