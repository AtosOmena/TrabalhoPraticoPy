
import tkinter as tk

class BaseView(tk.Frame):
    """Classe base para todas as views"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg='#2C3E50')
    
    def show(self):
        """Exibe a view"""
        self.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        """Oculta a view"""
        self.pack_forget()
    
    def clear(self):
        """Limpa todos os widgets"""
        for widget in self.winfo_children():
            widget.destroy()
