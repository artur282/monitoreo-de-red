from scapy.all import sniff, Ether, ARP  # type: ignore
from scapy.layers.inet import IP, TCP, UDP, ICMP  # type: ignore
import time
from collections import defaultdict
import queue
from typing import Dict, Tuple, Optional

class PacketModel:
    def __init__(self):
        self.packet_queue = queue.Queue()
        self.protocol_counts = defaultdict(int)
        self.ip_counts = defaultdict(int)
        self.total_bytes = 0
        self.packet_count = 0
        self.start_time = 0
        self.capturing = False

    def start_capture(self, filtro: Optional[str] = None) -> None:
        """Inicia la captura de paquetes."""
        self.capturing = True
        self.start_time = time.time()
        
        try:
            # Iniciar la captura en modo asíncrono
            sniff(
                filter=filtro if filtro else None,
                prn=self.process_packet,
                store=False,
                stop_filter=lambda x: not self.capturing,
                count=0
            )
        except Exception as e:
            print(f"Error al iniciar la captura: {e}")
            self.capturing = False

    def stop_capture(self) -> None:
        """Detiene la captura de paquetes."""
        self.capturing = False

    def clear_data(self) -> None:
        """Limpia todos los datos capturados."""
        self.protocol_counts.clear()
        self.ip_counts.clear()
        self.total_bytes = 0
        self.packet_count = 0
        self.start_time = 0
        self.packet_queue = queue.Queue()

    def process_packet(self, packet) -> None:
        """Procesa un paquete capturado."""
        try:
            timestamp = time.strftime("%H:%M:%S", time.localtime(packet.time))
            size = len(packet)
            protocol = "Desconocido"
            ip_src = "N/A"
            ip_dst = "N/A"
            port_src = "N/A"
            port_dst = "N/A"

            # Identificar el tipo de paquete y protocolo
            if ARP in packet:
                protocol = "ARP"
                arp_layer = packet[ARP]
                ip_src = arp_layer.psrc
                ip_dst = arp_layer.pdst
                port_src = "ARP"
                port_dst = "ARP"
                
            elif IP in packet:
                ip_layer = packet[IP]
                ip_src = ip_layer.src
                ip_dst = ip_layer.dst
                
                if TCP in packet:
                    tcp_layer = packet[TCP]
                    protocol = "TCP"
                    port_src = str(tcp_layer.sport)
                    port_dst = str(tcp_layer.dport)
                    # Identificar protocolos comunes por puerto
                    if tcp_layer.dport == 80 or tcp_layer.sport == 80:
                        protocol = "HTTP"
                    elif tcp_layer.dport == 443 or tcp_layer.sport == 443:
                        protocol = "HTTPS"
                    elif tcp_layer.dport == 53 or tcp_layer.sport == 53:
                        protocol = "DNS"
                        
                elif UDP in packet:
                    udp_layer = packet[UDP]
                    protocol = "UDP"
                    port_src = str(udp_layer.sport)
                    port_dst = str(udp_layer.dport)
                    # Identificar protocolos UDP comunes
                    if udp_layer.dport == 53 or udp_layer.sport == 53:
                        protocol = "DNS"
                    elif udp_layer.dport == 67 or udp_layer.dport == 68:
                        protocol = "DHCP"
                        
                elif ICMP in packet:
                    protocol = "ICMP"
                    port_src = "ICMP"
                    port_dst = "ICMP"
                    
            elif IPv6 in packet: # type: ignore
                protocol = "IPv6"
                ipv6_layer = packet[IPv6] # type: ignore
                ip_src = ipv6_layer.src
                ip_dst = ipv6_layer.dst

            # Actualizar contadores
            self.protocol_counts[protocol] = self.protocol_counts.get(protocol, 0) + 1
            if ip_src != "N/A":
                self.ip_counts[ip_src] = self.ip_counts.get(ip_src, 0) + 1
            if ip_dst != "N/A":
                self.ip_counts[ip_dst] = self.ip_counts.get(ip_dst, 0) + 1

            self.total_bytes += size
            self.packet_count += 1

            # Crear la tupla de información del paquete
            packet_info = (timestamp, protocol, str(ip_src), str(ip_dst),
                         str(port_src), str(port_dst), str(size))
            
            try:
                self.packet_queue.put_nowait(packet_info)
            except Exception as e:
                print(f"Error añadiendo paquete a la cola: {e}")

        except Exception as e:
            print(f"Error procesando paquete: {e}")
            # Asegurar que los contadores básicos se actualicen incluso si hay error
            self.total_bytes += len(packet)
            self.packet_count += 1

    def _get_protocol_name(self, proto_num: int) -> str:
        """Obtiene el nombre del protocolo a partir de su número."""
        protocols = {
            1: 'ICMP', 2: 'IGMP', 4: 'IPv4', 6: 'TCP', 8: 'EGP',
            17: 'UDP', 41: 'IPv6', 47: 'GRE', 50: 'ESP', 51: 'AH',
            88: 'EIGRP', 89: 'OSPF', 132: 'SCTP'
        }
        return protocols.get(proto_num, f'IP_{proto_num}')