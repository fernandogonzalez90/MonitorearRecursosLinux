from fastapi import FastAPI
from pydantic import BaseModel
import psutil
import platform

app = FastAPI()

class SystemInfo(BaseModel):
    processor_info: str
    ram_info: int
    disk_info: int

@app.get("/get_system_info")
def get_system_info():
    # Obtener información del sistema
    processor_info = platform.processor()
    ram_info = psutil.virtual_memory().total
    disk_info = psutil.disk_usage('/').total

    # Construir la respuesta
    system_info = SystemInfo(
        processor_info=processor_info,
        ram_info=ram_info,
        disk_info=disk_info
    )

    # Formatear la respuesta
    formatted_response = {
        "Processor Info": system_info.processor_info,
        "RAM Info (bytes)": system_info.ram_info,
        "Disk Info (bytes)": system_info.disk_info
    }

    return formatted_response

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
