from pydantic import BaseModel
from typing import List, Dict, Optional


class InvoiceItem(BaseModel):
    item_name: str
    item_price: float
    quantity: int
    total_price: float


class InvoiceDocTypePayload(BaseModel):
    loan_product: str
    applicant_type: str
    applicant: str
    requested_by: str
    requestor_name: str
    reference_request_id: str
    invoice_id: str
    invoice_number: str
    invoice_date: str
    invoice_status: str
    client_id: str
    client_name: str
    loan_amount: float
    representative_name: str
    representative_id: str
    total_invoice_amount: float
    paid_amount: float
    outstanding_amount: float
    invoice_items: List[InvoiceItem]
    file_urls: Optional[List[str]] = []  # Add optional field for file URLs

class UpdateDocTypePayload(BaseModel):
    id: str
    doctype: str
    data: Dict  # Data for the document update

class ReadDocTypeResponse(BaseModel):
    workflow_state: str
    repayments: List[Dict[str, str]]

class APIKeyResponse(BaseModel):
    key: str
    secret: str

class PaymentDocTypePayload(BaseModel):
    loan_type: str
    loan_id: str
    repayment_method: str
    payment_date: str
    payment_amount: float
    source: str
    transaction_id: Optional[str] = None
    transaction_fee: float

# Define the request body structure using Pydantic
class FileUploadRequest(BaseModel):
    doctype: str
    docname: str
    file_urls: List[str]
