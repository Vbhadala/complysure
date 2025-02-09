from fastapi import FastAPI, APIRouter, Request,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse,PlainTextResponse

from typing import Any, List
import os

from utils import fetch_sebi, fetch_nse


app = FastAPI(title="Chat App", version="0.0.1")
templates_path = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_path)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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


@app.get("/api/{segment}", response_class=JSONResponse)
async def get_segments(request: Request, segment:str):

    if segment == 'Stock Broker':
        return {'tabs': ['SEBI','NSE','BSE','NCDEX','MCX','MSEI','CDSL','NSDL']}

    elif segment == 'MF PMS':
        return {'tabs': ['SEBI','AMFI']}

    elif segment == 'RA IA':
        return {'tabs': ['SEBI']}

    else:
        return {'error': 'Invalid option', 'opt': segment}


@app.get("/api/{segment}/{category}", response_class=JSONResponse)
async def get_segment_data(request: Request, segment:str,category:str):


    #response structure
    #success: status:ok data:data, segment:segment, category:category,
    #error: status:error data:data, segment:segment, category:category,
    #comming soon: status:pending data:data, segment:segment, category:category,
    
    if segment == 'Stock Broker':

        if category == 'SEBI':
            data = fetch_sebi()
            if data:
                return {'status':'ok','segment': segment,'category': category,'data': data}
            else:
                return {'status':'error','segment': segment,'category': category,'message':'No data available'}

        elif category == 'NSE':
            data = fetch_nse()
            if data:
                return {'status':'ok','segment': segment,'category': category,'data': data}
            else:
                return {'status':'error','segment': segment,'category': category,'message':'No data available'}

        elif category == 'BSE':
            return {'status':'pending','segment': segment,'category': category}

        elif category == 'NCDEX':
            return {'status':'pending','segment': segment,'category': category}

        elif category == 'MCX':
            return {'status':'pending','segment': segment,'category': category}

        elif category == 'MSEI':
            return {'status':'pending','segment': segment,'category': category}

        elif category == 'CDSL':
            return {'status':'pending','segment': segment,'category': category}

        elif category == 'NSDL':
            return {'status':'pending','segment': segment,'category': category}

    elif segment == 'MF PMS':

        if category == 'SEBI':
            data = fetch_sebi()
            if data:
                return {'status':'ok','segment': segment,'category': category,'data': data}
            else:
                return {'status':'error','segment': segment,'category': category,'message':'No data available'}

        elif category == 'AMFI':
            return {'status':'pending','segment': segment,'category': category}


    elif segment == 'RA IA':
        if category == 'SEBI':
            data = fetch_sebi()
            if data:
                return {'status':'ok','segment': segment,'category': category,'data': data}
            else:
                return {'status':'pending','segment': segment,'category': category}

    else:
        return {'status':'error','error': 'Invalid option', 'segment': segment,'category': category,}
        


@app.get("/segment", response_class=HTMLResponse)
async def root_segment(request: Request):

    data = fetch_sebi()
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
        data = fetch_sebi()

    else:
        data = fetch_nse()
        
        
    return templates.TemplateResponse("circular.html", {
        "request": request,
        'exchange': exchange,
        "data": data
    })


