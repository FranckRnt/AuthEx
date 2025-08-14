# Authy Token Extraction Procedure

This procedure details how to extract your authentication tokens from the Authy application using a proxy to intercept communications.

## 📱 Prerequisites

- An iPhone running iOS
- Installation of [OWASP ZAP](https://www.zaproxy.org/download/) on your computer
- Common Wi-Fi connection between computer and phone

## ⚙️ ZAP Configuration

### 1. Proxy Configuration
Configure ZAP to listen on all network interfaces:
- Go to **Options** → **Network** → **Local Servers/Proxies**
- In **Main Proxy**, replace the address with `0.0.0.0`
- Port remains `8080` by default

### 2. SSL Certificate Retrieval
- Go to **Options** → **Network** → **Server Certificates**
- Save the ZAP Root CA certificate

## 📲 Installing the Certificate on iOS

### Step 1: Certificate Transfer
1. Transfer the ZAP SSL certificate to your iPhone (via email, AirDrop, etc.)

### Step 2: Profile Installation
1. Go to **Settings** → **General** → **VPN & Device Management**
2. At the bottom under **DOWNLOADED PROFILE**, tap **Zed Attack Proxy Root CA**
3. Tap **Install** → enter passcode → **Install** → **Install** → **Done**

### Step 3: Trust Activation
1. Go to **Settings** → **General** → **About**
2. Scroll down to **Certificate Trust Settings** (last item)
3. Enable trust for the ZAP certificate

## 🔐 Token Capture

### Authy Preparation
1. **Backup password change** (recommended for a fresh copy):
   - In Authy: **Accounts** → Uncheck then recheck **Backup Password**
   - Optional: **Change password**

2. **Multi-device activation**:
   - Check **Allow Multi-device** to facilitate reconnection

### Capture Process

3. **Uninstall** the Authy application
4. **Reinstall** the application from the App Store
5. **Sign in** with your phone number

6. **⚠️ IMPORTANT** - Proxy configuration BEFORE verification:
   - Find your computer's local IP address (e.g., 192.168.x.x)
     - On Mac: Wi-Fi Settings → Details
   - On iPhone:
     - **Settings** → **Wi-Fi**
     - Tap **(i)** next to the connected network
     - Scroll down to **Configure Proxy**
     - Select **Manual**
     - **Server**: Your computer's IP
     - **Port**: `8080`
     - **Save**

7. **Account verification**: Click **Receive SMS Message**

8. **Token unlocking**: Click on a token with a lock and enter the password

## 📊 Data Extraction in ZAP

### Token Location
In ZAP, search in the request history:
- **Search**: `authenticator_tokens`
- **Or navigate** in the tree:
  ```
  api.authy.com
  └── json
      └── users
          └── [id]
              └── GET:authenticator_tokens
  ```

### Saving
1. In the request response, copy the JSON containing the tokens
2. Save to a file named `authenticator_tokens.json`

## 🔧 Data Processing

Once you have the `authenticator_tokens.json` file:

1. **Decryption**: Run `python decrypt.py`
2. **Conversion**: Run `python convert.py`

This generates import files for Vaultwarden and 2FAS.

## ⚠️ Security Notes

- Disable the proxy on your iPhone once finished
- Remove the ZAP certificate from your iPhone if you no longer use it
- Keep your Authy backup password safe
- Back up your tokens before starting the procedure
