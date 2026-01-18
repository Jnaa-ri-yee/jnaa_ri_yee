# ======================================================                     *
#  Project      : deep                                                       *
#  File         : hybrid_trainer.py                                          *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 17:49                                           *
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
Trainer para modelo híbrido con versionado automático.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import numpy as np
from pathlib import Path
import json
from typing import Dict, List
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


class HybridTrainer:
    """Trainer automático para modelos híbridos."""
    
    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        test_loader: DataLoader,
        config: Dict,
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.config = config
        self.device = device
        
        # Configurar optimizador
        self.optimizer = self._setup_optimizer()
        
        # Configurar loss
        self.criterion = nn.CrossEntropyLoss()
        
        # Configurar scheduler
        self.scheduler = self._setup_scheduler()
        
        # Métricas
        self.history = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': [],
            'learning_rates': []
        }
        
        self.best_val_acc = 0.0
        self.epochs_without_improvement = 0
    
    def _setup_optimizer(self):
        """Configura el optimizador."""
        lr = self.config['training']['learning_rate']
        optimizer_name = self.config['training']['optimizer'].lower()
        
        if optimizer_name == 'adam':
            return optim.Adam(self.model.parameters(), lr=lr)
        elif optimizer_name == 'adamw':
            return optim.AdamW(self.model.parameters(), lr=lr, weight_decay=0.01)
        elif optimizer_name == 'sgd':
            return optim.SGD(self.model.parameters(), lr=lr, momentum=0.9)
        else:
            return optim.AdamW(self.model.parameters(), lr=lr)
    
    def _setup_scheduler(self):
        """Configura el scheduler de learning rate."""
        scheduler_name = self.config['training']['scheduler'].lower()
        epochs = self.config['training']['epochs']
        
        if scheduler_name == 'cosine_annealing':
            return optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=epochs
            )
        elif scheduler_name == 'step':
            return optim.lr_scheduler.StepLR(
                self.optimizer, step_size=10, gamma=0.1
            )
        else:
            return optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer, mode='max', factor=0.5, patience=5
            )
    
    def train(self) -> Dict:
        """Entrena el modelo."""
        epochs = self.config['training']['epochs']
        patience = self.config['training']['early_stopping']['patience']
        
        print(f"\nIniciando entrenamiento ({epochs} epochs)")
        print(f"Device: {self.device}")
        print(f"Clases: {self.config['dataset']['num_classes']}")
        print("-" * 60)
        
        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")
            
            # Entrenar
            train_loss, train_acc = self._train_epoch()
            
            # Validar
            val_loss, val_acc = self._validate_epoch()
            
            # Actualizar scheduler
            if isinstance(self.scheduler, optim.lr_scheduler.ReduceLROnPlateau):
                self.scheduler.step(val_acc)
            else:
                self.scheduler.step()
            
            # Guardar métricas
            current_lr = self.optimizer.param_groups[0]['lr']
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            self.history['learning_rates'].append(current_lr)
            
            # Imprimir progreso
            print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")
            print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")
            print(f"LR: {current_lr:.6f}")
            
            # Early stopping
            if val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                self.epochs_without_improvement = 0
                print("Nueva mejor validación!")
            else:
                self.epochs_without_improvement += 1
                if self.epochs_without_improvement >= patience:
                    print(f"\nEarly stopping (sin mejora en {patience} epochs)")
                    break
        
        # Evaluación final en test
        print("\n" + "="*60)
        print("Evaluación Final en Test Set")
        print("="*60)
        test_metrics = self._evaluate_test()
        
        return {
            'history': self.history,
            'best_val_acc': self.best_val_acc,
            'test_metrics': test_metrics
        }
    
    def _train_epoch(self) -> tuple:
        """Entrena una época."""
        self.model.train()
        total_loss = 0
        all_preds = []
        all_labels = []
        
        pbar = tqdm(self.train_loader, desc="Training")
        for batch in pbar:
            images = batch['image'].to(self.device)
            labels = batch['label'].to(self.device)
            landmarks = batch.get('landmarks')
            
            if landmarks is not None:
                landmarks = landmarks.to(self.device)
            
            # Forward
            self.optimizer.zero_grad()
            outputs = self.model(images, landmarks)
            loss = self.criterion(outputs, labels)
            
            # Backward
            loss.backward()
            self.optimizer.step()
            
            # Métricas
            total_loss += loss.item()
            preds = outputs.argmax(dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
            # Actualizar progress bar
            pbar.set_postfix({'loss': loss.item()})
        
        avg_loss = total_loss / len(self.train_loader)
        accuracy = accuracy_score(all_labels, all_preds)
        
        return avg_loss, accuracy
    
    def _validate_epoch(self) -> tuple:
        """Valida una época."""
        self.model.eval()
        total_loss = 0
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for batch in tqdm(self.val_loader, desc="Validation"):
                images = batch['image'].to(self.device)
                labels = batch['label'].to(self.device)
                landmarks = batch.get('landmarks')
                
                if landmarks is not None:
                    landmarks = landmarks.to(self.device)
                
                outputs = self.model(images, landmarks)
                loss = self.criterion(outputs, labels)
                
                total_loss += loss.item()
                preds = outputs.argmax(dim=1)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        avg_loss = total_loss / len(self.val_loader)
        accuracy = accuracy_score(all_labels, all_preds)
        
        return avg_loss, accuracy
    
    def _evaluate_test(self) -> Dict:
        """Evaluación completa en test set."""
        self.model.eval()
        all_preds = []
        all_labels = []
        all_probs = []
        
        with torch.no_grad():
            for batch in tqdm(self.test_loader, desc="Testing"):
                images = batch['image'].to(self.device)
                labels = batch['label'].to(self.device)
                landmarks = batch.get('landmarks')
                
                if landmarks is not None:
                    landmarks = landmarks.to(self.device)
                
                outputs = self.model(images, landmarks)
                probs = torch.softmax(outputs, dim=1)
                preds = outputs.argmax(dim=1)
                
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                all_probs.extend(probs.cpu().numpy())
        
        # Calcular métricas
        accuracy = accuracy_score(all_labels, all_preds)
        precision, recall, f1, _ = precision_recall_fscore_support(
            all_labels, all_preds, average='weighted', zero_division=0
        )
        
        # Matriz de confusión
        cm = confusion_matrix(all_labels, all_preds)
        
        metrics = {
            'test_accuracy': float(accuracy),
            'test_precision': float(precision),
            'test_recall': float(recall),
            'test_f1': float(f1),
            'confusion_matrix': cm.tolist(),
            'predictions': all_preds,
            'labels': all_labels,
            'probabilities': all_probs
        }
        
        print(f"\nTest Accuracy: {accuracy:.4f}")
        print(f"Test Precision: {precision:.4f}")
        print(f"Test Recall: {recall:.4f}")
        print(f"Test F1-Score: {f1:.4f}")
        
        return metrics
    
    def save_model(self, save_path: str):
        """Guarda el modelo."""
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'config': self.config,
            'history': self.history,
            'best_val_acc': self.best_val_acc
        }, save_path)
        
        print(f"Modelo guardado en: {save_path}")
    
    def plot_training_history(self, save_dir: str):
        """Genera gráficas del entrenamiento."""
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Loss
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 2, 1)
        plt.plot(self.history['train_loss'], label='Train Loss')
        plt.plot(self.history['val_loss'], label='Val Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.title('Training and Validation Loss')
        plt.grid(True)
        
        # Accuracy
        plt.subplot(1, 2, 2)
        plt.plot(self.history['train_acc'], label='Train Acc')
        plt.plot(self.history['val_acc'], label='Val Acc')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.title('Training and Validation Accuracy')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_dir / 'training_curves.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Gráficas guardadas en: {save_dir / 'training_curves.png'}")
    
    def plot_confusion_matrix(self, cm: np.ndarray, class_names: List[str], save_dir: str):
        """Genera matriz de confusión."""
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names,
            yticklabels=class_names
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(save_dir / 'confusion_matrix.png', dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Matriz de confusión guardada en: {save_dir / 'confusion_matrix.png'}")
