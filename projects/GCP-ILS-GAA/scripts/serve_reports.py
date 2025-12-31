#!/usr/bin/env python3
"""
Servidor HTTP simple para los reportes
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path
import time
import os

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🌐 Servidor iniciado en http://localhost:{PORT}")
        print(f"📊 Abriendo validation_summary.html...")
        
        # Abrir en navegador
        time.sleep(1)
        webbrowser.open(f'http://localhost:{PORT}/validation_summary.html')
        
        print(f"✅ Presiona Ctrl+C para detener el servidor")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Servidor detenido")
