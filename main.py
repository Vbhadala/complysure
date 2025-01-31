from fastapi import FastAPI, APIRouter, Request,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse,PlainTextResponse

from typing import Any, List
import os

from utils import fetch_bse, fetch_nse


app = FastAPI(title="Chat App", version="0.0.1")
templates_path = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_path)


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

@app.get("/app", response_class=HTMLResponse)
async def root_app(request: Request):

    data = fetch_nse()
    if data:
        return templates.TemplateResponse("app.html", {"request": request, "data": data})    
    else:
        return templates.TemplateResponse("app.html", {
            "request": request,
            "data": {'error': 'No data available'}
        })


@app.get("/segment", response_class=HTMLResponse)
async def root_segment(request: Request):

    data = fetch_bse()
    if data:
        return templates.TemplateResponse("segment.html", {"request": request, "data": data})    
    else:
        return templates.TemplateResponse("segment.html", {
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

