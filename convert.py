import json
import uuid
import urllib.parse
import random
import time

def convert_authy_to_bitwarden(authy_data):
    # Convert to Bitwarden format
    bitwarden_data = {"encrypted": False, "items": []}

    for account in authy_data["decrypted_authenticator_tokens"]:
        # Ensure all fields are strings or provide defaults
        name = str(account.get("name", ""))
        issuer = account.get("issuer")  # May be None
        secret = str(account.get("decrypted_seed", ""))
        digits = str(account.get("digits", "6"))

        # Construct TOTP URI
        totp_uri = f"otpauth://totp/{urllib.parse.quote(issuer or '')}:{urllib.parse.quote(name)}?"
        totp_uri += f"secret={urllib.parse.quote(secret)}&digits={digits}"
        if issuer:
            totp_uri += f"&issuer={urllib.parse.quote(issuer)}"

        # Add to Bitwarden items
        bitwarden_data["items"].append({
            "favorite": False,
            "id": str(uuid.uuid4()).upper(),
            "name": name,
            "type": 1,
            "login": {
                "username": name,
                "totp": totp_uri
            }
        })

    # Save to JSON file
    with open("vaultwarden_import.json", "w") as f:
        json.dump(bitwarden_data, f, indent=4)

    print("Vaultwarden import file created: vaultwarden_import.json")

def convert_authy_to_2fas(authy_data):
    # Convert to 2FAS format
    colors = ["Red", "Green", "Blue", "Yellow", "Pink"]
    two_fas_data = {
        "appOrigin": "ios", 
        "appVersionName": "5.3.13", 
        "appVersionCode": 50313,
        "groups": [],
        "schemaVersion": 4,
        "services": []
    }

    for i, account in enumerate(authy_data["decrypted_authenticator_tokens"]):
        # Ensure all fields are properly formatted
        name = str(account.get("name", "")).strip()
        issuer = account.get("issuer")
        secret = str(account.get("decrypted_seed", "")).upper()
        digits = int(account.get("digits", 6))
        
        # Use issuer if available, otherwise use name
        account_name = name
        if issuer and issuer.strip():
            issuer = issuer.strip()
            # Format: issuer - account or just account
            display_name = f"{issuer} - {name}" if name and name != issuer else issuer
        else:
            issuer = None
            display_name = name

        # Construct proper TOTP URI format
        if issuer:
            totp_uri = f"otpauth:\\/\\/totp\\/{urllib.parse.quote(issuer)}%20-%20{urllib.parse.quote(account_name)}?"
        else:
            totp_uri = f"otpauth:\\/\\/totp\\/{urllib.parse.quote(account_name)}?"
        
        totp_uri += f"secret=[hidden]&digits={digits}"
        
        # Add to 2FAS services
        two_fas_data["services"].append({
            "secret": secret,
            "otp": {
                "tokenType": "TOTP",
                "digits": digits,
                "algorithm": "SHA1",
                "period": 30,
                "source": "link",
                "account": account_name,
                "counter": 0,
                "link": totp_uri
            },
            "icon": {
                "label": {
                    "backgroundColor": random.choice(colors),
                    "text": display_name[:2].upper() if display_name else "XX"
                },
                "iconCollection": {
                    "id": str(uuid.uuid4()).upper()
                },
                "selected": "Label"
            },
            "order": {
                "position": i
            },
            "updatedAt": int(time.time() * 1000),
            "name": display_name if display_name else f"Account {i+1}"
        })

    with open("2fas_import.2fas", "w") as f:
        json.dump(two_fas_data, f, indent=4)

    print("2FAS import file created: 2fas_import.2fas")


with open("decrypted_tokens.json", "r") as f:
    authy_data = json.load(f)
    convert_authy_to_bitwarden(authy_data)
    convert_authy_to_2fas(authy_data)