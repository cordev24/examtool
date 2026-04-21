"""
Módulo de gestión de configuración y plantillas del sistema.
Permite cargar, guardar y administrar configuraciones y plantillas de documentos.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any


class ConfigManager:
    """Gestiona la configuración general de la aplicación."""
    
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Carga la configuración desde el archivo JSON."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = self._get_default_config()
            self.save_config()
    
    def save_config(self) -> None:
        """Guarda la configuración en el archivo JSON."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Retorna la configuración por defecto."""
        return {
            "app_name": "Sistema de Generación de Exámenes con IA",
            "version": "1.0.0",
            "ollama": {
                "host": "http://localhost:11434",
                "default_model": "llama2"
            },
            "templates_path": "templates",
            "output_path": "output",
            "rules": {
                "max_questions": 20,
                "default_exam_duration": 90,
                "include_answer_key": True,
                "language": "es"
            }
        }
    
    def get_ollama_host(self) -> str:
        """Obtiene el host de Ollama."""
        return self.config.get("ollama", {}).get("host", "http://localhost:11434")
    
    def get_default_model(self) -> str:
        """Obtiene el modelo por defecto de Ollama."""
        return self.config.get("ollama", {}).get("default_model", "llama2")
    
    def get_output_path(self) -> Path:
        """Obtiene la ruta de salida."""
        return Path(self.config.get("output_path", "output"))
    
    def get_rules(self) -> Dict[str, Any]:
        """Obtiene las reglas de generación."""
        return self.config.get("rules", {})
    
    def update_ollama_settings(self, host: str, model: str) -> None:
        """Actualiza la configuración de Ollama."""
        if "ollama" not in self.config:
            self.config["ollama"] = {}
        self.config["ollama"]["host"] = host
        self.config["ollama"]["default_model"] = model
        self.save_config()
    
    def update_rules(self, rules: Dict[str, Any]) -> None:
        """Actualiza las reglas de generación."""
        self.config["rules"] = rules
        self.save_config()


class TemplateManager:
    """Gestiona las plantillas de documentos."""
    
    def __init__(self, templates_path: str = "config/templates.json"):
        self.templates_path = Path(templates_path)
        self.templates: List[Dict[str, Any]] = []
        self.load_templates()
    
    def load_templates(self) -> None:
        """Carga las plantillas desde el archivo JSON."""
        if self.templates_path.exists():
            with open(self.templates_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.templates = data.get("templates", [])
        else:
            self.templates = self._get_default_templates()
            self.save_templates()
    
    def save_templates(self) -> None:
        """Guarda las plantillas en el archivo JSON."""
        self.templates_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.templates_path, 'w', encoding='utf-8') as f:
            json.dump({"templates": self.templates}, f, indent=4, ensure_ascii=False)
    
    def _get_default_templates(self) -> List[Dict[str, Any]]:
        """Retorna las plantillas por defecto."""
        return [
            {
                "id": "template_001",
                "name": "Plantilla Estándar Universidad",
                "description": "Formato estándar para exámenes universitarios",
                "header": {
                    "institution_name": "UNIVERSIDAD EJEMPLO",
                    "faculty": "Facultad de Ciencias",
                    "department": "Departamento de Matemáticas",
                    "logo_path": "",
                    "show_logo": False
                },
                "exam_info": {
                    "include_course_name": True,
                    "include_student_name": True,
                    "include_date": True,
                    "include_duration": True,
                    "include_score": True
                },
                "footer": {
                    "include_page_numbers": True,
                    "confidentiality_notice": "Este documento es confidencial y de uso exclusivo para fines académicos."
                },
                "formatting": {
                    "font_family": "Arial",
                    "font_size": 12,
                    "line_spacing": 1.5,
                    "margins": {
                        "top": 2.54,
                        "bottom": 2.54,
                        "left": 2.54,
                        "right": 2.54
                    }
                }
            }
        ]
    
    def get_all_templates(self) -> List[Dict[str, Any]]:
        """Obtiene todas las plantillas disponibles."""
        return self.templates
    
    def get_template_by_id(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene una plantilla por su ID."""
        for template in self.templates:
            if template.get("id") == template_id:
                return template
        return None
    
    def get_template_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Obtiene una plantilla por su nombre."""
        for template in self.templates:
            if template.get("name") == name:
                return template
        return None
    
    def add_template(self, template: Dict[str, Any]) -> bool:
        """Agrega una nueva plantilla."""
        if "id" not in template or "name" not in template:
            return False
        
        # Verificar que el ID sea único
        if self.get_template_by_id(template["id"]):
            return False
        
        self.templates.append(template)
        self.save_templates()
        return True
    
    def update_template(self, template_id: str, updated_template: Dict[str, Any]) -> bool:
        """Actualiza una plantilla existente."""
        for i, template in enumerate(self.templates):
            if template.get("id") == template_id:
                updated_template["id"] = template_id  # Mantener el ID original
                self.templates[i] = updated_template
                self.save_templates()
                return True
        return False
    
    def delete_template(self, template_id: str) -> bool:
        """Elimina una plantilla."""
        for i, template in enumerate(self.templates):
            if template.get("id") == template_id:
                del self.templates[i]
                self.save_templates()
                return True
        return False
    
    def get_template_names(self) -> List[str]:
        """Obtiene los nombres de todas las plantillas."""
        return [t.get("name", "Sin nombre") for t in self.templates]
