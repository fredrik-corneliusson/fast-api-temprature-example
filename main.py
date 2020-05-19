from datetime import datetime

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sqlite3

from starlette.responses import RedirectResponse

# Skapa databas
# databasen är bara i ram, lätt att ändra till filsökvög om man vill så att det ligger kvar efter omstart.
conn = sqlite3.connect(':memory:', check_same_thread=False)
# Skapa en tabell i databasen för att spara tempraturer
conn.cursor().execute('''CREATE TABLE temps
             (ts timestamp, location text, temp real)''')
# när man jobbar mot databas så måsta man "commita" Det är samma som att spara ändringarna man gjort hittills.
conn.commit()

# Skapa webserver appen som vi kan registrera "REST-sökvägarna på nedan.
app = FastAPI()

# Se till att statiska filer kan hittas på webbservern under /static (där vi har index.html)
app.mount("/static", StaticFiles(directory="static", html=True), name="/")


# Denna är bara så att man kan gå mot http://127.0.0.1:8000 i browser och skickas vidare till startsidan.
@app.get("/")
def index():
    return RedirectResponse(url='/static/index.html')


# API att posta mätvärde till. Den tar en plats samt tempratur samt sparar tid och datum när det gjordes.
# exempel på hur man postar ett mätvärde till denna via kommandraden:
#  curl --location --request POST 'http://127.0.0.1:8000/tempraturer/kitchen/22.2'
@app.post("/tempraturer/{location}/{temp}")
def set_temp(location: str, temp: float):
    conn.cursor().execute("INSERT INTO temps VALUES (?,?,?)", (datetime.now(), location, temp))
    conn.commit()
    return {"location": location, "temp": temp}


# Denna hämtar de sparade tempraturerna, används av javascript på webbsidan.
# returnerar ett Json-sträng som ser ut liknande detta:
#  {"tempratures": [
#    {"timestamp":"2020-05-19 23:22:25.860707","location":"sovrum","temp":21.2},
#    {"timestamp":"2020-05-19 23:22:23.378780","location":"sovrum2","temp":21.2}
#  ]}
@app.get("/tempraturer")
def read_temps():
    temps = []
    for row in conn.cursor().execute('SELECT * FROM temps ORDER BY ts desc'):
        temps.append({'timestamp': row[0], 'location': row[1], 'temp': row[2]})
    return {'tempratures': temps}
