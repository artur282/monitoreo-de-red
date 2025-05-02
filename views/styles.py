import sys
import tkinter as tk
from tkinter import ttk, font as tkfont

class StyleConfig:
    # Paleta de Colores (Tema Claro)
    BG_COLOR_LIGHT = "#f0f0f0"
    FG_COLOR_LIGHT = "#333333"
    ACCENT_COLOR_LIGHT = "#0078d4"
    BUTTON_COLOR_LIGHT = "#e1e1e1"
    BUTTON_FG_LIGHT = FG_COLOR_LIGHT
    LIST_BG_LIGHT = "#ffffff"
    HEADER_BG_LIGHT = "#e5e5e5"
    SELECT_BG_LIGHT = ACCENT_COLOR_LIGHT
    SELECT_FG_LIGHT = "#ffffff"
    DANGER_COLOR_LIGHT = "#d32f2f"
    DISABLED_FG_LIGHT = "#aaaaaa"
    BORDER_COLOR_LIGHT = "#cccccc"

    # Configuración de Fuentes
    DEFAULT_FONT = "Segoe UI" if sys.platform == "win32" else "Helvetica"
    FONT_SIZE_NORMAL = 10
    FONT_SIZE_LARGE = 12

    @classmethod
    def configure_styles(cls, root):
        """Configura los estilos globales de la aplicación."""
        style = ttk.Style(root)
        
        # Configurar tema base
        try:
            if sys.platform == "win32":
                style.theme_use('vista')
            elif sys.platform == "darwin":
                style.theme_use('aqua')
        except tk.TclError:
            style.theme_use('default')

        # Configurar fuentes globales
        default_font = tkfont.Font(family=cls.DEFAULT_FONT, size=cls.FONT_SIZE_NORMAL)
        large_font = tkfont.Font(family=cls.DEFAULT_FONT, size=cls.FONT_SIZE_LARGE, weight="bold")
        
        # Aplicar estilos base
        cls._configure_base_styles(style)
        cls._configure_button_styles(style)
        cls._configure_treeview_styles(style)
        cls._configure_combobox_styles(style)
        cls._configure_scrollbar_styles(style)
        
        return default_font, large_font

    @classmethod
    def _configure_base_styles(cls, style):
        """Configura los estilos base."""
        style.configure('.',
            background=cls.BG_COLOR_LIGHT,
            foreground=cls.FG_COLOR_LIGHT,
            fieldbackground=cls.LIST_BG_LIGHT,
            borderwidth=0,
            focuscolor=cls.ACCENT_COLOR_LIGHT)

        style.configure('TFrame', background=cls.BG_COLOR_LIGHT)
        style.configure('TLabel', background=cls.BG_COLOR_LIGHT, foreground=cls.FG_COLOR_LIGHT, padding=(5, 5))
        style.configure('TPanedwindow', background=cls.BG_COLOR_LIGHT)

    @classmethod
    def _configure_button_styles(cls, style):
        """Configura los estilos de los botones."""
        # Estilo de botón normal
        style.configure('TButton',
            background=cls.BUTTON_COLOR_LIGHT,
            foreground=cls.BUTTON_FG_LIGHT,
            padding=(10, 6),
            borderwidth=1,
            relief=tk.FLAT,
            anchor=tk.CENTER)

        # Estilo de botón primario
        style.configure('Accent.TButton',
            background=cls.ACCENT_COLOR_LIGHT,
            foreground=cls.SELECT_FG_LIGHT)

        # Estilo de botón de peligro
        style.configure('Danger.TButton',
            background=cls.DANGER_COLOR_LIGHT,
            foreground=cls.SELECT_FG_LIGHT)

    @classmethod
    def _configure_treeview_styles(cls, style):
        """Configura los estilos del Treeview."""
        style.configure('Treeview',
            background=cls.LIST_BG_LIGHT,
            foreground=cls.FG_COLOR_LIGHT,
            fieldbackground=cls.LIST_BG_LIGHT,
            rowheight=26)

        style.configure('Treeview.Heading',
            background=cls.HEADER_BG_LIGHT,
            foreground=cls.FG_COLOR_LIGHT,
            padding=(8, 6))

    @classmethod
    def _configure_combobox_styles(cls, style):
        """Configura los estilos del Combobox."""
        style.configure('TCombobox',
            padding=5,
            fieldbackground=cls.LIST_BG_LIGHT,
            background=cls.BUTTON_COLOR_LIGHT,
            arrowcolor=cls.FG_COLOR_LIGHT,
            borderwidth=1)

    @classmethod
    def _configure_scrollbar_styles(cls, style):
        """Configura los estilos de las barras de desplazamiento."""
        for orientation in ['Vertical', 'Horizontal']:
            style.configure(f'{orientation}.TScrollbar',
                background=cls.BUTTON_COLOR_LIGHT,
                troughcolor=cls.BG_COLOR_LIGHT,
                borderwidth=0,
                arrowsize=14,
                arrowcolor=cls.FG_COLOR_LIGHT,
                relief=tk.FLAT)