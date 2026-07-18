import os
import json
import requests
from pathlib import Path

COOKIE_CACHE_PATH = Path("data/nfpa_cookies.json")

class NFPAConnector:
    def __init__(self):
        self.session = requests.Session()
        self.username = os.environ.get("NFPA_USERNAME", "")
        self.password = os.environ.get("NFPA_PASSWORD", "")
        self.login_url = os.environ.get("NFPA_LOGIN_URL", "https://link.nfpa.org/login-endpoint")
        self.search_url = os.environ.get("NFPA_SEARCH_URL", "https://link.nfpa.org/api/search")
        
        # Load cached cookies if they exist
        self._load_cached_cookies()

    def _load_cached_cookies(self):
        if COOKIE_CACHE_PATH.exists():
            try:
                with open(COOKIE_CACHE_PATH, "r") as f:
                    cookies_dict = json.load(f)
                    requests.utils.cookiejar_from_dict(cookies_dict, self.session.cookies)
                print("Loaded cached NFPA session cookies.")
            except Exception as e:
                print(f"Failed to load cached cookies: {e}")

    def _save_cookies(self):
        COOKIE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        try:
            with open(COOKIE_CACHE_PATH, "w") as f:
                json.dump(cookies_dict, f)
            print("Saved active NFPA session cookies to cache.")
        except Exception as e:
            print(f"Failed to save cookies to cache: {e}")

    def login(self):
        if not self.username or not self.password:
            print("Credentials missing. Cannot log in to NFPA.")
            return False

        payload = {
            "username": self.username,
            "password": self.password
        }
        try:
            print(f"Attempting login to NFPA at {self.login_url}...")
            response = self.session.post(self.login_url, json=payload, timeout=10)
            response.raise_for_status()
            
            # Save new cookies
            self._save_cookies()
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def search_regulations(self, query):
        if not query or not query.strip():
            return []

        # Check if session is valid by hitting the search or checking cookies
        # (If no cookies or search fails with 401/403, trigger login)
        if not self.session.cookies:
            self.login()

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        params = {"q": query}

        try:
            response = self.session.get(self.search_url, headers=headers, params=params, timeout=10)
            
            # Handle expired session/unauthorized
            if response.status_code in [401, 403]:
                print("Session expired or unauthorized. Re-authenticating...")
                if self.login():
                    response = self.session.get(self.search_url, headers=headers, params=params, timeout=10)
            
            response.raise_for_status()
            data = response.json()
            
            # Return parsed search results
            return data.get("results", [])
        except Exception as e:
            print(f"NFPA search request failed: {e}")
            return []
