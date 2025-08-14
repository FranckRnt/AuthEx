# AuthEx - Authy Token Exporter

AuthEx is a Python tool that allows you to decrypt and convert Authy authentication tokens to other two-factor authentication (2FA) managers.

## 🎯 Features

- **Authy Token Decryption**: Decrypts encrypted seeds from Authy authentication tokens
- **Bitwarden/Vaultwarden Conversion**: JSON export compatible with Bitwarden
- **2FAS Conversion**: .2fas format export for the 2FAS application
- **Security**: Uses standard cryptography (AES-256-CBC with PBKDF2-SHA1)

## 📋 Prerequisites

- Python 3.6+
- Dependencies listed in `requirements.txt`

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/FranckRnt/AuthEx.git
cd AuthEx
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or manually install the main dependency:
```bash
pip install cryptography
```

## 📖 Usage

### Step 1: Prepare the Authy file

Before using AuthEx, you need to obtain the `authenticator_tokens.json` file from your Authy application.

📋 **Detailed procedure available**: [Authy Token Extraction Guide](AUTHY_EXTRACTION.md)

This procedure uses a proxy (OWASP ZAP) to intercept communications and retrieve your encrypted tokens during Authy synchronization.

### Step 2: Decrypt the tokens

Run the decryption script:

```bash
python decrypt.py
```

The script will ask for your Authy backup password. Once decryption is successful, a `decrypted_tokens.json` file will be created.

### Step 3: Convert to your password manager

Run the conversion script:

```bash
python convert.py
```

This script generates two files:
- `vaultwarden_import.json`: Compatible with Bitwarden/Vaultwarden
- `2fas_import.2fas`: Compatible with the 2FAS application

## 📁 File Structure

```
AuthEx/
├── decrypt.py              # Authy token decryption script
├── convert.py              # Conversion script to other formats
├── requirements.txt        # Python dependencies
├── AUTHY_EXTRACTION.md     # Detailed token extraction guide
├── authenticator_tokens.json  # Input file (encrypted Authy tokens)
├── decrypted_tokens.json   # Temporary file (decrypted tokens)
├── vaultwarden_import.json # Bitwarden/Vaultwarden export
└── 2fas_import.2fas        # 2FAS export
```

## 🔧 Technical Details

### Decryption Algorithm
- **Encryption**: AES-256-CBC
- **Key Derivation**: PBKDF2 with SHA-1
- **Padding**: PKCS7

### Output Formats

#### Bitwarden/Vaultwarden
Generates a JSON file with the structure:
```json
{
  "encrypted": false,
  "items": [
    {
      "id": "UUID",
      "name": "Account Name",
      "type": 1,
      "login": {
        "username": "Account Name",
        "totp": "otpauth://totp/..."
      }
    }
  ]
}
```

#### 2FAS
Generates a .2fas file with the native 2FAS application structure including:
- Application metadata
- Services with TOTP secrets
- Automatically generated colored icons

```json
{
    "appOrigin": "ios",
    "appVersionName": "5.3.13",
    "appVersionCode": 50313,
    "groups": [],
    "schemaVersion": 4,
    "services": [
        {
            "secret": "Secret",
            "otp": {
                "tokenType": "TOTP",
                "digits": 6,
                "algorithm": "SHA1",
                "period": 30,
                "source": "link",
                "account": "Twitch",
                "counter": 0,
                "link": "otpauth:\\/\\/totp\\/Twitch%20-%20Twitch?secret=[hidden]&digits=6"
            },
            "icon": {
                "label": {
                    "backgroundColor": "Pink",
                    "text": "TW"
                },
                "iconCollection": {
                    "id": "05F67F51-AAE3-492A-9598-1A08BA1C6857"
                },
                "selected": "Label"
            },
            "order": {
                "position": 0
            },
            "updatedAt": 1754992012504,
            "name": "Twitch"
        }
    ]
}    
```

## ⚠️ Security Warnings

1. **Back up your data**: Make sure you have a backup of your tokens before starting
2. **Delete temporary files**: Delete `decrypted_tokens.json` after use
3. **Strong password**: Use a robust Authy backup password
4. **Secure environment**: Run these scripts in a trusted environment

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Add support for other 2FA managers

## 📄 License

This project is under the MIT license. See the LICENSE file for more details.

## 🙏 Acknowledgments

This project is inspired by research on Authy cryptography and export format specifications from popular 2FA managers.

---

**Disclaimer**: This tool is provided for educational and migration purposes. Use it responsibly and respect the terms of service of the relevant services.
