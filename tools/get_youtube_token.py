#!/usr/bin/env python3
"""
Get a read-only YouTube Analytics refresh token for the MN Cousins channel.

Run this on YOUR OWN computer (not in the chat). It opens a browser window,
you sign in with the Google account that owns the channel, and the script
prints three values to your terminal. Store them as secrets in the Claude
cloud environment settings — never paste them into a chat.

Usage:
    python3 get_youtube_token.py

Requirements: Python 3.8+ only (standard library, nothing to install).
Scopes requested (read-only):
    https://www.googleapis.com/auth/yt-analytics.readonly
    https://www.googleapis.com/auth/youtube.readonly
"""
import getpass
import hashlib
import base64
import http.server
import json
import secrets
import urllib.parse
import urllib.request
import webbrowser

SCOPES = " ".join([
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.readonly",
])
PORT = 8765
REDIRECT = f"http://127.0.0.1:{PORT}/"


def main():
    print("Paste the OAuth client values from Google Cloud Console (input is hidden).")
    client_id = input("Client ID: ").strip()
    client_secret = getpass.getpass("Client secret: ").strip()

    state = secrets.token_urlsafe(16)
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    })

    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] != state:
                self.send_response(400); self.end_headers()
                self.wfile.write(b"State mismatch. Close this tab and run the script again.")
                return
            result["code"] = q.get("code", [""])[0]
            result["error"] = q.get("error", [""])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("تم. ارجع للطرفية (Terminal). Done — return to the terminal.".encode())

        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    print("\nOpening your browser. Sign in with the account that owns MN Cousins…")
    print("If it does not open, visit:\n" + auth_url + "\n")
    webbrowser.open(auth_url)
    while "code" not in result:
        server.handle_request()
    server.server_close()

    if result.get("error") or not result.get("code"):
        raise SystemExit(f"Authorization failed: {result.get('error') or 'no code returned'}")

    data = urllib.parse.urlencode({
        "code": result["code"],
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": REDIRECT,
        "grant_type": "authorization_code",
        "code_verifier": verifier,
    }).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data, timeout=30) as r:
        token = json.load(r)

    refresh = token.get("refresh_token")
    if not refresh:
        raise SystemExit("No refresh token returned. Remove the app's access at "
                         "https://myaccount.google.com/permissions and run again.")

    print("\n✅ Success. Add these three secrets to the Claude environment settings:")
    print("   YT_CLIENT_ID      =", client_id)
    print("   YT_CLIENT_SECRET  = (the client secret you entered)")
    print("   YT_REFRESH_TOKEN  =", refresh)
    print("\nDo NOT paste them into any chat.")


if __name__ == "__main__":
    main()
