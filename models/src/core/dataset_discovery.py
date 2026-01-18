# ======================================================                     *
#  Project      : core                                                       *
#  File         : dataset_discovery.py                                       *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:33                                           *
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
Sistema autónomo de descubrimiento de datasets.
Detecta automáticamente la estructura y tipo de datos.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import yaml

class DatasetDiscovery:
    """Descubre y analiza automáticamente cualquier estructura de dataset."""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.structure = {}
        self.classes = []
        self.dataset_type = None  # 'image', 'video', 'mixed'
        self.hierarchy = {}
        self.metadata = {}
        
    def discover(self) -> Dict:
        """Descubre toda la estructura del dataset automáticamente."""
        print(f"Descubriendo dataset en: {self.dataset_path}")
        
        # 1. Analizar estructura de carpetas
        self.structure = self._analyze_directory_structure()
        
        # 2. Detectar tipo de datos (imágenes, videos, mixto)
        self.dataset_type = self._detect_data_type()
        
        # 3. Extraer clases automáticamente
        self.classes = self._extract_classes()
        
        # 4. Detectar jerarquía (alfabeto/consonantes/b, palabras/saludos/hola)
        self.hierarchy = self._detect_hierarchy()
        
        # 5. Analizar distribución de datos
        self.metadata = self._analyze_distribution()
        
        # 6. Generar reporte
        report = self._generate_report()
        
        print(f"Dataset descubierto: {len(self.classes)} clases")
        print(f"Tipo: {self.dataset_type}")
        print(f"Jerarquía detectada: {self._get_hierarchy_summary()}")
        
        return report
    
    def _analyze_directory_structure(self) -> Dict:
        """Analiza recursivamente la estructura de directorios."""
        structure = {
            'root': str(self.dataset_path),
            'tree': {},
            'all_paths': [],
            'leaf_dirs': []  # Directorios que contienen archivos
        }
        
        for root, dirs, files in os.walk(self.dataset_path):
            rel_path = os.path.relpath(root, self.dataset_path)
            
            # Filtrar archivos válidos (imágenes/videos)
            valid_files = [f for f in files if self._is_valid_file(f)]
            
            if valid_files:  # Es un directorio hoja con archivos
                structure['leaf_dirs'].append({
                    'path': root,
                    'relative_path': rel_path,
                    'name': os.path.basename(root),
                    'files': valid_files,
                    'count': len(valid_files)
                })
                structure['all_paths'].append(rel_path)
        
        return structure
    
    def _detect_data_type(self) -> str:
        """Detecta si el dataset contiene imágenes, videos o ambos."""
        image_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        video_exts = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
        
        has_images = False
        has_videos = False
        
        for leaf_dir in self.structure['leaf_dirs']:
            for file in leaf_dir['files']:
                ext = os.path.splitext(file)[1].lower()
                if ext in image_exts:
                    has_images = True
                if ext in video_exts:
                    has_videos = True
        
        if has_images and has_videos:
            return 'mixed'
        elif has_videos:
            return 'video'
        else:
            return 'image'
    
    def _extract_classes(self) -> List[str]:
        """Extrae automáticamente las clases del dataset."""
        classes = []
        
        for leaf_dir in self.structure['leaf_dirs']:
            class_name = leaf_dir['name']
            # Limpiar nombre de clase
            class_name = self._normalize_class_name(class_name)
            if class_name not in classes:
                classes.append(class_name)
        
        return sorted(classes)
    
    def _detect_hierarchy(self) -> Dict:
        """Detecta la jerarquía del dataset (ej: alfabeto/consonantes/b)."""
        hierarchy = defaultdict(lambda: defaultdict(list))
        
        for leaf_dir in self.structure['leaf_dirs']:
            path_parts = Path(leaf_dir['relative_path']).parts
            
            if len(path_parts) == 1:
                # Sin jerarquía (flat)
                hierarchy['flat']['classes'].append(leaf_dir['name'])
            elif len(path_parts) == 2:
                # Un nivel (ej: consonantes/b)
                category = path_parts[0]
                class_name = path_parts[1]
                hierarchy[category]['classes'].append(class_name)
            else:
                # Múltiples niveles (ej: alfabeto/consonantes/b)
                main_category = path_parts[0]
                sub_category = '/'.join(path_parts[1:-1])
                class_name = path_parts[-1]
                
                if main_category not in hierarchy:
                    hierarchy[main_category] = {}
                if sub_category not in hierarchy[main_category]:
                    hierarchy[main_category][sub_category] = []
                
                hierarchy[main_category][sub_category].append(class_name)
        
        return dict(hierarchy)
    
    def _analyze_distribution(self) -> Dict:
        """Analiza la distribución de datos por clase."""
        distribution = {
            'total_files': 0,
            'total_classes': len(self.classes),
            'files_per_class': {},
            'min_samples': float('inf'),
            'max_samples': 0,
            'avg_samples': 0,
            'imbalance_ratio': 0,
            'class_hierarchy': {}
        }
        
        for leaf_dir in self.structure['leaf_dirs']:
            class_name = self._normalize_class_name(leaf_dir['name'])
            count = leaf_dir['count']
            
            distribution['files_per_class'][class_name] = count
            distribution['total_files'] += count
            distribution['min_samples'] = min(distribution['min_samples'], count)
            distribution['max_samples'] = max(distribution['max_samples'], count)
        
        if distribution['total_classes'] > 0:
            distribution['avg_samples'] = distribution['total_files'] / distribution['total_classes']
            distribution['imbalance_ratio'] = distribution['max_samples'] / max(distribution['min_samples'], 1)
        
        return distribution
    
    def _is_valid_file(self, filename: str) -> bool:
        """Verifica si un archivo es válido (imagen o video)."""
        valid_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', 
                      '.mp4', '.avi', '.mov', '.mkv', '.webm'}
        ext = os.path.splitext(filename)[1].lower()
        return ext in valid_exts
    
    def _normalize_class_name(self, name: str) -> str:
        """Normaliza el nombre de una clase."""
        # Convertir guiones y underscores a espacios
        name = name.replace('-', ' ').replace('_', ' ')
        # Mantener ñ y caracteres especiales
        return name.strip().lower()
    
    def _get_hierarchy_summary(self) -> str:
        """Genera un resumen de la jerarquía."""
        if not self.hierarchy:
            return "flat"
        
        levels = []
        for main_cat, sub_cats in self.hierarchy.items():
            if isinstance(sub_cats, dict):
                for sub_cat in sub_cats.keys():
                    levels.append(f"{main_cat}/{sub_cat}")
            else:
                levels.append(main_cat)
        
        return ', '.join(levels[:3]) + ('...' if len(levels) > 3 else '')
    
    def _generate_report(self) -> Dict:
        """Genera un reporte completo del dataset."""
        return {
            'dataset_path': str(self.dataset_path),
            'dataset_type': self.dataset_type,
            'total_classes': len(self.classes),
            'classes': self.classes,
            'hierarchy': self.hierarchy,
            'distribution': self.metadata,
            'structure': {
                'total_directories': len(self.structure['leaf_dirs']),
                'paths': self.structure['all_paths']
            }
        }
    
    def save_report(self, output_path: str):
        """Guarda el reporte en formato JSON y YAML."""
        report = self._generate_report()
        
        # Guardar como JSON
        json_path = Path(output_path) / 'dataset_discovery.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Guardar como YAML
        yaml_path = Path(output_path) / 'dataset_discovery.yaml'
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(report, f, default_flow_style=False, allow_unicode=True)
        
        print(f"Reporte guardado en: {json_path}")
        print(f"Reporte guardado en: {yaml_path}")
    
    def get_data_loaders_config(self) -> Dict:
        """Genera configuración automática para los data loaders."""
        config = {
            'dataset_path': str(self.dataset_path),
            'dataset_type': self.dataset_type,
            'num_classes': len(self.classes),
            'class_names': self.classes,
            'class_to_idx': {cls: idx for idx, cls in enumerate(self.classes)},
            'data_paths': []
        }
        
        # Generar paths para cada clase
        for leaf_dir in self.structure['leaf_dirs']:
            class_name = self._normalize_class_name(leaf_dir['name'])
            class_idx = config['class_to_idx'][class_name]
            
            config['data_paths'].append({
                'class_name': class_name,
                'class_idx': class_idx,
                'path': leaf_dir['path'],
                'num_samples': leaf_dir['count'],
                'files': leaf_dir['files']
            })
        
        return config