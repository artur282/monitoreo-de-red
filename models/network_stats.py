import time
from typing import Dict, Optional, Tuple

class NetworkStats:
    def __init__(self):
        self.start_time = 0
        self.total_bytes = 0
        self.packet_count = 0

    def get_elapsed_time(self) -> str:
        """Obtiene el tiempo transcurrido desde el inicio de la captura."""
        if self.start_time == 0:
            return "00:00:00"
        elapsed = time.time() - self.start_time
        return time.strftime("%H:%M:%S", time.gmtime(elapsed))

    def format_size(self, size_bytes: int) -> str:
        """Formatea el tamaño en bytes a una forma legible."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes / (1024**2):.1f} MB"
        else:
            return f"{size_bytes / (1024**3):.1f} GB"

    def calculate_other_protocols(self, protocol_counts: Dict[str, int]) -> int:
        """Calcula la cantidad de paquetes de protocolos no estándar."""
        standard_protocols = ['TCP', 'UDP', 'ICMP', 'ARP']
        standard_count = sum(protocol_counts.get(proto, 0) for proto in standard_protocols)
        return max(0, self.packet_count - standard_count)

    def update_stats(self, bytes_count: int) -> None:
        """Actualiza las estadísticas con nuevos datos."""
        self.total_bytes += bytes_count
        self.packet_count += 1

    def reset_stats(self) -> None:
        """Reinicia todas las estadísticas."""
        self.start_time = 0
        self.total_bytes = 0
        self.packet_count = 0

    def start_counting(self) -> None:
        """Inicia el conteo de tiempo."""
        self.start_time = time.time()