"""
Módulo de gestión del historial de exámenes generados.
Permite guardar, cargar y buscar exámenes previamente creados.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class HistoryManager:
    """Gestiona el historial de exámenes generados."""
    
    def __init__(self, history_path: str = "output/history.json"):
        self.history_path = Path(history_path)
        self.history: List[Dict[str, Any]] = []
        self.load_history()
    
    def load_history(self) -> None:
        """Carga el historial desde el archivo JSON."""
        if self.history_path.exists():
            try:
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Error cargando historial: {str(e)}")
                self.history = []
        else:
            self.history = []
    
    def save_history(self) -> None:
        """Guarda el historial en el archivo JSON."""
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.history_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)
    
    def add_exam(self, exam_data: Dict[str, Any]) -> bool:
        """
        Agrega un examen al historial.
        
        Args:
            exam_data: Datos del examen generado
            
        Returns:
            True si se agregó correctamente
        """
        try:
            exam_record = {
                'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
                'timestamp': datetime.now().isoformat(),
                'topic': exam_data.get('metadata', {}).get('topic', 'Sin tema'),
                'content': exam_data.get('content', ''),
                'metadata': exam_data.get('metadata', {}),
                'success': exam_data.get('success', False)
            }
            
            self.history.insert(0, exam_record)  # Agregar al inicio
            self.save_history()
            return True
        except Exception as e:
            print(f"Error agregando examen al historial: {str(e)}")
            return False
    
    def get_all_exams(self) -> List[Dict[str, Any]]:
        """Obtiene todos los exámenes del historial."""
        return self.history
    
    def get_exam_by_id(self, exam_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un examen por su ID.
        
        Args:
            exam_id: ID del examen
            
        Returns:
            Datos del examen o None si no existe
        """
        for exam in self.history:
            if exam.get('id') == exam_id:
                return exam
        return None
    
    def search_exams(self, query: str) -> List[Dict[str, Any]]:
        """
        Busca exámenes por tema o contenido.
        
        Args:
            query: Término de búsqueda
            
        Returns:
            Lista de exámenes que coinciden con la búsqueda
        """
        query_lower = query.lower()
        results = []
        
        for exam in self.history:
            topic = exam.get('topic', '').lower()
            content = exam.get('content', '').lower()
            
            if query_lower in topic or query_lower in content:
                results.append(exam)
        
        return results
    
    def get_exams_by_date_range(self, 
                                start_date: datetime, 
                                end_date: datetime) -> List[Dict[str, Any]]:
        """
        Obtiene exámenes dentro de un rango de fechas.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha fin
            
        Returns:
            Lista de exámenes en el rango de fechas
        """
        results = []
        
        for exam in self.history:
            timestamp_str = exam.get('timestamp', '')
            try:
                exam_date = datetime.fromisoformat(timestamp_str)
                if start_date <= exam_date <= end_date:
                    results.append(exam)
            except (ValueError, TypeError):
                continue
        
        return results
    
    def get_exams_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Obtiene exámenes por tema (búsqueda parcial).
        
        Args:
            topic: Tema a buscar
            
        Returns:
            Lista de exámenes relacionados con el tema
        """
        topic_lower = topic.lower()
        results = []
        
        for exam in self.history:
            exam_topic = exam.get('topic', '').lower()
            if topic_lower in exam_topic or exam_topic in topic_lower:
                results.append(exam)
        
        return results
    
    def delete_exam(self, exam_id: str) -> bool:
        """
        Elimina un examen del historial.
        
        Args:
            exam_id: ID del examen a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        for i, exam in enumerate(self.history):
            if exam.get('id') == exam_id:
                del self.history[i]
                self.save_history()
                return True
        return False
    
    def clear_history(self) -> bool:
        """
        Limpia todo el historial.
        
        Returns:
            True si se limpió correctamente
        """
        self.history = []
        self.save_history()
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del historial.
        
        Returns:
            Diccionario con estadísticas
        """
        if not self.history:
            return {
                'total_exams': 0,
                'successful_exams': 0,
                'topics': [],
                'most_recent': None,
                'oldest': None
            }
        
        successful = sum(1 for exam in self.history if exam.get('success', False))
        topics = list(set(exam.get('topic', 'Sin tema') for exam in self.history))
        
        return {
            'total_exams': len(self.history),
            'successful_exams': successful,
            'failed_exams': len(self.history) - successful,
            'topics': topics,
            'unique_topics': len(topics),
            'most_recent': self.history[0].get('timestamp') if self.history else None,
            'oldest': self.history[-1].get('timestamp') if self.history else None
        }
    
    def export_exam_to_file(self, exam_id: str, output_path: str) -> bool:
        """
        Exporta un examen a un archivo de texto.
        
        Args:
            exam_id: ID del examen
            output_path: Ruta del archivo de salida
            
        Returns:
            True si se exportó correctamente
        """
        exam = self.get_exam_by_id(exam_id)
        if not exam:
            return False
        
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"EXAMEN GENERADO: {exam.get('topic', 'Sin tema')}\n")
                f.write(f"Fecha: {exam.get('timestamp', 'N/A')}\n")
                f.write(f"ID: {exam.get('id', 'N/A')}\n")
                f.write("=" * 80 + "\n\n")
                f.write(exam.get('content', ''))
            
            return True
        except Exception as e:
            print(f"Error exportando examen: {str(e)}")
            return False
    
    def get_recent_exams(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene los exámenes más recientes.
        
        Args:
            limit: Número máximo de exámenes a retornar
            
        Returns:
            Lista de exámenes recientes
        """
        return self.history[:limit]
