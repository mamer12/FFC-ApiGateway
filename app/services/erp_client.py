from http.client import HTTPException
import httpx # type: ignore
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables from the .env file
load_dotenv()

# Get the base URL of the ERP system and the API credentials
BASE_URL = os.getenv("ERP_BASE_URL")
API_KEY = os.getenv("ERP_API_KEY")
API_SECRET = os.getenv("ERP_API_SECRET")

# Headers to be used for API requests
HEADERS = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    'Accept': 'application/json'
}

# Mock API Key generation function (if needed)
async def create_api_key():
    return {"key": "mocked-key", "secret": "mocked-secret"}


# Function to create a new DocType entry in the ERP system
async def create_doc_type(doctype: str, payload: dict):
    async with httpx.AsyncClient() as client:
        # Make a POST request to the ERP system to create a new DocType
        response = await client.post(f"{BASE_URL}/api/resource/{doctype}", headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise error if the request fails
        return response.json()

# Function to read a DocType from the ERP system
async def read_doc_type(doctype: str, name: str):
    async with httpx.AsyncClient() as client:
        # Make a GET request to retrieve the DocType from the ERP system
        response = await client.get(f"{BASE_URL}/api/resource/{doctype}/{name}", headers=HEADERS)
        response.raise_for_status()  # Raise error if the request fails
        return response.json()

# Function to update a DocType in the ERP system
async def update_doc_type(doctype: str, name: str, payload: dict):
    async with httpx.AsyncClient() as client:
        # Make a PUT request to update the DocType in the ERP system
        response = await client.put(f"{BASE_URL}/api/resource/{doctype}/{name}", headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise error if the request fails
        return response.json()


async def upload_file(file_url: str, doctype: str, docname: str) -> str:
    """
    Uploads a file URL to ERPNext using the upload_file API endpoint.
    :param file_url: The URL of the file to be uploaded.
    :param doctype: The DocType where the file should be attached.
    :param docname: The name of the document where the file will be attached.
    :return: The uploaded file's URL returned by ERPNext.
    """
    try:
        async with httpx.AsyncClient() as client:
            # Form the URL for the upload endpoint
            url = f"{BASE_URL}/api/method/upload_file"

            # Define the payload with the necessary fields
            data = {
                "is_private": 1,  # Set to 1 if the file should be private
                "folder": "Home/Attachments",  # Define the folder for attachments
                "file_url": file_url,  # The file URL to upload
                "doctype": doctype,  # The DocType
                "docname": docname  # The document name (e.g., invoice ID)
            }

            # Make the POST request to upload the file
            response = await client.post(url, headers=HEADERS, json=data)

            response.raise_for_status()  # Raise an error if the request fails

            # Return the uploaded file's URL from ERPNext
            response_data = response.json()
            # Check if the file upload response has the expected structure
            if "message" in response_data and "file_url" in response_data["message"]:
                return response_data["message"]["file_url"]
            else:
                raise HTTPException(status_code=500, detail="File upload failed, missing 'file_url' in response.")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"File upload failed: {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def validate_payment(payload: dict):
    async with httpx.AsyncClient() as client:
        # Make a POST request to the ERP system to create a new DocType
        response = await client.post(f"{BASE_URL}/api/method/financing.lending.doctype.loan_payment.loan_payment.validate_payment", headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise error if the request fails
        return response.json()
