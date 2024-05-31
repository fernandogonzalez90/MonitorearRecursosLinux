import os
import platform
from fastapi import FastAPI
from pydantic import BaseModel
import psutil
from typing import Any


app = FastAPI()

class SystemInfo(BaseModel):
    processor_info: Any
    ram_total: float
    ram_used_percent: float
    disk_total: float
    disk_used_percent: float

@app.get("/")
def root():
    try:
        # Obtener información del sistema
        if os.name == 'nt':  # Windows
            processor_info = platform.processor()
            root_disk = os.environ['SystemDrive']  # Obtener la unidad del sistema (normalmente C:)
        else:  # Unix-like
            num_cores = psutil.cpu_count()
            cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
            processor_info = f'{num_cores} cores     {cpu_usage}%'
            root_disk = os.path.abspath(os.sep)  # Obtener la raíz del disco en sistemas Unix-like

        # Información de RAM
        ram_info = psutil.virtual_memory()
        ram_total_gb = round(ram_info.total / (1024 ** 3), 1)
        ram_used_percent = round(ram_info.percent, 1)

        # Información del disco
        disk_info = psutil.disk_usage(root_disk)
        disk_total_gb = round(disk_info.total / (1024 ** 3), 1)
        disk_used_percent = round(disk_info.percent, 1)

        # Construir la respuesta
        system_info = SystemInfo(
            processor_info=processor_info,
            ram_total=ram_total_gb,
            ram_used_percent=ram_used_percent,
            disk_total=disk_total_gb,
            disk_used_percent=disk_used_percent
        )

        # Formatear la respuesta
        formatted_response = {
            "Processor Info": system_info.processor_info,
            "RAM Total (GB)": system_info.ram_total,
            "RAM Used Percentage": system_info.ram_used_percent,
            "Disk Total (GB)": system_info.disk_total,
            "Disk Used Percentage": system_info.disk_used_percent
        }

        return formatted_response
    except Exception as e:
        return {"error": f"Error al obtener información del sistema: {str(e)}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
