"""
Módulo de generación de exámenes utilizando IA (Ollama).
Genera preguntas y exámenes basados en temas y fuentes proporcionadas.
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import ollama


class ExamGenerator:
    """Genera exámenes utilizando modelos de IA locales a través de Ollama."""
    
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama2"):
        self.host = host
        self.model = model
        self.client = ollama.Client(host=host)
    
    def set_model(self, model: str) -> None:
        """Cambia el modelo a utilizar."""
        self.model = model
    
    def get_available_models(self) -> List[str]:
        """Obtiene la lista de modelos disponibles en Ollama."""
        try:
            response = self.client.list()
            models = response.get('models', [])
            return [model['name'] for model in models]
        except Exception as e:
            print(f"Error obteniendo modelos: {str(e)}")
            return []
    
    def check_connection(self) -> bool:
        """Verifica la conexión con Ollama."""
        try:
            self.client.list()
            return True
        except Exception:
            return False
    
    def generate_exam_prompt(self, 
                            topic: str,
                            num_questions: int = 10,
                            question_types: List[str] = None,
                            difficulty: str = "medio",
                            duration_minutes: int = 90,
                            include_answers: bool = True,
                            language: str = "español") -> str:
        """
        Construye el prompt para generar un examen.
        
        Args:
            topic: Tema del examen
            num_questions: Número de preguntas
            question_types: Tipos de preguntas (opcional)
            difficulty: Nivel de dificultad
            duration_minutes: Duración del examen en minutos
            include_answers: Si se incluye hoja de respuestas
            language: Idioma del examen
            
        Returns:
            Prompt formateado para la IA
        """
        if question_types is None:
            question_types = ["selección múltiple", "desarrollo", "verdadero/falso"]
        
        prompt = f"""Eres un profesor universitario experto en creación de exámenes. 
Tu tarea es crear un examen académico profesional sobre el siguiente tema:

TEMA: {topic}

REQUISITOS DEL EXAMEN:
- Número de preguntas: {num_questions}
- Tipos de preguntas: {', '.join(question_types)}
- Nivel de dificultad: {difficulty}
- Duración estimada: {duration_minutes} minutos
- Idioma: {language}
- Incluir hoja de respuestas: {"Sí" if include_answers else "No"}

INSTRUCCIONES ESPECÍFICAS:
1. Las preguntas deben ser claras, precisas y académicamente rigurosas
2. Distribuye los diferentes tipos de preguntas de manera equilibrada
3. Asegúrate de que las preguntas evalúen comprensión, no solo memorización
4. Para preguntas de selección múltiple, incluye 4 opciones (a, b, c, d)
5. Incluye instrucciones claras al inicio del examen
6. Asigna puntaje a cada pregunta o sección
7. Organiza el examen en secciones lógicas

FORMATO DE SALIDA:
Por favor, genera el examen con el siguiente formato:

=== EXAMEN: {topic.upper()} ===

INSTRUCCIONES GENERALES:
[Instrucciones para el estudiante]

SECCIÓN 1: [Tipo de pregunta]
[Pregunta 1]
[Pregunta 2]
...

SECCIÓN 2: [Tipo de pregunta]
...

{"=== HOJA DE RESPUESTAS ===\n[Respuestas correctas y criterios de evaluación]" if include_answers else ""}

IMPORTANTE: Genera el contenido completo del examen listo para usar."""

        return prompt
    
    def generate_exam_with_sources(self,
                                   topic: str,
                                   sources_content: str,
                                   num_questions: int = 10,
                                   question_types: List[str] = None,
                                   difficulty: str = "medio",
                                   duration_minutes: int = 90,
                                   include_answers: bool = True,
                                   language: str = "español") -> str:
        """
        Genera un examen basado en fuentes específicas.
        
        Args:
            topic: Tema del examen
            sources_content: Contenido de las fuentes de referencia
            num_questions: Número de preguntas
            question_types: Tipos de preguntas
            difficulty: Nivel de dificultad
            duration_minutes: Duración del examen
            include_answers: Si se incluye hoja de respuestas
            language: Idioma del examen
            
        Returns:
            Examen generado por la IA
        """
        prompt = f"""Eres un profesor universitario experto en creación de exámenes. 
Tu tarea es crear un examen académico profesional basándote ÚNICAMENTE en las fuentes proporcionadas.

TEMA GENERAL: {topic}

FUENTES DE REFERENCIA:
{sources_content}

REQUISITOS DEL EXAMEN:
- Número de preguntas: {num_questions}
- Tipos de preguntas: {', '.join(question_types if question_types else ["selección múltiple", "desarrollo", "verdadero/falso"])}
- Nivel de dificultad: {difficulty}
- Duración estimada: {duration_minutes} minutos
- Idioma: {language}
- Incluir hoja de respuestas: {"Sí" if include_answers else "No"}

