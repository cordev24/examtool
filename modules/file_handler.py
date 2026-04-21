"""
Módulo de manejo de archivos y fuentes para el sistema.
Permite leer contenido de archivos PDF, DOCX, TXT y extraer texto de URLs.
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
import requests
from PyPDF2 import PdfReader
from docx import Document


class FileHandler:
    """Maneja la lectura y procesamiento de archivos de diferentes formatos."""
    
    def __init__(self):
        self.supported_extensions = ['.txt', '.pdf', '.docx', '.md']
    
    def read_file(self, file_path: str) -> Optional[str]:
        """
        Lee el contenido de un archivo según su extensión.
        
        Args:
            file_path: Ruta del archivo a leer
            
        Returns:
            Contenido del archivo como string, o None si hay error
        """
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        extension = path.suffix.lower()
        
        try:
            if extension == '.txt' or extension == '.md':
                return self._read_text(path)
            elif extension == '.pdf':
                return self._read_pdf(path)
            elif extension == '.docx':
                return self._read_docx(path)
            else:
                return None
        except Exception as e:
            print(f"Error leyendo archivo {file_path}: {str(e)}")
            return None
    
    def _read_text(self, path: Path) -> str:
        """Lee archivos de texto plano."""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _read_pdf(self, path: Path) -> str:
        """Lee archivos PDF y extrae el texto."""
        text_content = []
        reader = PdfReader(str(path))
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
        
        return '\n'.join(text_content)
    
    def _read_docx(self, path: Path) -> str:
        """Lee archivos DOCX y extrae el texto."""
        doc = Document(str(path))
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return '\n'.join(paragraphs)
    
    def read_multiple_files(self, file_paths: List[str]) -> Dict[str, str]:
        """
        Lee múltiples archivos y retorna un diccionario con ruta y contenido.
        
        Args:
            file_paths: Lista de rutas de archivos
            
        Returns:
            Diccionario con {ruta: contenido}
        """
        results = {}
        for path in file_paths:
            content = self.read_file(path)
            if content is not None:
                results[path] = content
        return results
    
    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información básica de un archivo.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Diccionario con información del archivo
        """
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        return {
            'name': path.name,
            'extension': path.suffix,
            'size': path.stat().st_size,
            'path': str(path.absolute())
        }


class URLHandler:
    """Maneja la extracción de contenido desde URLs."""
    
    def __init__(self):
        self.timeout = 10  # segundos
    
    def fetch_url_content(self, url: str) -> Optional[str]:
        """
        Obtiene el contenido de texto de una URL.
        
        Args:
            url: URL a consultar
            
        Returns:
            Contenido de texto de la URL, o None si hay error
        """
        try:
            # Validar URL
            if not self._is_valid_url(url):
                return None
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Extraer texto del HTML
            return self._extract_text_from_html(response.text)
            
        except Exception as e:
            print(f"Error obteniendo URL {url}: {str(e)}")
            return None
    
    def _is_valid_url(self, url: str) -> bool:
        """Valida que la URL tenga un formato correcto."""
        url_pattern = re.compile(
            r'^https?://'  # http:// o https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # dominio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # o IP
            r'(?::\d+)?'  # puerto opcional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def _extract_text_from_html(self, html: str) -> str:
        """
        Extrae texto limpio de contenido HTML.
        Implementación básica sin dependencias adicionales.
        """
        # Eliminar etiquetas script y style
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Eliminar todas las etiquetas HTML
        text = re.sub(r'<[^>]+>', ' ', html)
        
        # Decodir entidades HTML básicas
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&amp;', '&')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        
        # Limpiar espacios en blanco
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def fetch_multiple_urls(self, urls: List[str]) -> Dict[str, str]:
        """
        Obtiene contenido de múltiples URLs.
        
        Args:
            urls: Lista de URLs
            
        Returns:
            Diccionario con {url: contenido}
        """
        results = {}
        for url in urls:
            content = self.fetch_url_content(url)
            if content is not None:
                results[url] = content
        return results


class SourceManager:
    """Gestiona las fuentes de información (archivos y URLs) para la generación de exámenes."""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.url_handler = URLHandler()
        self.sources: List[Dict[str, Any]] = []
    
    def add_file_source(self, file_path: str) -> bool:
        """
        Agrega un archivo como fuente.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        content = self.file_handler.read_file(file_path)
        if content is None:
            return False
        
        file_info = self.file_handler.get_file_info(file_path)
        if file_info is None:
            return False
        
        source = {
            'type': 'file',
            'path': file_path,
            'name': file_info['name'],
            'content': content,
            'size': file_info['size']
        }
        
        self.sources.append(source)
        return True
    
    def add_url_source(self, url: str) -> bool:
        """
        Agrega una URL como fuente.
        
        Args:
            url: URL a agregar
            
        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        content = self.url_handler.fetch_url_content(url)
        if content is None:
            return False
        
        source = {
            'type': 'url',
            'path': url,
            'name': url,
            'content': content,
            'size': len(content)
        }
        
        self.sources.append(source)
        return True
    
    def add_sources(self, files: List[str] = None, urls: List[str] = None) -> int:
        """
        Agrega múltiples fuentes (archivos y URLs).
        
        Args:
            files: Lista de rutas de archivos
            urls: Lista de URLs
            
        Returns:
            Número de fuentes agregadas exitosamente
        """
        count = 0
        
        if files:
            for file_path in files:
                if self.add_file_source(file_path):
                    count += 1
        
        if urls:
            for url in urls:
                if self.add_url_source(url):
                    count += 1
        
        return count
    
    def get_all_content(self) -> str:
        """
        Obtiene todo el contenido combinado de las fuentes.
        
        Returns:
            Texto combinado de todas las fuentes
        """
        contents = []
        for source in self.sources:
            contents.append(f"=== FUENTE: {source['name']} ===\n")
            contents.append(source['content'])
            contents.append("\n")
        
        return '\n'.join(contents)
    
    def get_sources_summary(self) -> List[Dict[str, Any]]:
        """
        Obtiene un resumen de las fuentes cargadas.
        
        Returns:
            Lista con información resumida de cada fuente
        """
        return [
            {
                'type': source['type'],
                'name': source['name'],
                'size': source['size'],
                'content_length': len(source['content'])
            }
            for source in self.sources
        ]
    
    def clear_sources(self) -> None:
        """Limpia todas las fuentes cargadas."""
        self.sources = []
    
    def remove_source(self, index: int) -> bool:
        """
        Elimina una fuente por su índice.
        
        Args:
            index: Índice de la fuente a eliminar
            
        Returns:
            True si se eliminó correctamente
        """
        if 0 <= index < len(self.sources):
            del self.sources[index]
            return True
        return False
