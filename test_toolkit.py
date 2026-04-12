import sys
import os
from playwright.sync_api import sync_playwright

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.browser import BrowserManager
from utils.logger import get_logger, take_error_screenshot
from utils.helpers import random_sleep, scroll_down_human

log = get_logger("DuckRunner")

def run_test():
    with sync_playwright() as p:
        mgr = BrowserManager()
        # headless=False para ver la magia
        browser, context, page = mgr.launch_stealth_context(p, headless=False)
        
        try:
            log.info("Navegando a DuckDuckGo (Entorno seguro para tests)...")
            page.goto("https://duckduckgo.com")
            random_sleep(1, 2)
            
            log.info("Buscando perfil profesional...")
            # El selector de DuckDuckGo para la barra de búsqueda es #search_form_input_homepage o similar
            search_selector = "input[name='q']"
            mgr.human_type(page, search_selector, "Jorge Otero Full Stack Developer")
            page.keyboard.press("Enter")
            
            log.info("Esperando resultados...")
            page.wait_for_load_state("networkidle")
            
            log.info("Simulando lectura humana (Scroll)...")
            scroll_down_human(page)
            random_sleep(2, 4)
            
            log.info("Prueba de fuego exitosa.")
            
        except Exception as e:
            log.error(f"Error inesperado: {e}")
            take_error_screenshot(page, "duck_failure")
        finally:
            log.info("Cerrando navegador.")
            browser.close()

if __name__ == "__main__":
    run_test()
