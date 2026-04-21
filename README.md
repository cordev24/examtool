# Sistema de Generación de Exámenes con IA

Sistema de escritorio para docentes universitarios que permite generar exámenes escritos utilizando modelos de IA locales (Ollama), respetando las plantillas institucionales.

## Características Principales

1. **Configuración de Plantillas**: Gestión de plantillas de documentos universitarios
2. **Generador de Exámenes**: Creación de exámenes basados en temas y fuentes específicas
3. **Gestión de Fuentes**: Adjuntar archivos PDF, DOCX y enlaces web como referencia
4. **Historial**: Registro de exámenes generados anteriormente
5. **Vista Previa**: Visualización del contenido antes de exportar

## Requisitos

- Python 3.8+
- Ollama instalado y configurado localmente
- Modelos de IA descargados en Ollama (ej: llama2, mistral, etc.)

## Instalación

```bash
pip install ollama requests ttkbootstrap python-docx PyPDF2
```

## Uso

Ejecutar la aplicación principal:

```bash
python main.py
```

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación
- `config/`: Configuraciones y plantillas
- `modules/`: Módulos del sistema
  - `config_manager.py`: Gestión de configuración y plantillas
  - `exam_generator.py`: Generación de exámenes con IA
  - `file_handler.py`: Manejo de archivos y fuentes
  - `history_manager.py`: Historial de exámenes
- `templates/`: Plantillas de documentos
- `output/`: Exámenes generados

## Requisitos Previos

1. Instalar Ollama desde https://ollama.ai
2. Descargar un modelo: `ollama pull llama2` o `ollama pull mistral`
3. Asegurar que Ollama esté corriendo: `ollama serve`
