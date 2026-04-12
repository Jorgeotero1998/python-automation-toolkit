import requests
import time
from playwright.sync_api import Page

class CaptchaSolver:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._url = "http://2captcha.com"

    def solve_recaptcha_v2(self, page: Page, site_key: str):
        payload = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page.url,
            'json': 1
        }
        try:
            resp = requests.post(f"{self._url}/in.php", data=payload).json()
            if resp.get("status") != 1: return False
            job_id = resp.get("request")
            while True:
                time.sleep(5)
                res = requests.get(f"{self._url}/res.php?key={self.api_key}&action=get&id={job_id}&json=1").json()
                if res.get("status") == 1:
                    token = res.get("request")
                    page.evaluate(f'document.getElementById("g-recaptcha-response").innerHTML="{token}";')
                    return True
                if res.get("request") != "CAPCHA_NOT_READY": return False
        except:
            return False
