from fastapi import APIRouter, File, UploadFile, Request, HTTPException,BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse,StreamingResponse


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
from io import BytesIO

from annotated_types import Interval
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from datetime import datetime
import traceback

import pandas as pd

import uuid
from pathlib import Path

from checklist.checklist_data import CHECKLIST_ITEMS


router = APIRouter()

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # Point to your templates directory



class ChecklistItemResponse(BaseModel):
    sr_no: int
    parameter: str
    remark: str


class UserChecklistResponse(BaseModel):
    sr_no: int
    user_remark: str




@router.get("/checklist", response_model=List[ChecklistItemResponse])
async def get_checklist():
    """Get the checklist for frontend display."""
    return CHECKLIST_ITEMS


@router.post("/checklist")
async def post_checklist(data: List[UserChecklistResponse]):
    """Accept user checklist input."""
    # Here you can save the data in DB if needed.
    return {"status": "ok", "count": len(data)}


@router.post("/checklist/download")
async def download_checklist(data: List[UserChecklistResponse]):
    """Return an Excel file with user inputs merged into the checklist."""
    # Merge the user input into the checklist
    results = []
    user_data = {d.sr_no: d.user_remark for d in data}
    for item in CHECKLIST_ITEMS:
        results.append({
            "SrNo": item["sr_no"],
            "Parameter": item["parameter"],
            "Original Remark": item["remark"],
            "User Remark": user_data.get(item["sr_no"], "")
        })

    df = pd.DataFrame(results)

    # Export to Excel
    buffer = BytesIO()
    df.to_excel(buffer, index=False, sheet_name="Checklist Results")
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=checklist_results.xlsx"}
    )
