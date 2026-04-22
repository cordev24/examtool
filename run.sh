#!/bin/bash
# Script de inicio rápido para el Sistema de Generación de Exámenes con IA
# Usa uv como gestor de paquetes

set -e

echo "=============================================="
echo "  Sistema de Generación de Exámenes con IA"
echo "=============================================="
echo ""

# Verificar si uv está disponible
if ! command -v uv &> /dev/null; then
    echo "❌ uv no está instalado."
    echo "   Por favor, instale uv desde: https://docs.astral.sh/uv/getting-started/installation/"
    echo ""
    echo "   Comando de instalación:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi

echo "✅ uv detectado: $(uv --version)"

# Verificar si Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama no está instalado."
    echo "   Por favor, instale Ollama desde: https://ollama.ai"
    echo ""
    echo "   En Linux/Mac:"
    echo "   curl -fsSL https://ollama.ai/install.sh | sh"
    echo ""
    exit 1
fi

echo "✅ Ollama detectado"

# Verificar si Ollama está corriendo
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "⚠️  Ollama no está ejecutándose."
    echo "   Iniciando Ollama en segundo plano..."
    ollama serve &
    OLLAMA_PID=$!
    sleep 3
    
    # Función para limpiar al salir
    cleanup() {
        echo ""
        echo "Deteniendo Ollama..."
        kill $OLLAMA_PID 2>/dev/null || true
    }
    trap cleanup EXIT
fi

echo "✅ Ollama está corriendo"

# Verificar modelos disponibles
echo ""
echo "📦 Modelos disponibles:"
ollama list 2>/dev/null || echo "   No se pudieron listar los modelos"

echo ""
echo "=============================================="
echo "  Instalando/Verificando dependencias con uv"
echo "=============================================="
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Sincronizar dependencias con uv
uv sync

echo ""
echo "=============================================="
echo "  Iniciando la aplicación..."
echo "=============================================="
echo ""

# Ejecutar la aplicación con uv run
uv run python main.py
