import base64
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key

def verify_request(raw_body, signature, public_key_pem):
    """Verify the request payload with the provided public key and signature"""
    try:
        # Decode the signature from base64
        signature = base64.b64decode(signature)

        # Load the public key
        public_key = load_pem_public_key(public_key_pem.encode())

        # Verify the signature based on key type
        if isinstance(public_key, ec.EllipticCurvePublicKey):
            # EC key verification
            public_key.verify(
                signature,
                raw_body.encode(),
                ec.ECDSA(hashes.SHA256())
            )
        else:
            raise ValueError("Unsupported key type")

        return True
    except Exception as e:
        print(f"Verification failed: {e}")
        return False


def fetch_verification_keys(token=""):
    """Fetch the public keys from GitHub"""
    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"

    response = requests.get("https://api.github.com/meta/public_keys/copilot_api", headers=headers)

    if response.status_code == 200:
        # Parse the response and return the keys
        return response.json().get('public_keys', [])
    else:
        raise Exception(f"Failed to fetch keys: {response.status_code}")


def verify_request_by_key_id(raw_body, signature, key_id, token=""):
    """Fetch the public key matching the key identifier and verify the request"""
    # Fetch all public keys
    public_keys = fetch_verification_keys(token)

    # Find the matching key by key_id
    public_key = next((key for key in public_keys if key["key_identifier"] == key_id), None)

    if not public_key:
        raise Exception(f"No public key found matching key identifier: {key_id}")

    # Verify the request using the matching public key
    public_key_pem = public_key['key']
    is_valid = verify_request(raw_body, signature, public_key_pem)

    return is_valid
