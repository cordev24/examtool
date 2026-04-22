# Sistema de Generación de Exámenes con IA

Sistema de escritorio para docentes universitarios que permite generar exámenes escritos utilizando modelos de IA locales (Ollama), respetando las plantillas institucionales.

## Características Principales

1. **Configuración de Plantillas**: Gestión de plantillas de documentos universitarios
2. **Generador de Exámenes**: Creación de exámenes basados en temas y fuentes específicas
3. **Gestión de Fuentes**: Adjuntar archivos PDF, DOCX y enlaces web como referencia
4. **Historial**: Registro de exámenes generados anteriormente
5. **Vista Previa**: Visualización del contenido antes de exportar
6. **Exportación Flexible**: Exportar a Word (.docx) o texto (.txt) con formato institucional

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) gestor de paquetes moderno
- Ollama instalado y configurado localmente
- Modelos de IA descargados en Ollama (ej: llama2, mistral, etc.)

## Instalación Rápida con uv

### 1. Instalar uv (si no lo tienes)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clonar y configurar el proyecto

```bash
cd exam-generator-ia
uv sync
```

### 3. Configurar Ollama

```bash
# Instalar Ollama (Linux/Mac)
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar un modelo
ollama pull llama2
# o alternativamente
ollama pull mistral
```

## Uso

### En Linux / macOS

#### Opción 1: Usando el script de inicio (recomendado)

```bash
./run.sh
```

Este script:
- Verifica que uv esté instalado
- Verifica que Ollama esté instalado y corriendo
- Instala/sincroniza dependencias automáticamente
- Inicia la aplicación

#### Opción 2: Manual con uv

```bash
uv run python main.py
```

#### Opción 3: Como comando instalado

```bash
uv pip install -e .
exam-generator
```

### En Windows

#### Opción 1: Usando el script batch (recomendado)

Haz doble clic en `run.bat` o ejecuta desde CMD/PowerShell:

```cmd
run.bat
```

Este script:
- Verifica que uv esté instalado (incluye instrucciones si falta)
- Sincroniza el entorno virtual e instala dependencias
- Inicia la aplicación
- Muestra mensajes de error útiles

#### Opción 2: Manual con uv

```cmd
uv run python main.py
```

#### Instalar uv en Windows (si no lo tienes)

Ejecuta en PowerShell (como administrador):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

O descarga el ejecutable desde: https://github.com/astral-sh/uv/releases

## Estructura del Proyecto

```
exam-generator-ia/
├── main.py                 # Aplicación principal con UI moderna
├── run.sh                  # Script de inicio (Linux/Mac)
├── run.bat                 # Script de inicio (Windows)
├── pyproject.toml          # Configuración del proyecto (uv)
├── uv.lock                 # Lock file de dependencias
├── README.md               # Esta documentación
├── INSTALL.md              # Guía detallada de instalación
├── config/
│   ├── settings.json       # Configuración general
│   └── templates.json      # Plantillas de documentos
├── modules/
│   ├── config_manager.py   # Módulo 1: Gestión de configuración
│   ├── exam_generator.py   # Módulo 2: Generación de exámenes
│   ├── file_handler.py     # Manejo de archivos y URLs
│   ├── history_manager.py  # Módulo 3: Historial
│   └── export_manager.py   # Módulo 4: Exportación
├── templates/              # Plantillas personalizadas
└── output/                 # Exámenes generados
```

## Módulos del Sistema

### 1. Configuración (`config_manager.py`)
- Gestión de plantillas de documentos universitarios
- Configuración de Ollama (host, modelo, parámetros)
- Reglas de generación (número máximo de preguntas, idioma, duración)
- Personalización de encabezados y pies de página

### 2. Generador de Exámenes (`exam_generator.py`)
- Interfaz para solicitar exámenes por tema
- Tipos de preguntas: selección múltiple, desarrollo, verdadero/falso
- Niveles de dificultad configurables
- La IA se basa ÚNICAMENTE en las fuentes proporcionadas

### 3. Manejo de Fuentes (`file_handler.py`)
- Lectura de archivos: PDF, DOCX, TXT, MD
- Extracción de contenido de URLs
- Múltiples fuentes simultáneas
- Límite de tamaño configurable

### 4. Historial (`history_manager.py`)
- Búsqueda y filtrado de exámenes anteriores
- Estadísticas de uso
- Reutilización de exámenes previos

### 5. Exportación (`export_manager.py`)
- Exportación a Word (.docx) con plantillas institucionales
- Exportación a texto plano (.txt)
- Formato personalizado según configuración

## Requisitos Previos

1. **Instalar uv** (gestor de paquetes):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```

2. **Instalar Ollama** desde https://ollama.ai

3. **Descargar un modelo**:
   ```bash
   ollama pull llama2
   # o
   ollama pull mistral
   ```

4. **Asegurar que Ollama esté corriendo**:
   ```bash
   ollama serve
   ```

## Dependencias

El proyecto usa las siguientes dependencias gestionadas por uv:

- `ttkbootstrap` - UI moderna basada en Tkinter
- `ollama` - Cliente para Ollama (IA local)
- `requests` - Peticiones HTTP para URLs
- `beautifulsoup4` - Parsing de HTML
- `PyPDF2` - Lectura de archivos PDF
- `python-docx` - Lectura/escritura de Word

## Licencia

MIT License - Uso educativo permitido

## Soporte

Para problemas o sugerencias, consultar la documentación completa en `INSTALL.md`.
