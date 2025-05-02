import tkinter as tk
from tkinter import ttk, messagebox
from .styles import StyleConfig
from typing import Callable, Dict, Any

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitor de Red Moderno - Tema Claro")
        self.geometry("1350x800")
        
        # Configurar estilos
        self.default_font, self.large_font = StyleConfig.configure_styles(self)
        
        # Variables de la interfaz
        self.filter_var = tk.StringVar(value="tcp or udp")
        self.stats_labels: Dict[str, ttk.Label] = {}
        self._create_widgets()

    def _create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        self._create_menu()
        
        # Frame principal
        main_frame = ttk.Frame(self, padding="15 15 15 15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # PanedWindow principal
        main_paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo
        self._create_left_panel(main_paned)
        
        # Panel derecho
        self._create_right_panel(main_paned)

    def _create_menu(self):
        """Crea la barra de menú."""
        self.menu_bar = tk.Menu(self)
        
        # Menú Archivo
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Salir", command=self.quit)
        self.menu_bar.add_cascade(label="Archivo", menu=file_menu)
        
        # Menú Reportes
        self.report_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Reportes", menu=self.report_menu)
        
        # Menú Ayuda
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=lambda: None)
        self.menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        
        self.config(menu=self.menu_bar)

    def _create_left_panel(self, parent):
        """Crea el panel izquierdo con los controles y la lista de paquetes."""
        left_container = ttk.Frame(parent, padding=(0, 0, 10, 0))
        parent.add(left_container, weight=3)

        # Controles superiores
        control_frame = ttk.Frame(left_container)
        control_frame.pack(fill=tk.X, pady=(0, 15))

        # Botones de control
        self.btn_iniciar = ttk.Button(
            control_frame,
            text="▶ Iniciar Captura",
            style="Accent.TButton",
            width=18
        )
        self.btn_iniciar.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_detener = ttk.Button(
            control_frame,
            text="■ Detener Captura",
            style="Danger.TButton",
            width=18,
            state=tk.DISABLED
        )
        self.btn_detener.pack(side=tk.LEFT, padx=8)

        self.btn_limpiar = ttk.Button(
            control_frame,
            text="🧹 Limpiar",
            width=12
        )
        self.btn_limpiar.pack(side=tk.LEFT, padx=8)

        # Filtro
        filter_frame = ttk.Frame(control_frame)
        filter_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        ttk.Label(filter_frame, text="Filtro (BPF):", anchor=tk.W).pack(side=tk.LEFT, padx=(0, 5))

        filter_options = ["tcp or udp", "tcp", "udp", "icmp", "arp", "ip", "port 80", "port 443", ""]
        self.filter_menu = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=filter_options,
            state="readonly",
            width=15
        )
        self.filter_menu.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # TreeView de paquetes
        self._create_packet_tree(left_container)
        
        # Panel de estadísticas
        self._create_stats_panel(left_container)

    def _create_packet_tree(self, parent):
        """Crea el TreeView para la lista de paquetes."""
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.packet_tree = ttk.Treeview(
            tree_frame,
            columns=('Hora', 'Protocolo', 'Origen', 'Destino', 'Puerto Origen', 'Puerto Destino', 'Tamaño'),
            show='headings'
        )

        # Configurar columnas
        columns = [
            ('Hora', 80, 70, tk.W),
            ('Protocolo', 70, 60, tk.W),
            ('Origen', 180, 120, tk.W),
            ('Destino', 180, 120, tk.W),
            ('Puerto Origen', 90, 70, tk.CENTER),
            ('Puerto Destino', 90, 70, tk.CENTER),
            ('Tamaño', 70, 60, tk.E)
        ]

        for col, width, minwidth, anchor in columns:
            self.packet_tree.heading(col, text=col, anchor=anchor)
            self.packet_tree.column(col, width=width, minwidth=minwidth, stretch=tk.YES, anchor=anchor)

        # Scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.packet_tree.yview)
        scrollbar_x = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.packet_tree.xview)
        self.packet_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.packet_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_x.pack(fill=tk.X, side=tk.BOTTOM, pady=(5,0))

    def _create_stats_panel(self, parent):
        """Crea el panel de estadísticas."""
        stats_frame = ttk.Frame(parent, padding=(10, 5))
        stats_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.stats_labels = {
            'Tiempo': ttk.Label(stats_frame, text="Tiempo: 00:00:00", anchor=tk.W),
            'Paquetes': ttk.Label(stats_frame, text="Paquetes: 0", anchor=tk.W),
            'Trafico': ttk.Label(stats_frame, text="Tráfico: 0 B", anchor=tk.W),
            'TCP': ttk.Label(stats_frame, text="TCP: 0", anchor=tk.W),
            'UDP': ttk.Label(stats_frame, text="UDP: 0", anchor=tk.W),
            'Otros': ttk.Label(stats_frame, text="Otros: 0", anchor=tk.W)
        }

        num_cols = 3
        stats_frame.columnconfigure(list(range(num_cols)), weight=1)
        for i, label in enumerate(self.stats_labels.values()):
            label.grid(row=i // num_cols, column=i % num_cols, padx=5, pady=2, sticky="ew")

    def _create_right_panel(self, parent):
        """Crea el panel derecho con la lista de IPs."""
        right_container = ttk.Frame(parent, padding=(10, 0, 0, 0))
        parent.add(right_container, weight=1)

        # Título
        ttk.Label(
            right_container,
            text="Direcciones IP Detectadas",
            font=self.large_font,
            anchor=tk.CENTER
        ).pack(fill=tk.X, pady=(0, 10))

        # TreeView de IPs
        ip_tree_frame = ttk.Frame(right_container)
        ip_tree_frame.pack(fill=tk.BOTH, expand=True)

        self.ip_tree = ttk.Treeview(
            ip_tree_frame,
            columns=('IP', 'Cantidad'),
            show='headings'
        )
        
        self.ip_tree.heading('IP', text='Dirección IP', anchor=tk.W)
        self.ip_tree.heading('Cantidad', text='Paquetes', anchor=tk.E)
        self.ip_tree.column('IP', width=180, minwidth=140, stretch=tk.YES, anchor=tk.W)
        self.ip_tree.column('Cantidad', width=80, minwidth=70, stretch=tk.NO, anchor=tk.E)

        scrollbar_ip = ttk.Scrollbar(ip_tree_frame, orient=tk.VERTICAL, command=self.ip_tree.yview)
        self.ip_tree.configure(yscroll=scrollbar_ip.set)

        scrollbar_ip.pack(side=tk.RIGHT, fill=tk.Y)
        self.ip_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def set_start_capture_callback(self, callback: Callable[[], None]):
        """Configura el callback para iniciar la captura."""
        self.btn_iniciar.configure(command=callback)

    def set_stop_capture_callback(self, callback: Callable[[], None]):
        """Configura el callback para detener la captura."""
        self.btn_detener.configure(command=callback)

    def set_clear_results_callback(self, callback: Callable[[], None]):
        """Configura el callback para limpiar resultados."""
        self.btn_limpiar.configure(command=callback)

    def update_stats_label(self, label_key: str, text: str):
        """Actualiza el texto de una etiqueta de estadísticas."""
        if label_key in self.stats_labels:
            self.stats_labels[label_key].config(text=text)

    def update_capture_state(self, is_capturing: bool):
        """Actualiza el estado de los botones según el estado de captura."""
        self.btn_iniciar.config(state=tk.DISABLED if is_capturing else tk.NORMAL)
        self.btn_detener.config(state=tk.NORMAL if is_capturing else tk.DISABLED)
        self.filter_menu.config(state=tk.DISABLED if is_capturing else "readonly")
        self.btn_limpiar.config(state=tk.DISABLED if is_capturing else tk.NORMAL)

    def show_error(self, title: str, message: str):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)

    def show_info(self, title: str, message: str):
        """Muestra un mensaje informativo."""
        messagebox.showinfo(title, message)

    def get_filter(self) -> str:
        """Obtiene el filtro actual."""
        return self.filter_var.get().strip()

    def add_packet_to_tree(self, packet_info):
        """Añade un paquete al árbol de paquetes."""
        try:
            # Asegurar que estamos en el hilo principal
            if not isinstance(packet_info, tuple) or len(packet_info) != 7:
                return
                
            timestamp, protocol, ip_src, ip_dst, port_src, port_dst, size = packet_info
            
            # Insertar al inicio del árbol para mejor rendimiento
            self.packet_tree.insert(
                '',
                0,
                values=(timestamp, protocol, ip_src, ip_dst, port_src, port_dst, size)
            )
            
            # Mantener un límite de elementos mostrados para evitar problemas de rendimiento
            if len(self.packet_tree.get_children()) > 1000:
                # Eliminar el último elemento
                last_item = self.packet_tree.get_children()[-1]
                self.packet_tree.delete(last_item)
                
            # Asegurar que el scroll siga los nuevos elementos
            self.packet_tree.yview_moveto(0)
            
        except Exception as e:
            print(f"Error añadiendo paquete al árbol: {e}")

    def update_ip_list(self, ip_counts: Dict[str, int]):
        """Actualiza la lista de IPs con sus contadores."""
        try:
            # Guardar la selección actual
            current_selection = self.ip_tree.selection()
            current_focus = self.ip_tree.focus()

            # Limpiar la lista actual
            self.ip_tree.delete(*self.ip_tree.get_children())
            
            # Insertar las IPs ordenadas por cantidad de paquetes
            for ip, count in sorted(
                ip_counts.items(),
                key=lambda x: (-x[1], x[0])  # Ordenar por count (descendente) y luego por IP
            ):
                if ip and ip != "N/A":  # Solo mostrar IPs válidas
                    self.ip_tree.insert('', tk.END, values=(ip, count), iid=ip)

            # Restaurar la selección si los elementos aún existen
            if current_focus and self.ip_tree.exists(current_focus):
                self.ip_tree.focus(current_focus)
            if current_selection:
                valid_selection = [item for item in current_selection if self.ip_tree.exists(item)]
                if valid_selection:
                    self.ip_tree.selection_set(valid_selection)
                    
        except Exception as e:
            print(f"Error actualizando lista de IPs: {e}")