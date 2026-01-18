# ======================================================                     *
#  Project      : loaders                                                    *
#  File         : universal_loader.py                                        *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 16:27                                           *
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
Data loader universal que funciona con cualquier estructura de dataset.
Soporta imágenes y videos con split automático.
"""

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml
import random


class UniversalImageDataset(Dataset):
    """Dataset universal para imágenes de cualquier estructura."""
    
    def __init__(
        self,
        data_config: Dict,
        split: str = 'train',
        transform: Optional[transforms.Compose] = None,
        extract_landmarks: bool = True,
        split_ratios: Dict = None
    ):
        """
        Args:
            data_config: Configuración del dataset
            split: 'train', 'val' o 'test'
            transform: Transformaciones de imagen
            extract_landmarks: Si extraer landmarks con MediaPipe
            split_ratios: Proporciones de split (train/val/test)
        """
        self.data_config = data_config
        self.split = split
        self.transform = transform
        self.extract_landmarks = extract_landmarks
        
        if split_ratios is None:
            split_ratios = {'train': 0.7, 'val': 0.15, 'test': 0.15}
        
        # Cargar MediaPipe si es necesario
        self.hands = None
        if extract_landmarks:
            try:
                import mediapipe as mp
                # CAMBIO: Manejo compatible con diferentes versiones de MediaPipe
                if hasattr(mp, 'solutions'):
                    # MediaPipe versión antigua (< 0.10.8)
                    self.mp_hands = mp.solutions.hands
                    self.hands = self.mp_hands.Hands(
                        static_image_mode=True,
                        max_num_hands=2,
                        min_detection_confidence=0.5
                    )
                else:
                    # MediaPipe versión nueva (>= 0.10.8)
                    from mediapipe.python.solutions import hands as mp_hands
                    self.mp_hands = mp_hands
                    self.hands = mp_hands.Hands(
                        static_image_mode=True,
                        max_num_hands=2,
                        min_detection_confidence=0.5
                    )
                print("✅ MediaPipe Hands inicializado correctamente")
            except ImportError:
                print("⚠️ MediaPipe no instalado. Landmarks desactivados.")
                self.extract_landmarks = False
            except AttributeError as e:
                print(f"⚠️ Error de compatibilidad con MediaPipe: {e}")
                print("⚠️ Intentando sin MediaPipe...")
                self.extract_landmarks = False
        
        # Construir lista de samples con split
        self.samples = self._build_samples_with_split(split_ratios)
        self.class_to_idx = data_config['class_to_idx']
        
        print(f"{split.capitalize()}: {len(self.samples)} muestras")
    
    def _build_samples_with_split(self, split_ratios: Dict) -> List[Tuple[str, int]]:
        """Construye lista de samples con split estratificado por clase."""
        all_samples_by_class = {}
        
        # Agrupar por clase
        for class_data in self.data_config['data_paths']:
            class_path = Path(class_data['path'])
            class_idx = class_data['class_idx']
            
            samples = []
            for file_name in class_data['files']:
                file_path = class_path / file_name
                if file_path.exists():
                    samples.append((str(file_path), class_idx))
            
            if samples:
                all_samples_by_class[class_idx] = samples
        
        # Split estratificado por clase
        split_samples = []
        for class_idx, class_samples in all_samples_by_class.items():
            # Shuffle con seed fijo para reproducibilidad
            random.seed(42)
            random.shuffle(class_samples)
            
            n_samples = len(class_samples)
            n_train = int(n_samples * split_ratios['train'])
            n_val = int(n_samples * split_ratios['val'])
            
            # Asegurar al menos 1 muestra por split si es posible
            if n_samples >= 3:
                n_train = max(1, n_train)
                n_val = max(1, n_val)
            elif n_samples == 2:
                n_train = 1
                n_val = 0
            else:  # n_samples == 1
                n_train = 1
                n_val = 0
            
            # Asignar samples al split correspondiente
            if self.split == 'train':
                split_samples.extend(class_samples[:n_train])
            elif self.split == 'val':
                split_samples.extend(class_samples[n_train:n_train + n_val])
            else:  # test
                split_samples.extend(class_samples[n_train + n_val:])
        
        # Shuffle final
        random.shuffle(split_samples)
        return split_samples
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Dict:
        """
        Retorna un sample del dataset.
        
        Returns:
            Dict con 'image', 'landmarks', 'label', 'class_name', 'path'
        """
        img_path, label = self.samples[idx]
        
        try:
            # Cargar imagen
            image = Image.open(img_path).convert('RGB')
            
            # Extraer landmarks si está habilitado
            landmarks = None
            if self.extract_landmarks and self.hands is not None:
                landmarks = self._extract_landmarks(image)
            
            # Si no se extrajeron landmarks, usar ceros
            if landmarks is None:
                landmarks = np.zeros(126, dtype=np.float32)
            
            # Aplicar transformaciones
            if self.transform:
                image = self.transform(image)
            
            # Obtener nombre de clase
            class_name = self.data_config['class_names'][label]
            
            return {
                'image': image,
                'landmarks': torch.from_numpy(landmarks),
                'label': label,
                'class_name': class_name,
                'path': img_path
            }
        
        except Exception as e:
            print(f"Error cargando {img_path}: {e}")
            # Retornar sample dummy en caso de error
            dummy_image = torch.zeros(3, 224, 224)
            dummy_landmarks = torch.zeros(126)
            return {
                'image': dummy_image,
                'landmarks': dummy_landmarks,
                'label': label,
                'class_name': self.data_config['class_names'][label],
                'path': img_path
            }
    
    def _extract_landmarks(self, image: Image.Image) -> Optional[np.ndarray]:
        """Extrae landmarks de la imagen usando MediaPipe."""
        try:
            # Convertir PIL a numpy
            img_np = np.array(image)
            
            # Procesar con MediaPipe
            results = self.hands.process(img_np)
            
            if results.multi_hand_landmarks:
                # Extraer landmarks de todas las manos detectadas
                all_landmarks = []
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = []
                    for landmark in hand_landmarks.landmark:
                        landmarks.extend([landmark.x, landmark.y, landmark.z])
                    all_landmarks.extend(landmarks)
                
                # Padding si solo hay una mano (63 valores)
                if len(all_landmarks) == 63:
                    all_landmarks.extend([0.0] * 63)  # Agregar mano vacía
                
                return np.array(all_landmarks[:126], dtype=np.float32)
            else:
                # No se detectaron manos
                return np.zeros(126, dtype=np.float32)
        
        except Exception as e:
            # Error al procesar
            return np.zeros(126, dtype=np.float32)


class UniversalVideoDataset(Dataset):
    """Dataset universal para videos/secuencias."""
    
    def __init__(
        self,
        data_config: Dict,
        split: str = 'train',
        num_frames: int = 30,
        transform: Optional[transforms.Compose] = None,
        split_ratios: Dict = None
    ):
        self.data_config = data_config
        self.split = split
        self.num_frames = num_frames
        self.transform = transform
        
        if split_ratios is None:
            split_ratios = {'train': 0.7, 'val': 0.15, 'test': 0.15}
        
        self.samples = self._build_samples_with_split(split_ratios)
        self.class_to_idx = data_config['class_to_idx']
        
        print(f"{split.capitalize()}: {len(self.samples)} videos")
    
    def _build_samples_with_split(self, split_ratios: Dict) -> List[Tuple[str, int]]:
        """Construye lista de samples con split estratificado."""
        all_samples_by_class = {}
        
        for class_data in self.data_config['data_paths']:
            class_path = Path(class_data['path'])
            class_idx = class_data['class_idx']
            
            samples = []
            for file_name in class_data['files']:
                file_path = class_path / file_name
                ext = file_path.suffix.lower()
                if file_path.exists() and ext in ['.mp4', '.avi', '.mov', '.mkv']:
                    samples.append((str(file_path), class_idx))
            
            if samples:
                all_samples_by_class[class_idx] = samples
        
        # Split estratificado
        split_samples = []
        for class_idx, class_samples in all_samples_by_class.items():
            random.seed(42)
            random.shuffle(class_samples)
            
            n_samples = len(class_samples)
            n_train = int(n_samples * split_ratios['train'])
            n_val = int(n_samples * split_ratios['val'])
            
            if n_samples >= 3:
                n_train = max(1, n_train)
                n_val = max(1, n_val)
            elif n_samples == 2:
                n_train = 1
                n_val = 0
            else:
                n_train = 1
                n_val = 0
            
            if self.split == 'train':
                split_samples.extend(class_samples[:n_train])
            elif self.split == 'val':
                split_samples.extend(class_samples[n_train:n_train + n_val])
            else:
                split_samples.extend(class_samples[n_train + n_val:])
        
        random.shuffle(split_samples)
        return split_samples
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Dict:
        video_path, label = self.samples[idx]
        
        try:
            # Cargar video
            frames = self._load_video(video_path)
            
            # Aplicar transformaciones
            if self.transform:
                frames = torch.stack([
                    self.transform(Image.fromarray(f)) for f in frames
                ])
            else:
                # Convertir a tensor si no hay transform
                frames = torch.from_numpy(
                    np.array(frames).transpose(0, 3, 1, 2)
                ).float() / 255.0
            
            class_name = self.data_config['class_names'][label]
            
            return {
                'frames': frames,
                'label': label,
                'class_name': class_name,
                'path': video_path
            }
        
        except Exception as e:
            print(f"Error cargando video {video_path}: {e}")
            # Retornar frames dummy
            dummy_frames = torch.zeros(self.num_frames, 3, 224, 224)
            return {
                'frames': dummy_frames,
                'label': label,
                'class_name': self.data_config['class_names'][label],
                'path': video_path
            }
    
    def _load_video(self, video_path: str) -> List[np.ndarray]:
        """Carga video y samplea frames uniformemente."""
        cap = cv2.VideoCapture(video_path)
        frames = []
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames == 0:
            cap.release()
            # Retornar frames vacíos
            return [np.zeros((224, 224, 3), dtype=np.uint8) for _ in range(self.num_frames)]
        
        # Samplear frames uniformemente
        indices = np.linspace(0, total_frames - 1, self.num_frames, dtype=int)
        
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (224, 224))
                frames.append(frame)
        
        cap.release()
        
        # Padding si no hay suficientes frames
        while len(frames) < self.num_frames:
            frames.append(frames[-1] if frames else np.zeros((224, 224, 3), dtype=np.uint8))
        
        return frames[:self.num_frames]


def create_data_loaders(
    config_path: str,
    batch_size: int = 32,
    num_workers: int = 4,
    extract_landmarks: bool = True
) -> Dict[str, DataLoader]:
    """
    Crea data loaders automáticamente desde la configuración.
    
    Args:
        config_path: Ruta a data_loaders_config.yaml
        batch_size: Tamaño del batch
        num_workers: Número de workers
        extract_landmarks: Si extraer landmarks
    
    Returns:
        Dict con data loaders: {'train': ..., 'val': ..., 'test': ...}
    """
    # Cargar configuración
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Transformaciones
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Crear datasets según el tipo
    dataset_type = config['dataset_type']
    
    print(f"\nCreando data loaders ({dataset_type})...")
    
    if dataset_type == 'image':
        datasets = {
            'train': UniversalImageDataset(
                config, split='train', 
                transform=train_transform, 
                extract_landmarks=extract_landmarks
            ),
            'val': UniversalImageDataset(
                config, split='val', 
                transform=val_transform, 
                extract_landmarks=extract_landmarks
            ),
            'test': UniversalImageDataset(
                config, split='test', 
                transform=val_transform, 
                extract_landmarks=extract_landmarks
            )
        }
    elif dataset_type == 'video':
        datasets = {
            'train': UniversalVideoDataset(
                config, split='train', 
                transform=train_transform
            ),
            'val': UniversalVideoDataset(
                config, split='val', 
                transform=val_transform
            ),
            'test': UniversalVideoDataset(
                config, split='test', 
                transform=val_transform
            )
        }
    else:
        raise ValueError(f"Dataset type '{dataset_type}' no soportado")
    
    # Crear data loaders
    loaders = {}
    for split, dataset in datasets.items():
        loaders[split] = DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=(split == 'train'),
            num_workers=num_workers,
            pin_memory=torch.cuda.is_available(),
            drop_last=(split == 'train')  # Drop last batch in training
        )
    
    return loaders