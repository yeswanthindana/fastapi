from fastapi import Request, HTTPException, status
import json
import logging
import random
import string

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def duplicate_key_checker(ordered_pairs):
    """
    Hook to check for duplicate keys in JSON object.
    """
    cleaned_dict = {}
    for key, value in ordered_pairs:
        if key in cleaned_dict:
            raise ValueError(f"Duplicate key detected: '{key}'")
        cleaned_dict[key] = value
    return cleaned_dict

async def verify_unique_keys(request: Request):
    """
    Middleware-like dependency to verify incoming JSON does not have duplicate keys.
    """
    # Only verify for state-changing methods
    if request.method in ["POST", "PUT", "PATCH"]:
        
        # Check content type
        content_type = request.headers.get("content-type", "")
        if "application/json" not in content_type:
            # If not JSON, skip validation or handle appropriately
            return

        body_bytes = await request.body()
        if not body_bytes:
            return

        try:
            # Parse using the custom hook
            json.loads(body_bytes.decode("utf-8"), object_pairs_hook=duplicate_key_checker)
        except ValueError as e:
            logger.error(f"Duplicate key error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Invalid JSON Payload: {str(e)}"
            )
        except Exception:
            # Let default parsers handle other malformed JSON errors
            pass    

def generate_random_password(length=12):
    """
    Generates a secure random password of given length.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password
