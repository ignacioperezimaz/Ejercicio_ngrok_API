
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# CREAR LA API
app = FastAPI(
    title="CHALLENGE - API de Tareas",
    description="""
    # Bienvenido a nuestra API

    Esta API permite gestionar una lista de tareas.

    Puedes consultar, crear, modificar y eliminar tareas.

    ## ¿Cómo utilizar esta API?

    1. Selecciona uno de los métodos disponibles.
    2. Lee la descripción del método.
    3. Pulsa **Try it out**.
    4. Introduce los datos solicitados, si los hay.
    5. Pulsa **Execute**.
    6. Consulta el resultado en **Response body**.

    ## Significado de los métodos
    - **GET:** Consultar información.
    - **POST:** Crear información nueva.
    - **PUT:** Modificar información existente.
    - **DELETE:** Eliminar información.
    """,
    version="1.0.0"
)

# MODELO DE DATOS
class Tarea(BaseModel):
    nombre: str = Field(
        ...,
        description="Nombre de la tarea",
        examples=["Estudiar Python"]
    )
    completada: bool = Field(
        False,
        description="true si está terminada, false si está pendiente"
    )


# LISTA INICIAL DE TAREAS
tareas = [
    {"id": 1, "nombre": "Estudiar Python", "completada": False},
    {"id": 2, "nombre": "Hacer ejercicio", "completada": True}
]


# METODO 1: GET - VER TODAS LAS TAREAS
@app.get(
    "/tareas",
    tags=["1. Consultar tareas"],
    summary="Ver todas las tareas",
    description="""
    Devuelve una lista con todas las tareas guardadas.

    ### Pasos
    1. Pulsa **Try it out**.
    2. Pulsa **Execute**.
    3. Observa la lista en **Response body**.

    No es necesario introducir ningún dato.
    """
)
def obtener_tareas():
    return tareas


# METODO 2: GET - BUSCAR UNA TAREA
@app.get(
    "/tareas/{id}",
    tags=["1. Consultar tareas"],
    summary="Buscar una tarea por ID",
    description="""
    Busca una tarea utilizando su identificador.

    ### Pasos
    1. Pulsa **Try it out**.
    2. Introduce un ID, por ejemplo **1**.
    3. Pulsa **Execute**.
    4. Observa la tarea encontrada.

    Si el ID no existe, aparece un error 404.
    """
)
def buscar_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            return tarea

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )


# METODO 3: POST - CREAR UNA TAREA
@app.post(
    "/tareas",
    tags=["2. Crear tareas"],
    summary="Crear una nueva tarea",
    status_code=201,
    description="""
    Permite añadir una tarea nueva a la lista.

    ### Pasos
    1. Pulsa **Try it out**.
    2. Introduce el nombre y el estado de la tarea.
    3. Pulsa **Execute**.
    4. Observa la tarea creada.

    ### Ejemplo de entrada
    ```json
    {
      "nombre": "Estudiar Docker",
      "completada": false
    }
    ```

    El ID se genera automáticamente.
    """
)
def crear_tarea(tarea: Tarea):
    nuevo_id = max(
        (t["id"] for t in tareas),
        default=0
    ) + 1

    nueva_tarea = {
        "id": nuevo_id,
        **tarea.model_dump()
    }

    tareas.append(nueva_tarea)
    return nueva_tarea


# METODO 4: PUT - MODIFICAR UNA TAREA
@app.put(
    "/tareas/{id}",
    tags=["3. Modificar tareas"],
    summary="Modificar una tarea existente",
    description="""
    Permite cambiar los datos de una tarea.

    ### Pasos
    1. Pulsa **Try it out**.
    2. Introduce el ID de la tarea.
    3. Escribe los nuevos datos.
    4. Pulsa **Execute**.

    ### Ejemplo
    Para marcar una tarea como terminada:

    ```json
    {
      "nombre": "Estudiar Python",
      "completada": true
    }
    ```

    Si el ID no existe, aparece un error 404.
    """
)
def modificar_tarea(id: int, datos: Tarea):
    for tarea in tareas:
        if tarea["id"] == id:
            tarea.update(datos.model_dump())
            return tarea

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )


# METODO 5: DELETE - ELIMINAR UNA TAREA
@app.delete(
    "/tareas/{id}",
    tags=["4. Eliminar tareas"],
    summary="Eliminar una tarea",
    description="""
    Elimina una tarea de la lista mediante su ID.

    ### Pasos
    1. Pulsa **Try it out**.
    2. Introduce el ID de la tarea.
    3. Pulsa **Execute**.
    4. Comprueba el mensaje de confirmación.

    ### Ejemplo
    Introduce el ID **2** para eliminar la tarea 2.

    Si la tarea no existe, aparece un error 404.
    """
)
def eliminar_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            tareas.remove(tarea)
            return {"mensaje": "Tarea eliminada correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Tarea no encontrada"
    )

# INTERFAZ WEB
from pathlib import Path
from fastapi.responses import FileResponse

@app.get("/interfaz", include_in_schema=False)
def mostrar_interfaz():
    archivo = Path(__file__).with_name("index.html")
    return FileResponse(archivo, media_type="text/html")
