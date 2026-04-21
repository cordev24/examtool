# Guía de Instalación y Uso

## Requisitos Previos

### 1. Instalar Ollama

Ollama es necesario para ejecutar los modelos de IA localmente.

**En Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**En macOS:**
```bash
brew install ollama
```

**En Windows:**
Descargue el instalador desde https://ollama.ai/download

### 2. Descargar un Modelo

Después de instalar Ollama, descargue un modelo:

```bash
# Modelos recomendados en español:
ollama pull llama2          # Modelo general (3.5GB)
ollama pull mistral         # Modelo rápido y eficiente (4.1GB)
ollama pull codellama       # Especializado en código (3.8GB)
ollama pull llama2-uncensored  # Sin restricciones de contenido
```

### 3. Iniciar Ollama

```bash
# En segundo plano (Linux/Mac)
ollama serve &

# O dejar que el script run.sh lo inicie automáticamente
```

## Instalación del Sistema

### Paso 1: Clonar o descargar el proyecto

```bash
cd /ruta/donde/guardar/el/proyecto
```

### Paso 2: Instalar dependencias de Python

```bash
pip install ollama requests ttkbootstrap python-docx PyPDF2
```

### Paso 3: Verificar instalación

```bash
python3 -c "import tkinter; print('✅ Tkinter OK')"
python3 -c "import ollama; print('✅ Ollama OK')"
python3 -c "import docx; print('✅ python-docx OK')"
```

## Ejecución

### Opción 1: Usar el script de inicio (recomendado)

```bash
./run.sh
```

### Opción 2: Ejecutar directamente con Python

```bash
python3 main.py
```

## Estructura del Proyecto

```
/workspace/
├── main.py                 # Aplicación principal (Interfaz gráfica)
├── run.sh                  # Script de inicio rápido
├── README.md               # Documentación general
├── config/
│   ├── settings.json       # Configuración general
│   └── templates.json      # Plantillas de documentos
├── modules/
│   ├── config_manager.py   # Gestión de configuración
│   ├── exam_generator.py   # Generación de exámenes con IA
│   ├── file_handler.py     # Manejo de archivos y fuentes
│   ├── history_manager.py  # Historial de exámenes
│   └── export_manager.py   # Exportación a Word/TXT
├── templates/              # Plantillas personalizadas
└── output/                 # Exámenes generados
```

## Uso de la Aplicación

### 1. Pestaña "Generar Examen"

- **Tema**: Ingrese el tema del examen
- **Número de Preguntas**: Cantidad de preguntas a generar
- **Tipos de Preguntas**: Seleccione los tipos (selección múltiple, desarrollo, verdadero/falso)
- **Dificultad**: Fácil, Medio o Difícil
- **Duración**: Tiempo estimado del examen en minutos
- **Incluir Hoja de Respuestas**: Marque si desea incluir respuestas correctas

**Botones:**
- 🚀 **Generar Examen**: Crea el examen usando IA
- 💾 **Exportar a Word**: Guarda como documento .docx
- 📄 **Exportar a Texto**: Guarda como archivo .txt
- 📋 **Copiar al Portapapeles**: Copia el contenido

### 2. Pestaña "Fuentes"

Permite agregar material de referencia para que la IA se base en él:

**Archivos soportados:**
- PDF (.pdf)
- Word (.docx)
- Texto (.txt, .md)

**URLs:**
- Páginas web con contenido educativo
- Artículos en línea
- Documentación técnica

**Funciones:**
- 📁 **Seleccionar Archivos**: Agrega archivos locales
- ➕ **Agregar URL**: Agrega una URL como fuente
- 🗑️ **Eliminar Seleccionada**: Remueve una fuente
- 🧹 **Limpiar Todas**: Elimina todas las fuentes

### 3. Pestaña "Configuración"

**Configuración de Ollama:**
- **Host**: URL del servidor Ollama (por defecto: http://localhost:11434)
- **Modelo**: Modelo de IA a utilizar
- 🔄 **Cargar Modelos**: Obtiene lista de modelos disponibles

**Reglas de Generación:**
- Máximo de preguntas permitidas
- Idioma de los exámenes

### 4. Pestaña "Historial"

Muestra todos los exámenes generados anteriormente:

**Funciones:**
- 🔍 **Buscar**: Filtra exámenes por tema o contenido
- 👁️ **Ver Examen**: Muestra el contenido completo
- 📤 **Exportar**: Guarda un examen previo
- 🗑️ **Eliminar**: Remueve del historial

**Estadísticas mostradas:**
- Total de exámenes generados
- Exámenes exitosos/fallidos
- Temas únicos tratados

## Consejos de Uso

### Para mejores resultados:

1. **Proporcione fuentes específicas**: Adjunte PDFs, apuntes o URLs relevantes al tema
2. **Sea específico en el tema**: En lugar de "Matemáticas", use "Álgebra Lineal: Matrices y Determinantes"
3. **Ajuste la dificultad**: Comience con "Medio" y ajuste según necesite
4. **Revise antes de usar**: Siempre revise el examen generado antes de aplicarlo
5. **Guarde plantillas**: Configure su plantilla institucional una vez y úsela siempre

### Flujo de trabajo recomendado:

1. Abra la aplicación
2. Vaya a "Fuentes" y agregue material de referencia (opcional pero recomendado)
3. En "Generar Examen":
   - Ingrese el tema específico
   - Configure número y tipo de preguntas
   - Haga clic en "Generar Examen"
4. Revise la vista previa
5. Exporte a Word para aplicar la plantilla institucional final
6. El examen se guarda automáticamente en el historial

## Solución de Problemas

### "No se pudo conectar a Ollama"

1. Verifique que Ollama esté instalado: `ollama --version`
2. Inicie Ollama: `ollama serve`
3. Verifique que haya modelos descargados: `ollama list`
4. Descargue un modelo si es necesario: `ollama pull llama2`

### "Error al leer archivo PDF"

- Algunos PDFs escaneados no contienen texto extraíble
- Intente convertir el PDF a texto primero
- Use archivos DOCX o TXT como alternativa

### "La interfaz no responde durante la generación"

- Esto es normal para modelos grandes
- La generación puede tomar de 30 segundos a varios minutos
- No cierre la aplicación, espere a que termine

### "El examen generado no es satisfactorio"

1. Agregue más fuentes de referencia
2. Sea más específico en el tema
3. Pruebe con otro modelo (mistral suele ser más rápido)
4. Ajuste el nivel de dificultad

## Personalización Avanzada

### Modificar plantillas

Edite `config/templates.json` para personalizar:
- Encabezado institucional
- Formato de fuente y márgenes
- Pie de página con avisos de confidencialidad

### Agregar nuevos modelos

```bash
# Descargar modelo adicional
ollama pull nombre-del-modelo

# Aparecerá automáticamente en la lista de modelos disponibles
```

### Cambiar configuración por defecto

Edite `config/settings.json`:
```json
{
    "ollama": {
        "host": "http://localhost:11434",
        "default_model": "mistral"
    },
    "rules": {
        "max_questions": 30,
        "default_exam_duration": 120
    }
}
```

## Soporte

Para reportar errores o sugerencias, consulte la documentación del proyecto o contacte al administrador del sistema.

---

**Nota Importante**: Este sistema utiliza IA para generar contenido. Siempre revise y valide los exámenes generados antes de usarlos en evaluaciones reales.
