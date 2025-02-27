from data.database import get_db_connection
from typing import Annotated

from data.dao.dao_alumnos import DaoAlumnos

from data.modelo.menu import Menu

from typing import Union

from fastapi import FastAPI, Request,Form, HTTPException

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")


templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT nombre, numero_pacientes FROM hospital")
    hospitales = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    db.close()
    return templates.TemplateResponse("ver-hospital.html", {"request": request, "hospitales": hospitales})
    

@app.get("/añadir-hospital", response_class=HTMLResponse)
async def añadirhospital(request: Request):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT nombre, numero_pacientes FROM hospital")
    hospitales = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    db.close()
    return templates.TemplateResponse("añadir-hospital.html", {"request": request, "hospitales": hospitales})
   
@app.post("/añadir-hospital/agregar")
async def agregarhospital(request: Request, nombre: str = Form(...), numero_pacientes: int = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO hospital (nombre, numero_pacientes) VALUES (%s, %s)", (nombre, numero_pacientes,))
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        db.close()
    return RedirectResponse(url=request.url_for("añadirhospital"), status_code=303)

@app.get("/actualizar-hospital", response_class=HTMLResponse)
async def actualizarhospital(request: Request):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT nombre, numero_pacientes FROM hospital")
    hospitales = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    db.close()
    return templates.TemplateResponse("actualizar-hospital.html", {"request": request, "hospitales": hospitales})

@app.post("/actualizar-hospital/actualizar")
async def cambiarpacientes(request: Request, nombre_actual: str = Form(...), numero_pacientes: int = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE hospital SET numero_pacientes = %s WHERE nombre = %s", (numero_pacientes, nombre_actual,))
    db.commit()
    cursor.close()
    db.close()
    return RedirectResponse(url=request.url_for("actualizarhospital"), status_code=303)

@app.get("/borrar-hospital", response_class=HTMLResponse)
async def borrarhospital(request: Request):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT nombre, numero_pacientes FROM hospital")
    hospitales = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    db.close()
    return templates.TemplateResponse("borrar-hospital.html", {"request": request, "hospitales": hospitales})

@app.post("/borrar-hospital/eliminar")
async def eliminarhospital(request: Request, nombre: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM hospital WHERE nombre = %s", (nombre,))
    db.commit()
    cursor.close()
    db.close()
    return RedirectResponse(url=request.url_for("borrarhospital"), status_code=303)