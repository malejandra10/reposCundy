import psycopg2
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Cundy Crosh API")

class Partida(BaseModel):
    nombre: str
    puntuacion: int
    fecha: str
    duracion: int

@app.get("/")
async def root():
    html = """
    <html>
        <head>
            <title>API para Cundy Crosh</title>
        </head>
        <body>
            <p>Ver las partidas (GET): <a href="/cundy">/cundy</a> con GET</p>
            <p>Insertar partida (POST): <a href="/cundy">/cundy</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)

@app.get("/cundy")
async def get_tabla():
    """
        Devolver todas las partidas almacenadas en la base de datos
    """
    conn = psycopg2.connect(
        dbname="cundycroshdb",
        user="AdminCundy@servidor-cundycrosh",
        password="123 ",
        host="servidor-cundycrosh.postgres.database.azure.com",
        port="5432"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM partida")
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    json = []
    for partida in result:
        json.append({
            "id": partida[0],
            "nombre": partida[1],
            "puntuacion": partida[2],
            "fecha": partida[3],
            "duracion": partida[4]
        })

    return {"partidas": json}

@app.post("/cundy")
async def post_tabla(partida: Partida):
    """
        Insertar partida en la base de datos
    """
    conn = psycopg2.connect(
        dbname="cundycroshdb",
        user="AdminCundy@servidor-cundycrosh",
        password="123",
        host="servidor-cundycrosh.postgres.database.azure.com",
        port="5432"
    )

    cursor = conn.cursor()
    cursor.execute("INSERT INTO partida (nombre, puntuacion, fecha, duracion) VALUES (%s, %s, %s, %s)", (partida.nombre, partida.puntuacion, partida.fecha, partida.duracion))
    conn.commit()
    cursor.close()
    conn.close()
    return "Partida insertada"

