from fastapi import FastAPI, APIRouter, Request,HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.responses import JSONResponse, HTMLResponse, FileResponse,PlainTextResponse

from typing import Any, List


from utils import fetch_bse, fetch_nse


app = FastAPI(title="Chat App", version="0.0.1")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def root(request: Request):

    data = fetch_nse()
    if data:
        return templates.TemplateResponse("index.html", {"request": request, "data": data})    
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "data": {'error': 'No data available'}
        })


@app.get("/data/{exchange}", response_class=HTMLResponse)
async def get_oc_data(request: Request, exchange:str):

    if exchange == "NSE":
        data = fetch_nse()

    elif exchange == "SEBI":
        data = fetch_bse()

    else:
        data = fetch_nse()
        
        
    return templates.TemplateResponse("circular.html", {
        "request": request,
        'exchange': exchange,
        "data": data
    })

