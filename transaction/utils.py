import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def calculate_sha256_string(input_string):
    """
        Function to hash the string into SHA-256 format
    """
    # Create a hash object using the SHA-256 algorithm
    sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    # Update hash with the encoded string
    sha256.update(input_string.encode('utf-8'))
    # Return the hexadecimal representation of the hash
    return sha256.finalize().hex()


def base64_encode(input_dict):
    """
        Function to Encode json to Base64 string
    """
    # Convert the dictionary to a JSON string
    json_data = json.dumps(input_dict)
    # Encode the JSON string to bytes
    data_bytes = json_data.encode('utf-8')
    # Perform Base64 encoding and return the result as a string
    return base64.b64encode(data_bytes).decode('utf-8')

