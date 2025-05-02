# 🌐 Monitor de Red Moderno

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Scapy](https://img.shields.io/badge/scapy-latest-green.svg)](https://scapy.net/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Una aplicación moderna y eficiente para el monitoreo de tráfico de red en tiempo real, con interfaz gráfica intuitiva y capacidades de análisis detallado.

![Banner del Proyecto]

> 🚀 Visualiza y analiza el tráfico de tu red con una interfaz moderna y funcional

## ✨ Características Principales

- 📊 **Monitoreo en Tiempo Real**

  - Captura y visualización de paquetes en tiempo real
  - Estadísticas actualizadas dinámicamente
  - Filtrado de paquetes mediante expresiones BPF

- 🔍 **Análisis Detallado**

  - Identificación automática de protocolos (TCP, UDP, HTTP, HTTPS, DNS, etc.)
  - Seguimiento de direcciones IP y puertos
  - Estadísticas de tráfico y conteo de paquetes

- 📈 **Reportes y Exportación**

  - Generación de reportes en PDF
  - Exportación de datos a CSV
  - Estadísticas detalladas por protocolo

- 🎨 **Interfaz Moderna**
  - Diseño limpio y profesional
  - Tema claro optimizado
  - Tablas interactivas y ordenables

## 🚀 Inicio Rápido

### Requisitos Previos

```bash
# Python 3.x
# Privilegios de administrador/root para la captura de paquetes
```

### Instalación

1. Clona el repositorio:

```bash
git clone [URL del repositorio]
cd monitoreo-de-red
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

### Ejecución

En sistemas Linux/Unix:

```bash
sudo python3 monitor_red.py
```

En Windows (como administrador):

```bash
python monitor_red.py
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **Tkinter**: Framework para la interfaz gráfica
- **Scapy**: Biblioteca para captura y análisis de paquetes
- **FPDF**: Generación de reportes PDF
- **CSV**: Exportación de datos

## 📖 Estructura del Proyecto

```
monitoreo-de-red/
├── monitor_red.py         # Punto de entrada principal
├── controllers/
│   └── network_controller.py  # Controlador principal
├── models/
│   ├── network_stats.py      # Modelo de estadísticas
│   └── packet_model.py       # Modelo de paquetes
├── views/
│   ├── main_view.py          # Vista principal
│   └── styles.py             # Configuración de estilos
└── readme.md                 # Documentación
```

## 🔧 Configuración

La aplicación permite configurar:

- Filtros de captura personalizados (formato BPF)
- Límite de paquetes mostrados
- Formato de visualización de datos

## 📊 Características Detalladas

### Captura de Paquetes

- Captura en tiempo real de todo el tráfico de red
- Soporte para múltiples protocolos
- Filtrado mediante expresiones BPF
- Modo promiscuo para captura completa

### Análisis de Tráfico

- Identificación automática de protocolos
- Estadísticas por protocolo
- Seguimiento de direcciones IP
- Análisis de puertos

### Reportes

- Exportación a PDF con estadísticas detalladas
- Reportes en CSV para análisis posterior
- Resúmenes de tráfico por protocolo

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

📌 _Desarrollado con ❤️_

