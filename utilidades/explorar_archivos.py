import os
from datetime import datetime
from config import RUTA_COMPARTIDA

def obtener_listado_archivos():
    archivos = []
    for nombre in os.listdir(RUTA_COMPARTIDA):
        ruta = os.path.join(RUTA_COMPARTIDA, nombre)
        if os.path.isfile(ruta):
            stat = os.stat(ruta)
            archivos.append({
                "nombre": nombre,
                "fecha": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "tipo": os.path.splitext(nombre)[1].replace(".", "").upper(),
                "tamano": f"{stat.st_size / 1024:.1f} KB"
            })
    return archivos
