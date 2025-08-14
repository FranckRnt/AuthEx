import json
import base64
import binascii  # For base16 decoding
from getpass import getpass  # For hidden password input
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def decrypt_token(kdf_rounds, encrypted_seed_b64, salt, iv, passphrase):
    try:
        # Decode the base64-encoded encrypted seed
        encrypted_seed = base64.b64decode(encrypted_seed_b64)

        # Derive the encryption key using PBKDF2 with SHA-1
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(),
            length=32,  # AES-256 requires a 32-byte key
            salt=salt.encode(),
            iterations=kdf_rounds,
            backend=default_backend()
        )
        key = kdf.derive(passphrase.encode())

        # AES with CBC mode
        # Some versions of Authy used an IV, while others used a null IV. We account for both cases here.
        if not iv:
            iv = bytes([0] * 16)
        else:
            iv = binascii.unhexlify(iv)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the ciphertext
        decrypted_data = decryptor.update(encrypted_seed) + decryptor.finalize()

        # Remove PKCS7 padding
        padding_len = decrypted_data[-1]

        padding_start = len(decrypted_data) - padding_len

        # Validate padding
        if padding_len > 16 or padding_start < 0:
            raise ValueError("Invalid padding length")
        if not all(pad == padding_len for pad in decrypted_data[padding_start:]):
            raise ValueError("Invalid padding bytes")

        return decrypted_data[:padding_start].decode('utf-8')
    except Exception as e:
        return f"Decryption failed: {str(e)}"


def process_authenticator_data(input_file, output_file, backup_password):
    with open(input_file, "r") as json_file:
        data = json.load(json_file)

    decrypted_tokens = []
    for token in data['authenticator_tokens']:
        decrypted_seed = decrypt_token(
            kdf_rounds=token['key_derivation_iterations'],
            encrypted_seed_b64=token['encrypted_seed'],
            salt=token['salt'],
            iv=token['unique_iv'],
            passphrase=backup_password
        )
        decrypted_token = {
            "account_type": token["account_type"],
            "name": token["name"],
            "issuer": token["issuer"],
            "decrypted_seed": decrypted_seed,  # Store as UTF-8 string
            "digits": token["digits"],
            "logo": token["logo"],
            "unique_id": token["unique_id"]
        }
        decrypted_tokens.append(decrypted_token)

    output_data = {
        "message": "success",
        "decrypted_authenticator_tokens": decrypted_tokens,
        "success": True
    }

    with open(output_file, "w") as output_json_file:
        json.dump(output_data, output_json_file, indent=4)

    print(f"Decryption completed. Decrypted data saved to '{output_file}'.")


input_file = "authenticator_tokens.json"
output_file = "decrypted_tokens.json"

# Prompt for the backup password at runtime (hidden input)
backup_password = getpass("Enter the backup password: ").strip()

process_authenticator_data(input_file, output_file, backup_password)