INSTRUCCIONES CRÍTICAS:
1. LAS PREGUNTAS DEBEN BASARSE ÚNICAMENTE EN LA INFORMACIÓN DE LAS FUENTES PROPORCIONADAS
2. No inventes información que no esté en las fuentes
3. Cita implícitamente los conceptos clave de las fuentes
4. Las preguntas deben evaluar la comprensión del material de las fuentes
5. Mantén el rigor académico y la claridad

FORMATO DE SALIDA:
Genera el examen con el siguiente formato:

=== EXAMEN: {topic.upper()} ===

INSTRUCCIONES GENERALES:
[Instrucciones para el estudiante]

[Contenido del examen con preguntas organizadas por secciones]

{"=== HOJA DE RESPUESTAS ===\n[Respuestas correctas con justificación basada en las fuentes]" if include_answers else ""}

IMPORTANTE: Todo el contenido debe derivarse exclusivamente de las fuentes proporcionadas."""

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False
            )
            return response.get('response', '')
        except Exception as e:
            return f"Error generando examen: {str(e)}"
    
    def generate_exam(self,
                     topic: str,
                     sources_content: str = None,
                     num_questions: int = 10,
                     question_types: List[str] = None,
                     difficulty: str = "medio",
                     duration_minutes: int = 90,
                     include_answers: bool = True,
                     language: str = "español") -> Dict[str, Any]:
        """
        Genera un examen completo con metadatos.
        
        Args:
            topic: Tema del examen
            sources_content: Contenido de fuentes (opcional)
            num_questions: Número de preguntas
            question_types: Tipos de preguntas
            difficulty: Nivel de dificultad
            duration_minutes: Duración del examen
            include_answers: Si se incluye hoja de respuestas
            language: Idioma del examen
            
        Returns:
            Diccionario con el examen y metadatos
        """
        start_time = datetime.now()
        
        # Verificar conexión
        if not self.check_connection():
            return {
                'success': False,
                'error': 'No se pudo conectar con Ollama. Asegúrate de que esté ejecutándose.',
                'content': '',
                'metadata': {}
            }
        
        # Generar prompt apropiado
        if sources_content and sources_content.strip():
            exam_content = self.generate_exam_with_sources(
                topic=topic,
                sources_content=sources_content,
                num_questions=num_questions,
                question_types=question_types,
                difficulty=difficulty,
                duration_minutes=duration_minutes,
                include_answers=include_answers,
                language=language
            )
        else:
            prompt = self.generate_exam_prompt(
                topic=topic,
                num_questions=num_questions,
                question_types=question_types,
                difficulty=difficulty,
                duration_minutes=duration_minutes,
                include_answers=include_answers,
                language=language
            )
            
            try:
                response = self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    stream=False
                )
                exam_content = response.get('response', '')
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Error generando examen: {str(e)}',
                    'content': '',
                    'metadata': {}
                }
        
        end_time = datetime.now()
        generation_time = (end_time - start_time).total_seconds()
        
        return {
            'success': True,
            'content': exam_content,
            'metadata': {
                'topic': topic,
                'num_questions': num_questions,
                'question_types': question_types or [],
                'difficulty': difficulty,
                'duration_minutes': duration_minutes,
                'include_answers': include_answers,
                'language': language,
                'model_used': self.model,
                'generation_time_seconds': generation_time,
                'generated_at': start_time.isoformat(),
                'has_sources': bool(sources_content and sources_content.strip())
            }
        }
    
    def refine_exam(self, 
                   exam_content: str,
                   refinement_request: str) -> str:
        """
        Refina o modifica un examen existente según una solicitud.
        
        Args:
            exam_content: Contenido del examen actual
            refinement_request: Solicitud de refinamiento
            
        Returns:
            Examen refinado
        """
        prompt = f"""Tienes el siguiente examen:

{exam_content}

Por favor, realiza las siguientes modificaciones o mejoras:

{refinement_request}

Proporciona el examen completo con las modificaciones aplicadas."""

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False
            )
            return response.get('response', '')
        except Exception as e:
            return f"Error refinando examen: {str(e)}"
    
    def generate_question_variants(self,
                                  question: str,
                                  num_variants: int = 3) -> List[str]:
        """
        Genera variantes de una pregunta dada.
        
        Args:
            question: Pregunta original
            num_variants: Número de variantes a generar
            
        Returns:
            Lista de variantes de la pregunta
        """
        prompt = f"""Dada la siguiente pregunta de examen:

"{question}"

Genera {num_variants} variantes de esta pregunta que:
1. Evalúen el mismo concepto o habilidad
2. Tengan diferente redacción o contexto
3. Mantengan el mismo nivel de dificultad
4. Sean igualmente válidas académicamente

Proporciona solo las variantes numeradas, sin explicaciones adicionales."""

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False
            )
            content = response.get('response', '')
            # Separar las variantes
            variants = [v.strip() for v in content.split('\n') if v.strip() and not v.startswith('===')]
            return variants
        except Exception as e:
            return [f"Error generando variantes: {str(e)}"]
