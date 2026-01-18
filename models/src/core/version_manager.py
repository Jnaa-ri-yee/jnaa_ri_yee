# ======================================================                     *
#  Project      : core                                                       *
#  File         : version_manager.py                                         *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:45                                           *
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
Gestor automático de versiones de modelos.
"""

import json
import shutil
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional


class NumpyEncoder(json.JSONEncoder):
    """Encoder personalizado para manejar tipos de NumPy y otros tipos especiales."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32, np.float16)):
            return float(obj)
        return super(NumpyEncoder, self).default(obj)


class VersionManager:
    """Gestiona versiones de modelos automáticamente."""
    
    def __init__(self, base_dir: str = 'models'):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.registry_path = self.base_dir / 'registry' / 'model_registry.json'
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Carga el registro de modelos."""
        if self.registry_path.exists():
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'versions': [], 'current_version': 0}
    
    def _save_registry(self):
        """Guarda el registro de modelos."""
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            # CAMBIO CRÍTICO: Usa NumpyEncoder
            json.dump(self.registry, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
    
    def _convert_numpy_types(self, obj):
        """
        Convierte recursivamente tipos NumPy a tipos nativos de Python.
        
        Args:
            obj: Objeto a convertir (puede ser dict, list, numpy type, etc.)
        
        Returns:
            Objeto con tipos nativos de Python
        """
        if isinstance(obj, dict):
            return {k: self._convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_numpy_types(item) for item in obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
            return int(obj)
        elif isinstance(obj, (np.float64, np.float32, np.float16)):
            return float(obj)
        else:
            return obj
    
    def create_new_version(
        self,
        model_info: Dict,
        metrics: Dict,
        config: Dict,
        force: bool = False
    ) -> str:
        """
        Crea una nueva versión automáticamente.
        
        Args:
            model_info: Información del modelo
            metrics: Métricas del modelo
            config: Configuración usada
            force: Forzar creación aunque no haya mejora
        
        Returns:
            Nombre de la versión creada (ej: 'v1', 'v2')
        """
        # CAMBIO CRÍTICO: Convertir tipos NumPy antes de procesar
        model_info = self._convert_numpy_types(model_info)
        metrics = self._convert_numpy_types(metrics)
        config = self._convert_numpy_types(config)
        
        # Determinar si crear nueva versión
        should_create = self._should_create_version(metrics, force)
        
        if not should_create:
            print("No se creó nueva versión (no hay mejora significativa)")
            return None
        
        # Incrementar versión
        new_version_num = self.registry['current_version'] + 1
        version_name = f"v{new_version_num}"
        
        # Crear directorios de la versión
        version_dir = self.base_dir / version_name
        self._create_version_structure(version_dir)
        
        # Guardar metadata
        metadata = {
            'version': version_name,
            'version_number': new_version_num,
            'created_at': datetime.now().isoformat(),
            'model_info': model_info,
            'metrics': metrics,
            'config': config,
            'improvements': self._calculate_improvements(metrics)
        }
        
        metadata_path = version_dir / 'metadata' / 'model_info.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            # CAMBIO CRÍTICO: Usa NumpyEncoder
            json.dump(metadata, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
        
        # Actualizar registro
        self.registry['versions'].append(metadata)
        self.registry['current_version'] = new_version_num
        self._save_registry()
        
        # Crear evaluación
        eval_dir = Path('evaluation') / version_name
        eval_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Versión {version_name} creada exitosamente")
        print(f"Modelos en: {version_dir}")
        print(f"Evaluación en: {eval_dir}")
        
        return version_name
    
    def _should_create_version(self, metrics: Dict, force: bool) -> bool:
        """Decide si crear nueva versión basado en mejoras."""
        if force:
            return True
        
        if not self.registry['versions']:
            return True  # Primera versión
        
        # Obtener métricas de la última versión
        last_metrics = self.registry['versions'][-1]['metrics']
        
        # Verificar mejora
        current_acc = metrics.get('test_accuracy', 0)
        last_acc = last_metrics.get('test_accuracy', 0)
        
        improvement = current_acc - last_acc
        
        # Crear si hay mejora > 1%
        return improvement > 0.01
    
    def _calculate_improvements(self, metrics: Dict) -> Dict:
        """Calcula mejoras respecto a versión anterior."""
        if not self.registry['versions']:
            return {'baseline': True}
        
        last_metrics = self.registry['versions'][-1]['metrics']
        improvements = {}
        
        for key in metrics:
            if key in last_metrics:
                # Asegurar que son floats nativos
                current_val = float(metrics[key]) if metrics[key] is not None else 0.0
                last_val = float(last_metrics[key]) if last_metrics[key] is not None else 0.0
                
                diff = current_val - last_val
                improvements[key] = {
                    'absolute': float(diff),
                    'relative': float((diff / last_val * 100) if last_val != 0 else 0)
                }
        
        return improvements
    
    def _create_version_structure(self, version_dir: Path):
        """Crea estructura de directorios para la versión."""
        subdirs = [
            'checkpoints',
            'final',
            'config',
            'metadata',
            'artifacts'
        ]
        
        for subdir in subdirs:
            (version_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def get_best_version(self, metric: str = 'test_accuracy') -> Optional[str]:
        """Retorna la mejor versión según una métrica."""
        if not self.registry['versions']:
            return None
        
        best_version = max(
            self.registry['versions'],
            key=lambda v: float(v['metrics'].get(metric, 0))
        )
        
        return best_version['version']
    
    def get_version_info(self, version: str) -> Optional[Dict]:
        """Obtiene información de una versión específica."""
        for v in self.registry['versions']:
            if v['version'] == version:
                return v
        return None
    
    def list_versions(self) -> list:
        """Lista todas las versiones disponibles."""
        return [
            {
                'version': v['version'],
                'created_at': v['created_at'],
                'test_accuracy': v['metrics'].get('test_accuracy', 0),
                'test_f1': v['metrics'].get('test_f1', 0)
            }
            for v in self.registry['versions']
        ]
    
    def delete_version(self, version: str) -> bool:
        """
        Elimina una versión específica.
        
        Args:
            version: Nombre de la versión (ej: 'v1')
        
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        version_dir = self.base_dir / version
        
        if not version_dir.exists():
            print(f"Versión {version} no encontrada")
            return False
        
        # Eliminar directorio
        shutil.rmtree(version_dir)
        
        # Actualizar registro
        self.registry['versions'] = [
            v for v in self.registry['versions'] 
            if v['version'] != version
        ]
        self._save_registry()
        
        print(f"Versión {version} eliminada")
        return True
    
    def compare_versions(self, version1: str, version2: str) -> Dict:
        """
        Compara dos versiones.
        
        Args:
            version1: Primera versión
            version2: Segunda versión
        
        Returns:
            Diccionario con la comparación
        """
        v1_info = self.get_version_info(version1)
        v2_info = self.get_version_info(version2)
        
        if not v1_info or not v2_info:
            return {'error': 'Una o ambas versiones no existen'}
        
        comparison = {
            'version1': version1,
            'version2': version2,
            'metrics_comparison': {},
            'improvements': {}
        }
        
        # Comparar métricas
        for key in v1_info['metrics']:
            if key in v2_info['metrics']:
                val1 = float(v1_info['metrics'][key])
                val2 = float(v2_info['metrics'][key])
                diff = val2 - val1
                
                comparison['metrics_comparison'][key] = {
                    version1: val1,
                    version2: val2,
                    'difference': diff,
                    'improvement_pct': (diff / val1 * 100) if val1 != 0 else 0
                }
        
        return comparison
    
    def export_version(self, version: str, output_path: str) -> bool:
        """
        Exporta una versión a un archivo comprimido.
        
        Args:
            version: Nombre de la versión
            output_path: Ruta donde guardar el archivo
        
        Returns:
            True si se exportó correctamente
        """
        version_dir = self.base_dir / version
        
        if not version_dir.exists():
            print(f"Versión {version} no encontrada")
            return False
        
        # Crear archivo comprimido
        shutil.make_archive(output_path, 'zip', version_dir)
        print(f"Versión {version} exportada a {output_path}.zip")
        
        return True