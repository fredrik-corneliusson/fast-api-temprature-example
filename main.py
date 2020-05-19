from datetime import datetime

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sqlite3

# databasen är bara i ram, lätt att ändra till fil om man vill.
from starlette.responses import RedirectResponse

conn = sqlite3.connect(':memory:', check_same_thread=False)
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE temps
             (ts timestamp, location text, temp real)''')

conn.commit()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="/")


@app.get("/")
def index():
    return RedirectResponse(url='/static/index.html')


# API att posta tempratur till
# exempel:
#  curl --location --request POST 'http://127.0.0.1:8000/tempraturer/kitchen/22.2'
@app.post("/tempraturer/{location}/{temp}")
def set_temp(location: str, temp: float):
    c = conn.cursor()
    c.execute("INSERT INTO temps VALUES (?,?,?)", (datetime.now(), location, temp))
    conn.commit()
    return {"location": location, "temp": temp}


@app.get("/tempraturer")
def read_temps():
    c = conn.cursor()
    temps = []
    for row in c.execute('SELECT * FROM temps ORDER BY ts desc'):
        temps.append({'timestamp': row[0], 'location': row[1], 'temp': row[2]})
    return {'tempratures': temps}
