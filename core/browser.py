import random
import time
import os
from playwright.sync_api import sync_playwright, Playwright
import playwright_stealth

class BrowserManager:
    def __init__(self):
        self._user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
        self.proxy_file = "proxies.txt"

    def launch_stealth_context(self, playwright: Playwright, headless=False, use_proxy=False):
        proxy = None
        if use_proxy and os.path.exists(self.proxy_file):
            with open(self.proxy_file, "r") as f:
                proxies = [line.strip() for line in f if line.strip()]
                if proxies:
                    proxy = {"server": random.choice(proxies)}

        browser = playwright.chromium.launch(headless=headless, proxy=proxy)
        context = browser.new_context(
            user_agent=random.choice(self._user_agents),
            viewport={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        
        # TÉCNICA DE FUERZA BRUTA: Probamos todas las variantes de la librería
        try:
            from playwright_stealth import stealth
            stealth(page)
        except:
            try:
                playwright_stealth.stealth_sync(page)
            except:
                try:
                    from playwright_stealth import Stealth
                    Stealth(page)
                except:
                    # Si todo falla, imprimimos el error pero seguimos para no frenar el bot
                    print("Advertencia: No se pudo aplicar el modo Stealth, continuando de todas formas.")
        
        return browser, context, page

    def human_type(self, page, selector, text):
        page.wait_for_selector(selector)
        for char in text:
            page.type(selector, char, delay=random.randint(100, 250))
            
    def human_click(self, page, selector):
        page.wait_for_selector(selector)
        page.hover(selector)
        time.sleep(random.uniform(0.2, 0.5))
        page.click(selector)
