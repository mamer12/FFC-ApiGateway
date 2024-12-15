from app.utils.auth import API_KEY_STORAGE, verify_api_key
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, Depends
from typing import List
from app.models import DocTypePayload, APIKeyResponse, UpdateDocTypePayload
from app.services.erp_client import (
    create_doc_type,
    read_doc_type,
    update_doc_type,
    upload_file,
)
import secrets

router = APIRouter(tags=["ERPNext"])

@router.post("/generate-api-key")
async def generate_api_key():
    # Generate API key and secret
    api_key = secrets.token_hex(16)
    api_secret = secrets.token_hex(16)

    # Store the API key and secret (in memory for now; use a secure DB in production)
    API_KEY_STORAGE[api_key] = api_secret

    return {"api_key": api_key, "api_secret": api_secret}

@router.post("/new-invoice-request")
async def create_invoice_request(payload: List[DocTypePayload]):
    results = []
    for doc in payload:
        try:
            # Step 1: Create the DocType in ERPNext
            result = await create_doc_type("Online Invoice Financing", doc.dict())
            doc_name = result["data"]["name"]  # Extract the document name (ID) from the response

            # Step 2: Upload files associated with the created DocType
            uploaded_file_urls = []
            for file_url in doc.file_urls:  # Assuming file_urls is part of the payload
                uploaded_url = await upload_file(file_url, "Online Invoice Financing", doc_name)
                uploaded_file_urls.append(uploaded_url)

            # Step 3: Update the DocType with the uploaded file URLs if any
            if uploaded_file_urls:
                # Optionally update the document with the uploaded files (file URLs)
                update_payload = {"file_urls": uploaded_file_urls}
                await update_doc_type("Online Invoice Financing", doc_name, update_payload)

            # Append the result of the DocType creation and file upload
            results.append({
                "request_id": doc_name,
                "uploaded_file_urls": uploaded_file_urls
            })

        except HTTPException as e:
            raise HTTPException(status_code=500, detail=f"HTTP error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return {"results": results}

@router.get("/invoice-request-info", dependencies=[Depends(verify_api_key)])
async def read_invoice_request(doctype: str, name: str):
    response = await read_doc_type(doctype, name)
    workflow_state = response.get("workflow_state", "Pending")
    repayments = response.get("repayments", [])
    return {
        "workflow_state": workflow_state,
        "repayments": repayments
    }

@router.put("/update-invoice-info", dependencies=[Depends(verify_api_key)])
async def update_invoice_info(payload: List[UpdateDocTypePayload]):
    return payload


@router.post("/approved-request", )
async def handle_approved_request(payload: dict):
    """
    Handles webhook requests from ERPNext for approved invoices.

    Args:
        payload (dict): Incoming webhook data from ERPNext.

    Returns:
        dict: Response indicating success or failure.
    """
    return payload
