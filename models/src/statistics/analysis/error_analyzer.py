"""
Analizador automático de errores del modelo.
Proporciona insights sobre qué clases son difíciles y por qué.
"""

import numpy as np
from typing import Dict, List, Tuple
from collections import defaultdict, Counter


class ErrorAnalyzer:
    """
    Analiza errores del modelo para encontrar patrones y dar recomendaciones.
    """
    
    def __init__(
        self,
        predictions: List[int],
        labels: List[int],
        class_names: List[str],
        probabilities: List = None
    ):
        """
        Args:
            predictions: Lista de predicciones del modelo
            labels: Lista de etiquetas verdaderas
            class_names: Lista de nombres de clases
            probabilities: Lista opcional de probabilidades por clase
        """
        self.predictions = np.array(predictions)
        self.labels = np.array(labels)
        self.class_names = class_names
        self.probabilities = np.array(probabilities) if probabilities is not None else None
        
        # Identificar errores
        self.errors = self.predictions != self.labels
        self.error_indices = np.where(self.errors)[0]
        self.correct_indices = np.where(~self.errors)[0]
    
    def analyze(self) -> Dict:
        """
        Análisis completo de errores.
        
        Returns:
            Dict con diferentes análisis de errores
        """
        analysis = {
            'summary': self._get_summary(),
            'errors_per_class': self._errors_per_class(),
            'confusion_pairs': self._confusion_pairs(top_k=10),
            'hardest_classes': self._hardest_classes(top_k=5),
            'easiest_classes': self._easiest_classes(top_k=5),
            'confidence_analysis': self._confidence_analysis() if self.probabilities is not None else None
        }
        
        return analysis
    
    def _get_summary(self) -> Dict:
        """Resumen general de errores."""
        total_samples = len(self.labels)
        total_errors = int(self.errors.sum())
        
        return {
            'total_samples': total_samples,
            'total_errors': total_errors,
            'total_correct': total_samples - total_errors,
            'error_rate': float(self.errors.mean()),
            'accuracy': float(1 - self.errors.mean())
        }
    
    def _errors_per_class(self) -> Dict:
        """Cuenta errores por cada clase."""
        errors_per_class = {}
        
        for class_idx, class_name in enumerate(self.class_names):
            # Muestras de esta clase
            class_mask = self.labels == class_idx
            class_total = class_mask.sum()
            
            if class_total > 0:
                # Errores en esta clase
                class_errors = (self.errors & class_mask).sum()
                error_rate = class_errors / class_total
                
                errors_per_class[class_name] = {
                    'total_samples': int(class_total),
                    'errors': int(class_errors),
                    'correct': int(class_total - class_errors),
                    'error_rate': float(error_rate),
                    'accuracy': float(1 - error_rate)
                }
        
        return errors_per_class
    
    def _confusion_pairs(self, top_k: int = 10) -> List[Dict]:
        """
        Encuentra pares de clases que más se confunden.
        
        Args:
            top_k: Número de pares a retornar
        
        Returns:
            Lista de pares (clase_real, clase_predicha) y su frecuencia
        """
        confusion_counts = defaultdict(int)
        
        for idx in self.error_indices:
            true_label = self.labels[idx]
            pred_label = self.predictions[idx]
            
            pair = (int(true_label), int(pred_label))
            confusion_counts[pair] += 1
        
        # Ordenar por frecuencia
        sorted_pairs = sorted(
            confusion_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        result = []
        for (true_idx, pred_idx), count in sorted_pairs:
            result.append({
                'true_class': self.class_names[true_idx],
                'true_idx': true_idx,
                'predicted_class': self.class_names[pred_idx],
                'predicted_idx': pred_idx,
                'count': int(count),
                'percentage': float(count / len(self.error_indices) * 100) if len(self.error_indices) > 0 else 0.0
            })
        
        return result
    
    def _hardest_classes(self, top_k: int = 5) -> List[Dict]:
        """Clases con mayor tasa de error."""
        errors_per_class = self._errors_per_class()
        
        sorted_classes = sorted(
            errors_per_class.items(),
            key=lambda x: x[1]['error_rate'],
            reverse=True
        )[:top_k]
        
        return [
            {
                'class_name': name,
                'class_idx': self.class_names.index(name),
                'error_rate': data['error_rate'],
                'accuracy': data['accuracy'],
                'total_samples': data['total_samples'],
                'errors': data['errors']
            }
            for name, data in sorted_classes
        ]
    
    def _easiest_classes(self, top_k: int = 5) -> List[Dict]:
        """Clases con menor tasa de error."""
        errors_per_class = self._errors_per_class()
        
        sorted_classes = sorted(
            errors_per_class.items(),
            key=lambda x: x[1]['error_rate']
        )[:top_k]
        
        return [
            {
                'class_name': name,
                'class_idx': self.class_names.index(name),
                'error_rate': data['error_rate'],
                'accuracy': data['accuracy'],
                'total_samples': data['total_samples'],
                'errors': data['errors']
            }
            for name, data in sorted_classes
        ]
    
    def _confidence_analysis(self) -> Dict:
        """Analiza la confianza del modelo en predicciones correctas vs incorrectas."""
        if self.probabilities is None:
            return None
        
        # Probabilidades de la clase predicha
        pred_probs = np.max(self.probabilities, axis=1)
        
        # Separar por correctas e incorrectas
        correct_probs = pred_probs[self.correct_indices]
        error_probs = pred_probs[self.error_indices]
        
        return {
            'correct_predictions': {
                'mean_confidence': float(np.mean(correct_probs)) if len(correct_probs) > 0 else 0.0,
                'std_confidence': float(np.std(correct_probs)) if len(correct_probs) > 0 else 0.0,
                'min_confidence': float(np.min(correct_probs)) if len(correct_probs) > 0 else 0.0,
                'max_confidence': float(np.max(correct_probs)) if len(correct_probs) > 0 else 0.0
            },
            'incorrect_predictions': {
                'mean_confidence': float(np.mean(error_probs)) if len(error_probs) > 0 else 0.0,
                'std_confidence': float(np.std(error_probs)) if len(error_probs) > 0 else 0.0,
                'min_confidence': float(np.min(error_probs)) if len(error_probs) > 0 else 0.0,
                'max_confidence': float(np.max(error_probs)) if len(error_probs) > 0 else 0.0
            }
        }
    
    def get_recommendations(self) -> List[str]:
        """
        Genera recomendaciones basadas en el análisis de errores.
        
        Returns:
            Lista de recomendaciones textuales
        """
        recommendations = []
        analysis = self.analyze()
        
        # 1. Análisis de clases difíciles
        hardest = analysis['hardest_classes']
        if hardest and hardest[0]['error_rate'] > 0.3:
            rec = (
                f"La clase '{hardest[0]['class_name']}' tiene alta tasa de error "
                f"({hardest[0]['error_rate']:.1%}). "
                f"Recomendaciones:\n"
                f"   • Agregar más datos de entrenamiento para esta clase\n"
                f"   • Revisar calidad de las imágenes\n"
                f"   • Usar augmentación más agresiva"
            )
            recommendations.append(rec)
        
        # 2. Análisis de confusiones
        confusion_pairs = analysis['confusion_pairs']
        if confusion_pairs and confusion_pairs[0]['count'] > 3:
            pair = confusion_pairs[0]
            rec = (
                f"El modelo confunde frecuentemente '{pair['true_class']}' "
                f"con '{pair['predicted_class']}' ({pair['count']} veces).\n"
                f"   Estas clases pueden ser visualmente similares.\n"
                f"   Considera agregar features que las distingan mejor."
            )
            recommendations.append(rec)
        
        # 3. Análisis de confianza
        if analysis['confidence_analysis']:
            conf_analysis = analysis['confidence_analysis']
            error_conf = conf_analysis['incorrect_predictions']['mean_confidence']
            
            if error_conf > 0.7:
                rec = (
                    f"El modelo está muy confiado en sus errores "
                    f"(confianza promedio: {error_conf:.1%}).\n"
                    f"   Esto sugiere sobreajuste. Considera:\n"
                    f"   • Aumentar dropout\n"
                    f"   • Usar regularización L2\n"
                    f"   • Reducir complejidad del modelo"
                )
                recommendations.append(rec)
        
        # 4. Tasa de error general
        error_rate = analysis['summary']['error_rate']
        if error_rate > 0.2:
            rec = (
                f"Tasa de error alta ({error_rate:.1%}). "
                f"Sugerencias generales:\n"
                f"   • Aumentar epochs de entrenamiento\n"
                f"   • Ajustar learning rate (probar valores más bajos)\n"
                f"   • Usar un backbone más potente (ej: ResNet34 en lugar de ResNet18)\n"
                f"   • Verificar que landmarks se estén extrayendo correctamente"
            )
            recommendations.append(rec)
        elif error_rate < 0.05:
            rec = (
                f"Excelente rendimiento ({error_rate:.1%} de error)!\n"
                f"   Considera ajustes finos:\n"
                f"   • Optimizar hiperparámetros con búsqueda bayesiana\n"
                f"   • Experimentar con ensemble de modelos\n"
                f"   • Aplicar técnicas de regularización avanzadas"
            )
            recommendations.append(rec)
        
        # 5. Desbalance de clases
        errors_per_class = analysis['errors_per_class']
        error_rates = [data['error_rate'] for data in errors_per_class.values()]
        
        if len(error_rates) > 0:
            error_std = np.std(error_rates)
            if error_std > 0.2:
                rec = (
                    f"Hay gran variación en el rendimiento entre clases "
                    f"(std: {error_std:.2f}).\n"
                    f"   Esto puede indicar desbalance de datos.\n"
                    f"   Considera usar class weights o SMOTE para balancear."
                )
                recommendations.append(rec)
        
        # Si no hay problemas graves
        if not recommendations:
            recommendations.append(
                "El modelo tiene buen rendimiento general sin problemas críticos detectados."
            )
        
        return recommendations
    
    def print_summary(self):
        """Imprime un resumen legible del análisis."""
        analysis = self.analyze()
        
        print("\n" + "="*70)
        print("ANÁLISIS DE ERRORES")
        print("="*70)
        
        # Resumen general
        summary = analysis['summary']
        print(f"\nResumen General:")
        print(f"  • Total de muestras: {summary['total_samples']}")
        print(f"  • Correctas: {summary['total_correct']} ({summary['accuracy']:.2%})")
        print(f"  • Errores: {summary['total_errors']} ({summary['error_rate']:.2%})")
        
        # Clases difíciles
        print(f"\nTop 3 Clases Más Difíciles:")
        for i, cls in enumerate(analysis['hardest_classes'][:3], 1):
            print(f"  {i}. {cls['class_name']:20s} - Accuracy: {cls['accuracy']:.2%} "
                  f"({cls['errors']}/{cls['total_samples']} errores)")
        
        # Clases fáciles
        print(f"\nTop 3 Clases Más Fáciles:")
        for i, cls in enumerate(analysis['easiest_classes'][:3], 1):
            print(f"  {i}. {cls['class_name']:20s} - Accuracy: {cls['accuracy']:.2%} "
                  f"({cls['errors']}/{cls['total_samples']} errores)")
        
        # Confusiones principales
        print(f"\nTop 5 Confusiones:")
        for i, pair in enumerate(analysis['confusion_pairs'][:5], 1):
            print(f"  {i}. '{pair['true_class']}' → '{pair['predicted_class']}': "
                  f"{pair['count']} veces ({pair['percentage']:.1f}%)")
        
        # Recomendaciones
        print(f"\nRecomendaciones:")
        for i, rec in enumerate(self.get_recommendations(), 1):
            print(f"\n{i}. {rec}")
        
        print("\n" + "="*70 + "\n")