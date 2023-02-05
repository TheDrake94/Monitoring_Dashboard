#Librerie
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import datetime
import pandas as pd
import yfinance as yf
import asyncio

# Inizializzo Fastapi
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Settaggio della directory dei Templates
templates = Jinja2Templates(directory="templates")

# Pagina Home
@app.get("/Home", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Creazione Servizi Web Socket per ogni Stock
@app.websocket("/monitoring/monitoring")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    end = datetime.datetime.now()
    start = end + datetime.timedelta(days=-60)
    print('-------------------')
    print(start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
    print('-------------------')
    df_finance = yf.download("AAPL", start=start.strftime(
        "%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
    df_finance = df_finance.reset_index()

    for el in range(len(df_finance)):
        await websocket.send_json({
            'time':str(df_finance['Date'].iloc[el])[:10],
            'value':str(df_finance['Close'].iloc[el])
        })
        await asyncio.sleep(1)

# Avvio Programma
if __name__ == "__main__":
    uvicorn.run("server_python:app", port=5000)
    