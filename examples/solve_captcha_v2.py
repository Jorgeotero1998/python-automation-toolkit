import sys
import os
from playwright.sync_api import sync_playwright

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import BrowserManager
from utils.logger import get_logger, take_error_screenshot

log = get_logger("ProductionBot")

def run():
    with sync_playwright() as p:
        mgr = BrowserManager()
        browser, context = mgr.launch_stealth_context(p, headless=False)
        page = context.new_page()
        
        try:
            log.info("Iniciando tarea crítica...")
            page.goto("https://www.google.com/recaptcha/api2/demo")
            
            # Forzamos un error o una acción
            if page.query_selector(".g-recaptcha"):
                log.info("Formulario detectado.")
                mgr.human_click(page, "#recaptcha-demo-submit")
            else:
                raise Exception("No se encontró el elemento esperado")
                
        except Exception as e:
            log.error(f"Error en la ejecución: {e}")
            path = take_error_screenshot(page, "critical_failure")
            log.info(f"Captura de error guardada en: {path}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
