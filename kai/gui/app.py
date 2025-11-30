"""Desktop GUI for Kai settings."""

import tkinter as tk
from tkinter import ttk, messagebox
import ollama
from kai.core.config import Config


class KaiSettingsApp:
    """Kai settings GUI application."""
    
    def __init__(self):
        self.config = Config()
        self.root = tk.Tk()
        self.root.title("Kai Settings")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.ollama_status = ""
        
        self.setup_ui()
        self.load_settings()
        self.load_ollama_models()
        
        # Update status label after loading models
        self.status_label.config(text=self.ollama_status)
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="⚙️ Kai Settings", font=('Arial', 20, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Language
        ttk.Label(main_frame, text="Language:", font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.language_var = tk.StringVar()
        language_combo = ttk.Combobox(main_frame, textvariable=self.language_var, width=30)
        language_combo['values'] = (
            'en-US - English (US)',
            'en-GB - English (UK)',
            'es-ES - Spanish',
            'fr-FR - French',
            'de-DE - German',
            'it-IT - Italian',
            'pt-BR - Portuguese (Brazil)',
            'ja-JP - Japanese',
            'zh-CN - Chinese (Simplified)'
        )
        language_combo.grid(row=1, column=1, pady=10, padx=(10, 0))
        
        # LLM Model
        ttk.Label(main_frame, text="LLM Model:", font=('Arial', 11)).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.llm_var = tk.StringVar()
        self.llm_combo = ttk.Combobox(main_frame, textvariable=self.llm_var, width=30)
        self.llm_combo.grid(row=2, column=1, pady=10, padx=(10, 0))
        
        # Ollama status label
        self.status_label = ttk.Label(main_frame, text="", font=('Arial', 9), foreground='gray')
        self.status_label.grid(row=2, column=1, sticky=tk.E, padx=(10, 0), pady=(35, 0))
        
        # TTS Model
        ttk.Label(main_frame, text="TTS Voice:", font=('Arial', 11)).grid(row=3, column=0, sticky=tk.W, pady=10)
        self.tts_var = tk.StringVar()
        tts_entry = ttk.Entry(main_frame, textvariable=self.tts_var, width=32)
        tts_entry.grid(row=3, column=1, pady=10, padx=(10, 0))
        
        # Save button
        save_btn = ttk.Button(main_frame, text="Save Settings", command=self.save_settings)
        save_btn.grid(row=4, column=0, columnspan=2, pady=(30, 0), sticky=(tk.W, tk.E))
        
    def load_settings(self):
        """Load current settings."""
        language = self.config.get('core.language', 'en-US')
        self.language_var.set(f"{language} - {self.get_language_name(language)}")
        
        self.llm_var.set(self.config.get('models.llm', 'llama3.2:3b'))
        self.tts_var.set(self.config.get('models.tts', 'piper-en_US-lessac-medium'))
        
    def get_language_name(self, code):
        """Get language name from code."""
        names = {
            'en-US': 'English (US)',
            'en-GB': 'English (UK)',
            'es-ES': 'Spanish',
            'fr-FR': 'French',
            'de-DE': 'German',
            'it-IT': 'Italian',
            'pt-BR': 'Portuguese (Brazil)',
            'ja-JP': 'Japanese',
            'zh-CN': 'Chinese (Simplified)'
        }
        return names.get(code, 'English (US)')
        
    def load_ollama_models(self):
        """Load available Ollama models."""
        # Default popular models
        default_models = [
            'llama3.2:3b',
            'llama3.2:1b',
            'llama3.1:8b',
            'llama3:8b',
            'mistral:7b',
            'phi3:mini',
            'gemma2:2b',
            'qwen2.5:7b'
        ]
        
        try:
            client = ollama.Client()
            models = client.list()
            model_names = [m['name'] for m in models.get('models', [])]
            
            if model_names:
                # Combine installed models with defaults (remove duplicates)
                all_models = list(dict.fromkeys(model_names + default_models))
                self.llm_combo['values'] = all_models
                # Add status indicator
                self.ollama_status = "✓ Connected to Ollama"
            else:
                # No models installed, show defaults
                self.llm_combo['values'] = default_models
                self.ollama_status = "⚠ No models installed"
        except Exception as e:
            # Ollama not running or error, still allow manual entry
            self.llm_combo['values'] = default_models
            self.ollama_status = "⚠ Ollama not connected"
            # Don't show popup - just set status
            print(f"Note: Could not connect to Ollama - {str(e)}")
            
    def save_settings(self):
        """Save settings to config."""
        try:
            # Extract language code
            language = self.language_var.get().split(' - ')[0]
            self.config.set('core.language', language)
            
            self.config.set('models.llm', self.llm_var.get())
            self.config.set('models.tts', self.tts_var.get())
            
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            
    def run(self):
        """Run the application."""
        self.root.mainloop()


def launch_gui():
    """Launch the GUI application."""
    app = KaiSettingsApp()
    app.run()
