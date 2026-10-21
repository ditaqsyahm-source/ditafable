import os
import sys
import urllib.parse
import urllib.request
import json

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(DIR_PATH, ".env")

def load_env():
    env = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

def save_refresh_token(refresh_token):
    lines = []
    found = False
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("YT_REFRESH_TOKEN="):
                lines.append(f"YT_REFRESH_TOKEN={refresh_token}\n")
                found = True
            else:
                lines.append(line)
    if not found:
        lines.append(f"YT_REFRESH_TOKEN={refresh_token}\n")
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"\n[SUCCESS] Refresh token tersimpan di {ENV_PATH}")

def get_auth_url():
    env = load_env()
    client_id = env.get("GOOGLE_CLIENT_ID")
    if not client_id:
        raise ValueError("GOOGLE_CLIENT_ID belum diset di .env")
        
    redirect_uri = "http://localhost"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube",
        "access_type": "offline",
        "prompt": "consent",
        "login_hint": "ditawsyahn@gmail.com"
    }
    return f"https://accounts.google.com/o/oauth2/auth?{urllib.parse.urlencode(params)}"

def exchange_code(raw_input):
    env = load_env()
    client_id = env.get("GOOGLE_CLIENT_ID")
    client_secret = env.get("GOOGLE_CLIENT_SECRET")
    redirect_uri = "http://localhost"

    code = raw_input.strip()
    if "code=" in raw_input:
        parsed = urllib.parse.urlparse(raw_input)
        qs = urllib.parse.parse_qs(parsed.query)
        if "code" in qs:
            code = qs["code"][0]

    token_url = "https://oauth2.googleapis.com/token"
    token_data = urllib.parse.urlencode({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }).encode("utf-8")

    req = urllib.request.Request(token_url, data=token_data, headers={
        "Content-Type": "application/x-www-form-urlencoded"
    })
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        refresh_token = data.get("refresh_token")
        if refresh_token:
            save_refresh_token(refresh_token)
            return refresh_token
        else:
            print("[WARNING] Tidak ada refresh_token yang dikembalikan (apakah akun sudah pernah diotorisasi tanpa prompt=consent?):", data)
            return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "url":
            print(get_auth_url())
        elif sys.argv[1] == "exchange" and len(sys.argv) > 2:
            exchange_code(sys.argv[2])
    else:
        url = get_auth_url()
        print("="*65)
        print("  GOOGLE OAUTH2 SETUP FOR YOUTUBE (DITA-04 @ditafable)")
        print("  Target Account: ditawsyahn@gmail.com")
        print("="*65)
        print("\n1. Buka URL ini di browser (login akun ditawsyahn@gmail.com):\n")
        print(url)
        print("\n2. Setelah klik izinkan (Allow/Lanjutkan), browser diarahkan ke:")
        print("   http://localhost/?code=4/0A...&scope=...")
        print("3. Jalankan perintah berikut untuk menyimpan token:")
        print("   python auth_youtube.py exchange \"<URL_REDIRECT_ATAU_CODE>\"\n")
