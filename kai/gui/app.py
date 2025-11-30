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
        
        self.setup_ui()
        self.load_settings()
        self.load_ollama_models()
        
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
        language_combo = ttk.Combobox(main_frame, textvariable=self.language_var, state='readonly', width=30)
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
        self.llm_combo = ttk.Combobox(main_frame, textvariable=self.llm_var, state='readonly', width=30)
        self.llm_combo.grid(row=2, column=1, pady=10, padx=(10, 0))
        
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
        try:
            client = ollama.Client()
            models = client.list()
            model_names = [m['name'] for m in models.get('models', [])]
            
            if model_names:
                self.llm_combo['values'] = model_names
            else:
                self.llm_combo['values'] = ['No models found']
                messagebox.showwarning("Warning", "No Ollama models found. Install models with: ollama pull llama3.2")
        except Exception as e:
            self.llm_combo['values'] = ['Error loading models']
            messagebox.showerror("Error", f"Failed to connect to Ollama: {str(e)}")
            
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
