import threading
import time
from typing import Optional
from models.packet_model import PacketModel
from models.network_stats import NetworkStats
from views.main_view import MainView
from scapy.all import sniff  # type: ignore
import csv
from fpdf import FPDF  # type: ignore

class NetworkController:
    def __init__(self, view: MainView):
        self.view = view
        self.model = PacketModel()
        self.stats = NetworkStats()
        self.capture_thread: Optional[threading.Thread] = None
        self.is_capturing = False
        
        # Configurar callbacks de la vista
        self.view.set_start_capture_callback(self.start_capture)
        self.view.set_stop_capture_callback(self.stop_capture)
        self.view.set_clear_results_callback(self.clear_results)
        
        # Configurar eventos del menú
        self._setup_menu_callbacks()
        
        # Iniciar actualización de UI
        self._schedule_ui_update()

    def _setup_menu_callbacks(self):
        """Configura los callbacks del menú de reportes."""
        self.view.report_menu.add_command(
            label="Generar Reporte PDF",
            command=self.generate_pdf_report,
            state="normal" if FPDF else "disabled"
        )
        self.view.report_menu.add_command(
            label="Generar Reporte CSV",
            command=self.generate_csv_report
        )

    def start_capture(self):
        """Inicia la captura de paquetes."""
        if not self.is_capturing:
            self.is_capturing = True
            self.view.update_capture_state(True)
            self.stats.start_counting()
            
            # Iniciar hilo de captura
            filtro = self.view.get_filter()
            self.capture_thread = threading.Thread(
                target=self._capture_packets,
                args=(filtro,),
                daemon=True
            )
            self.capture_thread.start()

    def stop_capture(self):
        """Detiene la captura de paquetes."""
        if self.is_capturing:
            self.is_capturing = False
            self.model.stop_capture()
            self.view.update_capture_state(False)

    def clear_results(self):
        """Limpia todos los resultados y reinicia las estadísticas."""
        if not self.is_capturing:
            self.model.clear_data()
            self.stats.reset_stats()
            self.view.packet_tree.delete(*self.view.packet_tree.get_children())
            self.view.ip_tree.delete(*self.view.ip_tree.get_children())
            self._update_stats_display()
        else:
            self.view.show_warning("Limpiar", "Detén la captura antes de limpiar.")

    def _capture_packets(self, filtro: str):
        """Función ejecutada en el hilo de captura."""
        try:
            # Iniciar la captura directamente desde aquí
            sniff(
                filter=filtro if filtro else None,
                prn=self._process_packet,
                stop_filter=lambda x: not self.is_capturing,
                store=False
            )
        except Exception as e:
            self.view.after(0, lambda: self.view.show_error(
                "Error de Captura",
                f"Error al capturar paquetes: {str(e)}"
            ))
            self.is_capturing = False
            self.view.after(0, lambda: self.view.update_capture_state(False))

    def _process_packet(self, packet):
        """Procesa un paquete capturado y lo muestra en la vista."""
        try:
            # Procesar el paquete en el modelo
            self.model.process_packet(packet)
            
            # Procesar todos los paquetes pendientes en la cola
            while not self.model.packet_queue.empty():
                try:
                    packet_info = self.model.packet_queue.get_nowait()
                    if packet_info and len(packet_info) == 7:
                        # Asegurar que la actualización de UI se haga en el hilo principal
                        self.view.after(1, self.view.add_packet_to_tree, packet_info)
                except Exception as e:
                    print(f"Error procesando paquete de la cola: {e}")
                    break
                    
        except Exception as e:
            print(f"Error en _process_packet: {e}")
            
    def _update_stats_display(self):
        """Actualiza las etiquetas de estadísticas en la vista."""
        if self.is_capturing:
            self.view.update_stats_label('Tiempo', f"Tiempo: {self.stats.get_elapsed_time()}")
        
        self.view.update_stats_label('Paquetes', f"Paquetes: {self.model.packet_count}")
        self.view.update_stats_label('Trafico', f"Tráfico: {self.stats.format_size(self.model.total_bytes)}")
        self.view.update_stats_label('TCP', f"TCP: {self.model.protocol_counts.get('TCP', 0)}")
        self.view.update_stats_label('UDP', f"UDP: {self.model.protocol_counts.get('UDP', 0)}")
        
        otros = self.stats.calculate_other_protocols(self.model.protocol_counts)
        self.view.update_stats_label('Otros', f"Otros: {otros}")

    def _schedule_ui_update(self):
        """Programa la siguiente actualización de la interfaz."""
        if not self.view.winfo_exists():
            return
            
        try:
            # Actualizar estadísticas
            self._update_stats_display()
            
            # Actualizar lista de IPs (solo las IPs válidas)
            ip_counts = {ip: count for ip, count in self.model.ip_counts.items() 
                       if ip != "N/A" and ip != ""}
            self.view.update_ip_list(ip_counts)
            
            # Procesar cualquier paquete pendiente
            while not self.model.packet_queue.empty():
                try:
                    packet_info = self.model.packet_queue.get_nowait()
                    if packet_info and len(packet_info) == 7:
                        self.view.add_packet_to_tree(packet_info)
                except Exception as e:
                    print(f"Error procesando paquete pendiente: {e}")
                    break
                    
        except Exception as e:
            print(f"Error actualizando UI: {e}")
        finally:
            if self.view.winfo_exists():
                self.view.after(50, self._schedule_ui_update)  # Actualizar más frecuentemente

    def generate_pdf_report(self):
        """Genera un reporte en PDF de las estadísticas actuales."""
        if self.is_capturing:
            self.view.show_warning("Reporte PDF", "Detén la captura antes de generar el reporte.")
            return
        if not self.model.packet_count:
            self.view.show_info("Reporte PDF", "No hay datos capturados para generar el reporte.")
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Reporte de Monitoreo de Red', ln=True, align='C')
            pdf.ln(10)

            # Estadísticas generales
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Resumen Estadístico', ln=True)
            pdf.set_font('Arial', '', 10)
            
            stats = [
                f"Tiempo: {self.stats.get_elapsed_time()}",
                f"Paquetes Totales: {self.model.packet_count}",
                f"Tráfico Total: {self.stats.format_size(self.model.total_bytes)}"
            ]
            
            for stat in stats:
                pdf.cell(0, 7, stat, ln=True)
            
            # Protocolos
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Distribución por Protocolo', ln=True)
            pdf.set_font('Arial', '', 10)
            
            for proto, count in sorted(
                self.model.protocol_counts.items(),
                key=lambda x: x[1],
                reverse=True
            ):
                if count > 0:
                    pdf.cell(0, 7, f"- {proto}: {count}", ln=True)

            # Top IPs
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Top 20 Direcciones IP', ln=True)
            pdf.set_font('Arial', '', 10)
            
            for i, (ip, count) in enumerate(
                sorted(self.model.ip_counts.items(),
                key=lambda x: x[1],
                reverse=True)[:20]
            ):
                pdf.cell(0, 7, f"- {ip}: {count} paquetes", ln=True)

            filename = 'reporte_monitoreo.pdf'
            pdf.output(filename)
            self.view.show_info(
                "Reporte Generado",
                f"El reporte '{filename}' ha sido generado exitosamente."
            )

        except Exception as e:
            self.view.show_error(
                "Error Reporte PDF",
                f"No se pudo generar el reporte PDF:\n{e}"
            )

    def generate_csv_report(self):
        """Genera un reporte CSV con los datos de paquetes capturados."""
        if self.is_capturing:
            self.view.show_warning(
                "Reporte CSV",
                "Detén la captura antes de generar el reporte."
            )
            return
            
        if not self.view.packet_tree.get_children():
            self.view.show_info(
                "Reporte CSV",
                "No hay paquetes capturados para exportar."
            )
            return

        try:
            filename = 'reporte_paquetes.csv'
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(self.view.packet_tree['columns'])
                
                for item_id in self.view.packet_tree.get_children():
                    writer.writerow(self.view.packet_tree.item(item_id)['values'])
                    
            self.view.show_info(
                "Reporte Generado",
                f"El reporte '{filename}' ha sido generado exitosamente."
            )

        except Exception as e:
            self.view.show_error(
                "Error Reporte CSV",
                f"No se pudo generar el reporte CSV:\n{e}"
            )