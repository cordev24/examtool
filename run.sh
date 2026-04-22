#!/bin/bash
# Script de inicio rápido para el Sistema de Generación de Exámenes con IA

echo "=============================================="
echo "  Sistema de Generación de Exámenes con IA"
echo "=============================================="
echo ""

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
    echo "   Iniciando Ollama..."
    ollama serve &
    sleep 3
fi

echo "✅ Ollama está corriendo"

# Verificar modelos disponibles
echo ""
echo "📦 Modelos disponibles:"
ollama list 2>/dev/null || echo "   No se pudieron listar los modelos"

echo ""
echo "=============================================="
echo "  Iniciando la aplicación..."
echo "=============================================="
echo ""

# Ejecutar la aplicación
cd "$(dirname "$0")"
python3 main.py
