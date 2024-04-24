import json
import base64
import hashlib


def hash_with_sha256(data, data_encode=True):
    """
        Function to hash the string into SHA-256 format
    """
    sha256 = hashlib.sha256()
    if data_encode:
        sha256.update(data.encode('utf-8'))
        hashed_data = sha256.hexdigest()
    else:
        sha256.update(data)
        hashed_data = sha256.hexdigest()
    return hashed_data


def base64_encode(payload):
    """
        Function to Encode json to Base64 string
    """
    # Convert payload dictionary to JSON string
    json_payload = json.dumps(payload)
    # Encode JSON string in base64
    base64_encoded_payload = base64.b64encode(json_payload.encode('utf-8')).decode('utf-8')
    return base64_encoded_payload

