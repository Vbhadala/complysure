from fastapi import FastAPI, APIRouter, Request,HTTPException
from fastapi.templating import Jinja2Templates

from fastapi.responses import JSONResponse, HTMLResponse, FileResponse,PlainTextResponse

from typing import Any, List
import os

from utils import fetch_bse, fetch_nse


app = FastAPI(title="Chat App", version="0.0.1")

# Define the absolute path for the static directory
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
