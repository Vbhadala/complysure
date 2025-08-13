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

from fastapi import BackgroundTasks
from aiosmtplib import send
from email.message import EmailMessage

import smtplib, ssl

from checklist.checklist_data import CHECKLIST_ITEMS


router = APIRouter()

router = APIRouter()
templates = Jinja2Templates(directory="templates")  # Point to your templates directory


async def send_email_with_excel(clientCode, data, nonComplianceBrief, recipient_email):
    """Send an email with the Excel as an attachment."""

    smtp_host = "smtp.gmail.com"
    smtp_port = 465
    smtp_user = "query.moneypros@gmail.com"
    smtp_password = "vwty antt fmaf wgxn"
    
    results = []
    user_data = {d.sr_no: d.user_remark for d in data}
    for item in CHECKLIST_ITEMS:
        results.append({
            "SrNo": item["sr_no"],
            "Parameter": item["parameter"],
            "User Remark": user_data.get(item["sr_no"], "")
        })
    
    # Add non-compliance brief as a separate row
    if nonComplianceBrief:
        results.append({
            "SrNo": "",
            "Parameter": "Brief about Non-Compliance (if any)",
            "User Remark": nonComplianceBrief
        })
    else:
        results.append({
            "SrNo": "",
            "Parameter": "Brief about Non-Compliance (if any)",
            "User Remark": "Nil"
        })

    df = pd.DataFrame(results)

    buffer = BytesIO()
    df.to_excel(buffer, index=False, sheet_name="Checklist Results")
    buffer.seek(0)

    # Build the email
    msg = EmailMessage()
    msg["Subject"] = f"Audit Report Checklist - {clientCode}"
    msg["From"] = smtp_user
    msg["To"] = recipient_email
    msg.set_content("Please find the checklist results.")
    msg.add_attachment(buffer.read(),
                      maintype="application",
                      subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                      filename=f"report_{clientCode}.xlsx")

    # await send(msg, hostname=smtp_host, port=smtp_port,
    #            username=smtp_user, password=smtp_password,
    #            use_tls=True)

    await send(msg, hostname=smtp_host, port=587,
           username=smtp_user, password=smtp_password,
            start_tls=True)



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


class UserChecklistPayload(BaseModel):
    clientCode: str
    payload: List[UserChecklistResponse]
    nonComplianceBrief: str = ""
    

@router.post("/checklist")
async def post_checklist(data: UserChecklistPayload, background_tasks: BackgroundTasks):
    
    print(f"Client: {data.clientCode}")
    print(f"Data: {data.payload}")
    print(f"Non-Compliance Brief: {data.nonComplianceBrief}")
    
    recipient_email = "north.audit@srcl.in"

    background_tasks.add_task(send_email_with_excel,data.clientCode, data.payload, data.nonComplianceBrief, recipient_email)
    
    return {"status": "ok", "count": len(data.payload)}


class DownloadPayload(BaseModel):
    payload: List[UserChecklistResponse]
    nonComplianceBrief: str = ""

@router.post("/checklist/download")
async def download_checklist(data: DownloadPayload):
    """Return an Excel file with user inputs merged into the checklist."""
    # Merge the user input into the checklist
    results = []
    user_data = {d.sr_no: d.user_remark for d in data.payload}
    for item in CHECKLIST_ITEMS:
        results.append({
            "SrNo": item["sr_no"],
            "Parameter": item["parameter"],
            "Original Remark": item["remark"],
            "User Remark": user_data.get(item["sr_no"], "")
        })
    
    # Add non-compliance brief as a separate row
    if data.nonComplianceBrief:
        results.append({
            "SrNo": "",
            "Parameter": "Brief about Non-Compliance (if any)",
            "Original Remark": "",
            "User Remark": data.nonComplianceBrief
        })
    else:
        results.append({
            "SrNo": "",
            "Parameter": "Brief about Non-Compliance (if any)",
            "Original Remark": "",
            "User Remark": "Nil"
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
