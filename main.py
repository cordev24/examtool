"""
Aplicación principal del Sistema de Generación de Exámenes con IA.
Interfaz gráfica moderna usando ttkbootstrap.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from pathlib import Path
import threading

# Importar módulos del sistema
import sys
sys.path.append(str(Path(__file__).parent))

from modules.config_manager import ConfigManager, TemplateManager
from modules.file_handler import SourceManager
from modules.exam_generator import ExamGenerator
from modules.history_manager import HistoryManager
from modules.export_manager import ExamExporter


class ExamGeneratorApp:
    """Aplicación principal con interfaz gráfica."""
    
    def __init__(self):
        # Inicializar ventana principal
        self.root = ttkb.Window(themename="cosmo")
        self.root.title("Sistema de Generación de Exámenes con IA")
        self.root.geometry("1200x800")
        
        # Inicializar gestores
        self.config_manager = ConfigManager()
        self.template_manager = TemplateManager()
        self.source_manager = SourceManager()
        self.exam_generator = None
        self.history_manager = HistoryManager()
        self.exporter = ExamExporter()
        
        # Variables de estado
        self.current_exam_content = ""
        self.current_metadata = {}
        
        # Configurar interfaz
        self.setup_ui()
        
        # Verificar conexión con Ollama
        self.check_ollama_connection()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Crear notebook (pestañas)
        self.notebook = ttkb.Notebook(self.root, bootstyle=PRIMARY)
        self.notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Crear pestañas
        self.tab_generator = ttkb.Frame(self.notebook)
        self.tab_config = ttkb.Frame(self.notebook)
        self.tab_history = ttkb.Frame(self.notebook)
        self.tab_sources = ttkb.Frame(self.notebook)
        
        self.notebook.add(self.tab_generator, text="📝 Generar Examen")
        self.notebook.add(self.tab_sources, text="📚 Fuentes")
        self.notebook.add(self.tab_config, text="⚙️ Configuración")
        self.notebook.add(self.tab_history, text="📋 Historial")
        
        # Configurar cada pestaña
        self.setup_generator_tab()
        self.setup_sources_tab()
        self.setup_config_tab()
        self.setup_history_tab()
    
    def setup_generator_tab(self):
        """Configura la pestaña de generación de exámenes."""
        # Frame principal con dos columnas
        main_frame = ttkb.Frame(self.tab_generator)
        main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Columna izquierda - Configuración del examen
        left_frame = ttkb.LabelFrame(main_frame, text="Configuración del Examen", bootstyle=INFO)
        left_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5, ipadx=10, ipady=10)
        
        # Tema del examen
        ttkb.Label(left_frame, text="Tema del Examen:", bootstyle=INFO).pack(anchor=W, pady=(10, 5))
        self.topic_entry = ttkb.Entry(left_frame, width=50, bootstyle=INFO)
        self.topic_entry.pack(fill=X, pady=5)
        self.topic_entry.insert(0, "Introducción a la Programación")
        
        # Número de preguntas
        ttkb.Label(left_frame, text="Número de Preguntas:").pack(anchor=W, pady=(10, 5))
        self.num_questions_spin = ttkb.Spinbox(left_frame, from_=1, to=50, width=20, bootstyle=INFO)
        self.num_questions_spin.pack(anchor=W, pady=5)
        self.num_questions_spin.set(10)
        
        # Tipos de preguntas
        ttkb.Label(left_frame, text="Tipos de Preguntas:").pack(anchor=W, pady=(10, 5))
        self.multiple_choice_var = tk.BooleanVar(value=True)
        self.development_var = tk.BooleanVar(value=True)
        self.true_false_var = tk.BooleanVar(value=False)
        
        ttkb.Checkbutton(left_frame, text="Selección Múltiple", variable=self.multiple_choice_var, 
                        bootstyle="success-round-toggle").pack(anchor=W, pady=2)
        ttkb.Checkbutton(left_frame, text="Desarrollo", variable=self.development_var, 
                        bootstyle="success-round-toggle").pack(anchor=W, pady=2)
        ttkb.Checkbutton(left_frame, text="Verdadero/Falso", variable=self.true_false_var, 
                        bootstyle="success-round-toggle").pack(anchor=W, pady=2)
        
        # Dificultad
        ttkb.Label(left_frame, text="Nivel de Dificultad:").pack(anchor=W, pady=(10, 5))
        self.difficulty_combo = ttkb.Combobox(left_frame, values=["Fácil", "Medio", "Difícil"], 
                                              state="readonly", width=20, bootstyle=INFO)
        self.difficulty_combo.pack(anchor=W, pady=5)
        self.difficulty_combo.set("Medio")
        
        # Duración
        ttkb.Label(left_frame, text="Duración (minutos):").pack(anchor=W, pady=(10, 5))
        self.duration_spin = ttkb.Spinbox(left_frame, from_=15, to=180, width=20, bootstyle=INFO)
        self.duration_spin.pack(anchor=W, pady=5)
        self.duration_spin.set(90)
        
        # Incluir respuestas
        self.include_answers_var = tk.BooleanVar(value=True)
        ttkb.Checkbutton(left_frame, text="Incluir Hoja de Respuestas", 
                        variable=self.include_answers_var, bootstyle="success-round-toggle").pack(anchor=W, pady=10)
        
        # Botón generar
        self.generate_btn = ttkb.Button(left_frame, text="🚀 Generar Examen", 
                                       command=self.generate_exam, bootstyle=SUCCESS)
        self.generate_btn.pack(fill=X, pady=20)
        
        # Columna derecha - Vista previa
        right_frame = ttkb.LabelFrame(main_frame, text="Vista Previa del Examen", bootstyle=WARNING)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=5, pady=5)
        
        # Área de texto para vista previa
        self.preview_text = tk.Text(right_frame, wrap=tk.WORD, width=60, height=30)
        preview_scrollbar = ttkb.Scrollbar(right_frame, orient=VERTICAL, command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_text.pack(side=LEFT, fill=BOTH, expand=YES)
        preview_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Botones de exportación
        export_frame = ttkb.Frame(right_frame)
        export_frame.pack(fill=X, pady=10)
        
        ttkb.Button(export_frame, text="💾 Exportar a Word", 
                   command=lambda: self.export_exam('docx'), bootstyle=PRIMARY).pack(side=LEFT, padx=5)
        ttkb.Button(export_frame, text="📄 Exportar a Texto", 
                   command=lambda: self.export_exam('txt'), bootstyle=SECONDARY).pack(side=LEFT, padx=5)
        ttkb.Button(export_frame, text="📋 Copiar al Portapapeles", 
                   command=self.copy_to_clipboard, bootstyle=INFO).pack(side=LEFT, padx=5)
    
    def setup_sources_tab(self):
        """Configura la pestaña de gestión de fuentes."""
        main_frame = ttkb.Frame(self.tab_sources)
        main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Frame superior - Agregar fuentes
        top_frame = ttkb.LabelFrame(main_frame, text="Agregar Fuentes de Referencia", bootstyle=INFO)
        top_frame.pack(fill=X, padx=5, pady=5)
        
        # Agregar archivos
        file_frame = ttkb.Frame(top_frame)
        file_frame.pack(fill=X, pady=10)
        
        ttkb.Label(file_frame, text="Archivos (PDF, DOCX, TXT):").pack(side=LEFT, padx=5)
        ttkb.Button(file_frame, text="📁 Seleccionar Archivos", 
                   command=self.add_files, bootstyle=INFO).pack(side=LEFT, padx=5)
        
        # Agregar URLs
        url_frame = ttkb.Frame(top_frame)
        url_frame.pack(fill=X, pady=10)
        
        ttkb.Label(url_frame, text="URLs:").pack(side=LEFT, padx=5)
        self.url_entry = ttkb.Entry(url_frame, width=60, bootstyle=INFO)
        self.url_entry.pack(side=LEFT, padx=5, fill=X, expand=YES)
        ttkb.Button(url_frame, text="➕ Agregar URL", 
                   command=self.add_url, bootstyle=INFO).pack(side=LEFT, padx=5)
        
        # Lista de fuentes cargadas
        list_frame = ttkb.LabelFrame(main_frame, text="Fuentes Cargadas", bootstyle=WARNING)
        list_frame.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        # Treeview para mostrar fuentes
        columns = ('Tipo', 'Nombre', 'Tamaño')
        self.sources_tree = ttkb.Treeview(list_frame, columns=columns, show='headings', bootstyle=INFO)
        
        self.sources_tree.heading('Tipo', text='Tipo')
        self.sources_tree.heading('Nombre', text='Nombre')
        self.sources_tree.heading('Tamaño', text='Tamaño (bytes)')
        
        self.sources_tree.column('Tipo', width=100)
        self.sources_tree.column('Nombre', width=400)
        self.sources_tree.column('Tamaño', width=100)
        
        sources_scrollbar = ttkb.Scrollbar(list_frame, orient=VERTICAL, command=self.sources_tree.yview)
        self.sources_tree.configure(yscrollcommand=sources_scrollbar.set)
        
        self.sources_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        sources_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Botones de acción
        btn_frame = ttkb.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)
        
        ttkb.Button(btn_frame, text="🗑️ Eliminar Seleccionada", 
                   command=self.remove_source, bootstyle=DANGER).pack(side=LEFT, padx=5)
        ttkb.Button(btn_frame, text="🧹 Limpiar Todas", 
                   command=self.clear_sources, bootstyle=WARNING).pack(side=LEFT, padx=5)
        
        # Actualizar lista
        self.refresh_sources_list()
    
    def setup_config_tab(self):
        """Configura la pestaña de configuración."""
        main_frame = ttkb.Frame(self.tab_config)
        main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Configuración de Ollama
        ollama_frame = ttkb.LabelFrame(main_frame, text="Configuración de Ollama", bootstyle=INFO)
        ollama_frame.pack(fill=X, padx=5, pady=5)
        
        ttkb.Label(ollama_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.ollama_host_entry = ttkb.Entry(ollama_frame, width=40, bootstyle=INFO)
        self.ollama_host_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ollama_host_entry.insert(0, self.config_manager.get_ollama_host())
        
        ttkb.Label(ollama_frame, text="Modelo:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.model_combo = ttkb.Combobox(ollama_frame, width=37, bootstyle=INFO)
        self.model_combo.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        self.model_combo.set(self.config_manager.get_default_model())
        
        # Botón para cargar modelos disponibles
        ttkb.Button(ollama_frame, text="🔄 Cargar Modelos", 
                   command=self.load_available_models, bootstyle=INFO).grid(row=1, column=2, padx=5, pady=5)
        
        # Guardar configuración
        ttkb.Button(ollama_frame, text="💾 Guardar Configuración", 
                   command=self.save_config, bootstyle=SUCCESS).grid(row=2, column=1, padx=5, pady=10)
        
        # Estado de conexión
        self.connection_label = ttkb.Label(ollama_frame, text="Estado: Verificando...", bootstyle=WARNING)
        self.connection_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky=W)
        
        # Reglas de generación
        rules_frame = ttkb.LabelFrame(main_frame, text="Reglas de Generación", bootstyle=WARNING)
        rules_frame.pack(fill=X, padx=5, pady=5)
        
        ttkb.Label(rules_frame, text="Máximo de preguntas:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.max_questions_spin = ttkb.Spinbox(rules_frame, from_=1, to=100, width=10, bootstyle=WARNING)
        self.max_questions_spin.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        self.max_questions_spin.set(self.config_manager.get_rules().get('max_questions', 20))
        
        ttkb.Label(rules_frame, text="Idioma:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.language_combo = ttkb.Combobox(rules_frame, values=["Español", "English", "Português"], 
                                           state="readonly", width=35, bootstyle=WARNING)
        self.language_combo.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        self.language_combo.set("Español")
    
    def setup_history_tab(self):
        """Configura la pestaña de historial."""
        main_frame = ttkb.Frame(self.tab_history)
        main_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        # Buscador
        search_frame = ttkb.Frame(main_frame)
        search_frame.pack(fill=X, pady=5)
        
        ttkb.Label(search_frame, text="🔍 Buscar:").pack(side=LEFT, padx=5)
        self.search_entry = ttkb.Entry(search_frame, width=50, bootstyle=INFO)
        self.search_entry.pack(side=LEFT, padx=5)
        ttkb.Button(search_frame, text="Buscar", 
                   command=self.search_history, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttkb.Button(search_frame, text="Mostrar Todos", 
                   command=self.refresh_history, bootstyle=SECONDARY).pack(side=LEFT, padx=5)
        
        # Lista de exámenes
        list_frame = ttkb.LabelFrame(main_frame, text="Exámenes Generados", bootstyle=INFO)
        list_frame.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        columns = ('Fecha', 'Tema', 'Modelo', 'Preguntas')
        self.history_tree = ttkb.Treeview(list_frame, columns=columns, show='headings', bootstyle=INFO)
        
        self.history_tree.heading('Fecha', text='Fecha')
        self.history_tree.heading('Tema', text='Tema')
        self.history_tree.heading('Modelo', text='Modelo')
        self.history_tree.heading('Preguntas', text='Preguntas')
        
        self.history_tree.column('Fecha', width=150)
        self.history_tree.column('Tema', width=300)
        self.history_tree.column('Modelo', width=100)
        self.history_tree.column('Preguntas', width=80)
        
        history_scrollbar = ttkb.Scrollbar(list_frame, orient=VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        history_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Bind para ver examen al hacer doble click
        self.history_tree.bind('<Double-Button-1>', self.view_selected_exam)
        
        # Botones de acción
        btn_frame = ttkb.Frame(main_frame)
        btn_frame.pack(fill=X, pady=10)
        
        ttkb.Button(btn_frame, text="👁️ Ver Examen", 
                   command=self.view_selected_exam, bootstyle=INFO).pack(side=LEFT, padx=5)
        ttkb.Button(btn_frame, text="📤 Exportar", 
                   command=self.export_from_history, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        ttkb.Button(btn_frame, text="🗑️ Eliminar", 
                   command=self.delete_from_history, bootstyle=DANGER).pack(side=LEFT, padx=5)
        
        # Estadísticas
        stats_frame = ttkb.LabelFrame(main_frame, text="Estadísticas", bootstyle=WARNING)
        stats_frame.pack(fill=X, padx=5, pady=5)
        
        self.stats_label = ttkb.Label(stats_frame, text="Cargando estadísticas...")
        self.stats_label.pack(padx=10, pady=10, anchor=W)
        
        # Cargar historial
        self.refresh_history()
    
    def check_ollama_connection(self):
        """Verifica la conexión con Ollama."""
        try:
            self.exam_generator = ExamGenerator(
                host=self.config_manager.get_ollama_host(),
                model=self.config_manager.get_default_model()
            )
            
            if self.exam_generator.check_connection():
                self.connection_label.configure(text="✅ Conectado a Ollama", bootstyle=SUCCESS)
            else:
                self.connection_label.configure(text="❌ No se pudo conectar a Ollama", bootstyle=DANGER)
        except Exception as e:
            self.connection_label.configure(text=f"❌ Error: {str(e)}", bootstyle=DANGER)
    
    def load_available_models(self):
        """Carga los modelos disponibles desde Ollama."""
        if not self.exam_generator:
            self.check_ollama_connection()
        
        models = self.exam_generator.get_available_models()
        if models:
            self.model_combo['values'] = models
            if self.model_combo.get() not in models:
                self.model_combo.set(models[0])
            messagebox.showinfo("Modelos", f"Se encontraron {len(models)} modelos disponibles")
        else:
            messagebox.showwarning("Advertencia", "No se pudieron cargar los modelos. Verifica que Ollama esté ejecutándose.")
    
    def add_files(self):
        """Abre diálogo para seleccionar archivos."""
        files = filedialog.askopenfilenames(
            title="Seleccionar Archivos",
            filetypes=[
                ("Archivos soportados", "*.pdf *.docx *.txt *.md"),
                ("PDF", "*.pdf"),
                ("Word", "*.docx"),
                ("Texto", "*.txt *.md"),
                ("Todos", "*.*")
            ]
        )
        
        count = 0
        for file_path in files:
            if self.source_manager.add_file_source(file_path):
                count += 1
        
        if count > 0:
            self.refresh_sources_list()
            messagebox.showinfo("Éxito", f"Se agregaron {count} archivo(s)")
        elif files:
            messagebox.showerror("Error", "No se pudo leer ningún archivo")
    
    def add_url(self):
        """Agrega una URL como fuente."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Advertencia", "Por favor ingrese una URL")
            return
        
        if self.source_manager.add_url_source(url):
            self.url_entry.delete(0, tk.END)
            self.refresh_sources_list()
            messagebox.showinfo("Éxito", "URL agregada correctamente")
        else:
            messagebox.showerror("Error", "No se pudo obtener el contenido de la URL")
    
    def refresh_sources_list(self):
        """Actualiza la lista de fuentes en la interfaz."""
        # Limpiar treeview
        for item in self.sources_tree.get_children():
            self.sources_tree.delete(item)
        
        # Agregar fuentes
        for source in self.source_manager.get_sources_summary():
            size_str = f"{source['size']:,}"
            self.sources_tree.insert('', tk.END, values=(
                source['type'].upper(),
                source['name'],
                size_str
            ))
    
    def remove_source(self):
        """Elimina la fuente seleccionada."""
        selected = self.sources_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una fuente para eliminar")
            return
        
        # Obtener índice y eliminar
        index = self.sources_tree.index(selected[0])
        self.source_manager.remove_source(index)
        self.refresh_sources_list()
    
    def clear_sources(self):
        """Limpia todas las fuentes."""
        if messagebox.askyesno("Confirmar", "¿Está seguro de limpiar todas las fuentes?"):
            self.source_manager.clear_sources()
            self.refresh_sources_list()
    
    def generate_exam(self):
        """Genera un examen usando IA."""
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Advertencia", "Por favor ingrese el tema del examen")
            return
        
        # Recopilar configuración
        num_questions = int(self.num_questions_spin.get())
        difficulty = self.difficulty_combo.get().lower()
        duration = int(self.duration_spin.get())
        include_answers = self.include_answers_var.get()
        
        # Tipos de preguntas
        question_types = []
        if self.multiple_choice_var.get():
            question_types.append("selección múltiple")
        if self.development_var.get():
            question_types.append("desarrollo")
        if self.true_false_var.get():
            question_types.append("verdadero/falso")
        
        if not question_types:
            messagebox.showwarning("Advertencia", "Seleccione al menos un tipo de pregunta")
            return
        
        # Obtener contenido de fuentes
        sources_content = self.source_manager.get_all_content()
        
        # Deshabilitar botón durante generación
        self.generate_btn.configure(state=DISABLED, text="⏳ Generando...")
        self.root.update()
        
        # Generar en hilo separado para no congelar UI
        def generate_thread():
            try:
                result = self.exam_generator.generate_exam(
                    topic=topic,
                    sources_content=sources_content if sources_content else None,
                    num_questions=num_questions,
                    question_types=question_types,
                    difficulty=difficulty,
                    duration_minutes=duration,
                    include_answers=include_answers,
                    language="español"
                )
                
                # Actualizar UI en el hilo principal
                self.root.after(0, lambda: self.on_exam_generated(result))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Error generando examen: {str(e)}"))
            finally:
                self.root.after(0, lambda: self.generate_btn.configure(state=NORMAL, text="🚀 Generar Examen"))
        
        thread = threading.Thread(target=generate_thread)
        thread.start()
    
    def on_exam_generated(self, result):
        """Maneja el resultado de la generación del examen."""
        if result.get('success'):
            self.current_exam_content = result.get('content', '')
            self.current_metadata = result.get('metadata', {})
            
            # Mostrar en vista previa
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(tk.END, self.current_exam_content)
            
            # Guardar en historial
            self.history_manager.add_exam(result)
            self.refresh_history()
            
            messagebox.showinfo("Éxito", "Examen generado correctamente")
        else:
            error_msg = result.get('error', 'Error desconocido')
            messagebox.showerror("Error", f"No se pudo generar el examen: {error_msg}")
    
    def export_exam(self, format_type):
        """Exporta el examen actual."""
        if not self.current_exam_content:
            messagebox.showwarning("Advertencia", "No hay examen para exportar")
            return
        
        # Diálogo de guardado
        filetypes = [
            ("Word", "*.docx"),
            ("Texto", "*.txt"),
            ("Todos", "*.*")
        ]
        
        default_ext = '.docx' if format_type == 'docx' else '.txt'
        filename = filedialog.asksaveasfilename(
            title="Guardar Examen",
            defaultextension=default_ext,
            filetypes=filetypes
        )
        
        if filename:
            template = self.template_manager.get_all_templates()
            template_config = template[0] if template else None
            
            success = self.exporter.export(
                content=self.current_exam_content,
                output_path=filename,
                format=format_type,
                template_config=template_config,
                metadata=self.current_metadata
            )
            
            if success:
                messagebox.showinfo("Éxito", f"Examen exportado a: {filename}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el examen")
    
    def copy_to_clipboard(self):
        """Copia el examen al portapapeles."""
        if not self.current_exam_content:
            messagebox.showwarning("Advertencia", "No hay examen para copiar")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(self.current_exam_content)
        messagebox.showinfo("Éxito", "Examen copiado al portapapeles")
    
    def save_config(self):
        """Guarda la configuración."""
        host = self.ollama_host_entry.get().strip()
        model = self.model_combo.get().strip()
        
        if not host or not model:
            messagebox.showwarning("Advertencia", "Host y modelo son requeridos")
            return
        
        self.config_manager.update_ollama_settings(host, model)
        
        # Actualizar reglas
        rules = {
            'max_questions': int(self.max_questions_spin.get()),
            'language': self.language_combo.get().lower(),
            'default_exam_duration': int(self.duration_spin.get()),
            'include_answer_key': self.include_answers_var.get()
        }
        self.config_manager.update_rules(rules)
        
        # Reiniciar generador con nueva configuración
        self.exam_generator = ExamGenerator(host=host, model=model)
        self.check_ollama_connection()
        
        messagebox.showinfo("Éxito", "Configuración guardada correctamente")
    
    def refresh_history(self):
        """Actualiza la lista del historial."""
        # Limpiar treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Agregar exámenes
        exams = self.history_manager.get_all_exams()
        for exam in exams:
            metadata = exam.get('metadata', {})
            date_str = exam.get('timestamp', 'N/A')[:19].replace('T', ' ')
            
            self.history_tree.insert('', tk.END, values=(
                date_str,
                exam.get('topic', 'Sin tema'),
                metadata.get('model_used', 'N/A'),
                metadata.get('num_questions', 'N/A')
            ), tags=(exam.get('id'),))
        
        # Actualizar estadísticas
        self.update_statistics()
    
    def update_statistics(self):
        """Actualiza las estadísticas del historial."""
        stats = self.history_manager.get_statistics()
        
        stats_text = (
            f"Total de exámenes: {stats['total_exams']}\n"
            f"Exitosos: {stats['successful_exams']}\n"
            f"Fallidos: {stats['failed_exams']}\n"
            f"Temas únicos: {stats['unique_topics']}\n"
            f"Más reciente: {stats['most_recent'][:19] if stats['most_recent'] else 'N/A'}"
        )
        
        self.stats_label.configure(text=stats_text)
    
    def search_history(self):
        """Busca en el historial."""
        query = self.search_entry.get().strip()
        if not query:
            self.refresh_history()
            return
        
        # Limpiar treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Buscar y mostrar resultados
        results = self.history_manager.search_exams(query)
        for exam in results:
            metadata = exam.get('metadata', {})
            date_str = exam.get('timestamp', 'N/A')[:19].replace('T', ' ')
            
            self.history_tree.insert('', tk.END, values=(
                date_str,
                exam.get('topic', 'Sin tema'),
                metadata.get('model_used', 'N/A'),
                metadata.get('num_questions', 'N/A')
            ), tags=(exam.get('id'),))
    
    def view_selected_exam(self, event=None):
        """Muestra el examen seleccionado."""
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un examen para ver")
            return
        
        # Obtener ID del examen
        item_values = self.history_tree.item(selected[0], 'tags')
        if not item_values:
            return
        
        exam_id = item_values[0]
        exam = self.history_manager.get_exam_by_id(exam_id)
        
        if exam:
            # Mostrar en ventana emergente
            top = tk.Toplevel(self.root)
            top.title(f"Examen: {exam.get('topic', 'Sin tema')}")
            top.geometry("800x600")
            
            text_widget = tk.Text(top, wrap=tk.WORD)
            text_widget.pack(fill=BOTH, expand=YES, padx=10, pady=10)
            text_widget.insert(tk.END, exam.get('content', ''))
            text_widget.configure(state='disabled')
            
            scrollbar = ttkb.Scrollbar(top, orient=VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=RIGHT, fill=Y)
    
    def export_from_history(self):
        """Exporta un examen desde el historial."""
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un examen para exportar")
            return
        
        item_values = self.history_tree.item(selected[0], 'tags')
        if not item_values:
            return
        
        exam_id = item_values[0]
        exam = self.history_manager.get_exam_by_id(exam_id)
        
        if exam:
            filename = filedialog.asksaveasfilename(
                title="Guardar Examen",
                defaultextension=".docx",
                filetypes=[("Word", "*.docx"), ("Texto", "*.txt")]
            )
            
            if filename:
                success = self.history_manager.export_exam_to_file(exam_id, filename)
                if success:
                    messagebox.showinfo("Éxito", f"Examen exportado a: {filename}")
                else:
                    messagebox.showerror("Error", "No se pudo exportar el examen")
    
    def delete_from_history(self):
        """Elimina un examen del historial."""
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un examen para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este examen del historial?"):
            item_values = self.history_tree.item(selected[0], 'tags')
            if item_values:
                exam_id = item_values[0]
                self.history_manager.delete_exam(exam_id)
                self.refresh_history()
    
    def run(self):
        """Ejecuta la aplicación."""
        self.root.mainloop()


def main():
    """Punto de entrada principal."""
    app = ExamGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()
