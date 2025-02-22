from fastapi import FastAPI, APIRouter, Request,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse,PlainTextResponse

from typing import Any, List
import os

from utils import all_sebi, fetch_nse, fetch_sebi_exchange, fetch_sebi_mf_pms, fetch_sebi_ra_ia, fetch_cdsl,fetch_mcx


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
            data = all_sebi()
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
            data = fetch_mcx()
            if data:
                return {'status':'ok','segment': segment,'category': category,'data': data}
            else:
                return {'status':'error','segment': segment,'category': category,'message':'No data available'}


        elif category == 'MSEI':
            return {'status':'pending','segment': segment,'category': category}

        elif category == 'CDSL':
            data = fetch_cdsl()
            if data:
                return {'status':'ok','segment': segment,'category': category,'data': data}
            else:
                return {'status':'error','segment': segment,'category': category,'message':'No data available'}


        elif category == 'NSDL':
            return {'status':'pending','segment': segment,'category': category}

    elif segment == 'MF PMS':

        if category == 'SEBI':
            data = fetch_sebi_mf_pms()
            if data:
                return {'status':'ok','segment': segment,'category': category,'data': data}
            else:
                return {'status':'error','segment': segment,'category': category,'message':'No data available'}

        elif category == 'AMFI':
            return {'status':'pending','segment': segment,'category': category}


    elif segment == 'RA IA':
        if category == 'SEBI':
            data = fetch_sebi_ra_ia()
            if data:
                return {'status':'ok','segment': segment,'category': category,'data': data}
            else:
                return {'status':'pending','segment': segment,'category': category}

    else:
        return {'status':'error','error': 'Invalid option', 'segment': segment,'category': category,}
        

