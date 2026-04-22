"""
Módulo de exportación de exámenes a diferentes formatos.
Soporta DOCX, PDF y TXT.
"""

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
from typing import Dict, Any, Optional
import re


class ExamExporter:
    """Exporta exámenes generados a diferentes formatos de documento."""
    
    def __init__(self):
        self.supported_formats = ['.txt', '.docx']
    
    def export_to_txt(self, content: str, output_path: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Exporta el examen a un archivo de texto plano.
        
        Args:
            content: Contenido del examen
            output_path: Ruta del archivo de salida
            metadata: Metadatos del examen (opcional)
            
        Returns:
            True si la exportación fue exitosa
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                # Agregar metadatos si existen
                if metadata:
                    f.write("=" * 80 + "\n")
                    f.write(f"TEMA: {metadata.get('topic', 'N/A')}\n")
                    f.write(f"Fecha de generación: {metadata.get('generated_at', 'N/A')}\n")
                    f.write(f"Modelo utilizado: {metadata.get('model_used', 'N/A')}\n")
                    f.write(f"Número de preguntas: {metadata.get('num_questions', 'N/A')}\n")
                    f.write(f"Dificultad: {metadata.get('difficulty', 'N/A')}\n")
                    f.write(f"Duración: {metadata.get('duration_minutes', 'N/A')} minutos\n")
                    f.write("=" * 80 + "\n\n")
                
                f.write(content)
            
            return True
        except Exception as e:
            print(f"Error exportando a TXT: {str(e)}")
            return False
    
    def export_to_docx(self, content: str, output_path: str, 
                       template_config: Dict[str, Any] = None,
                       metadata: Dict[str, Any] = None) -> bool:
        """
        Exporta el examen a un documento Word (.docx).
        
        Args:
            content: Contenido del examen
            output_path: Ruta del archivo de salida
            template_config: Configuración de plantilla (opcional)
            metadata: Metadatos del examen (opcional)
            
        Returns:
            True si la exportación fue exitosa
        """
        try:
            doc = Document()
            
            # Configurar márgenes y formato según plantilla
            if template_config:
                self._apply_template_settings(doc, template_config)
            
            # Agregar encabezado institucional si existe en la plantilla
            if template_config and 'header' in template_config:
                self._add_header(doc, template_config['header'])
            
            # Agregar título del examen
            topic = metadata.get('topic', 'EXAMEN') if metadata else 'EXAMEN'
            title = doc.add_heading(f'EXAMEN: {topic}', level=1)
            title.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # Agregar información del examen
            if metadata:
                self._add_exam_info(doc, metadata)
            
            # Agregar contenido del examen
            self._add_content(doc, content)
            
            # Agregar pie de página si existe en la plantilla
            if template_config and 'footer' in template_config:
                self._add_footer(doc, template_config['footer'])
            
            # Guardar documento
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            doc.save(str(output_file))
            
            return True
        except Exception as e:
            print(f"Error exportando a DOCX: {str(e)}")
            return False
    
    def _apply_template_settings(self, doc: Document, template_config: Dict[str, Any]) -> None:
        """Aplica configuraciones de formato desde la plantilla."""
        formatting = template_config.get('formatting', {})
        
        # Configurar márgenes de las secciones
        for section in doc.sections:
            margins = formatting.get('margins', {})
            if 'top' in margins:
                section.top_margin = Inches(margins['top'] / 2.54)  # Convertir cm a pulgadas
            if 'bottom' in margins:
                section.bottom_margin = Inches(margins['bottom'] / 2.54)
            if 'left' in margins:
                section.left_margin = Inches(margins['left'] / 2.54)
            if 'right' in margins:
                section.right_margin = Inches(margins['right'] / 2.54)
        
        # Configurar fuente por defecto
        style = doc.styles['Normal']
        font = style.font
        font.name = formatting.get('font_family', 'Arial')
        font.size = Pt(formatting.get('font_size', 12))
    
    def _add_header(self, doc: Document, header_config: Dict[str, Any]) -> None:
        """Agrega encabezado institucional."""
        header = doc.sections[0].header
        
        institution = header_config.get('institution_name', '')
        faculty = header_config.get('faculty', '')
        department = header_config.get('department', '')
        
        if institution:
            p = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
            p.text = institution.upper()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].size = Pt(14)
        
        if faculty:
            p = header.add_paragraph()
            p.text = faculty
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].size = Pt(11)
        
        if department:
            p = header.add_paragraph()
            p.text = department
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].size = Pt(11)
        
        # Línea separadora
        header.add_paragraph('_' * 70)
    
    def _add_exam_info(self, doc: Document, metadata: Dict[str, Any]) -> None:
        """Agrega información del examen (curso, fecha, duración, etc.)."""
        doc.add_paragraph()
        
        info_table = doc.add_table(rows=4, cols=2)
        info_table.style = 'Table Grid'
        
        # Llenar tabla con información
        info_data = [
            ('Curso/Materia:', metadata.get('course', 'N/A')),
            ('Duración:', f"{metadata.get('duration_minutes', 90)} minutos"),
            ('Número de preguntas:', str(metadata.get('num_questions', 'N/A'))),
            ('Dificultad:', metadata.get('difficulty', 'N/A'))
        ]
        
        for i, (label, value) in enumerate(info_data):
            info_table.rows[i].cells[0].text = label
            info_table.rows[i].cells[1].text = value
            info_table.rows[i].cells[0].paragraphs[0].runs[0].bold = True
        
        doc.add_paragraph()
    
    def _add_content(self, doc: Document, content: str) -> None:
        """Agrega el contenido del examen al documento."""
        # Dividir el contenido en líneas y agregarlas como párrafos
        lines = content.split('\n')
        
        for line in lines:
            # Detectar tipo de línea y aplicar formato apropiado
            if line.startswith('===') or line.startswith('---'):
                # Línea separadora
                if line.strip():
                    doc.add_paragraph()
            elif line.startswith('SECCIÓN') or line.startswith('SECTION'):
                # Título de sección
                p = doc.add_heading(line, level=2)
            elif re.match(r'^\d+[\.|\)]', line):
                # Pregunta numerada
                p = doc.add_paragraph(line)
                p.paragraph_format.space_after = Pt(6)
            elif line.startswith('INSTRUCCIONES'):
                # Instrucciones
                p = doc.add_paragraph(line)
                p.runs[0].bold = True
                p.runs[0].italic = True
            else:
                # Texto normal
                if line.strip():
                    doc.add_paragraph(line)
    
    def _add_footer(self, doc: Document, footer_config: Dict[str, Any]) -> None:
        """Agrega pie de página."""
        footer = doc.sections[0].footer
        
        # Número de página
        if footer_config.get('include_page_numbers', True):
            p = footer.add_paragraph()
            p.text = 'Página '
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Nota de confidencialidad
        confidentiality = footer_config.get('confidentiality_notice', '')
        if confidentiality:
            p = footer.add_paragraph()
            p.text = confidentiality
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].size = Pt(9)
            p.runs[0].italic = True
    
    def export(self, content: str, output_path: str, format: str = 'txt',
               template_config: Dict[str, Any] = None,
               metadata: Dict[str, Any] = None) -> bool:
        """
        Exporta el examen al formato especificado.
        
        Args:
            content: Contenido del examen
            output_path: Ruta del archivo de salida
            format: Formato de exportación ('txt' o 'docx')
            template_config: Configuración de plantilla
            metadata: Metadatos del examen
            
        Returns:
            True si la exportación fue exitosa
        """
        format_lower = format.lower()
        
        if format_lower == 'txt':
            return self.export_to_txt(content, output_path, metadata)
        elif format_lower == 'docx':
            return self.export_to_docx(content, output_path, template_config, metadata)
        else:
            print(f"Formato no soportado: {format}")
            return False
    
    def get_supported_formats(self) -> list:
        """Retorna la lista de formatos soportados."""
        return self.supported_formats.copy()
