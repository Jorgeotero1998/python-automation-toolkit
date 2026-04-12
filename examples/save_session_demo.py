import sys
import os
from playwright.sync_api import sync_playwright

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser import BrowserManager
from core.sessions import SessionPersistor
from utils.logger import get_logger

log = get_logger("SessionDemo")

def run():
    session_name = "github_session"  # Ejemplo con GitHub
    with sync_playwright() as p:
        mgr = BrowserManager()
        persistor = SessionPersistor()
        
        # 1. Intentar cargar sesión existente
        existing_session = persistor.load_session(session_name)
        
        if existing_session:
            log.info("Cargando sesión existente...")
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(storage_state=existing_session)
        else:
            log.info("No hay sesión. Iniciando login manual...")
            browser, context = mgr.launch_stealth_context(p, headless=False)
        
        page = context.new_page()
        page.goto("https://github.com/login")
        
        # Si no estamos logueados, esperamos a que el usuario lo haga
        if not existing_session:
            log.info("Por favor, logueate manualmente en la ventana del navegador.")
            log.info("Esperando a que detectemos el dashboard...")
            page.wait_for_url("https://github.com/", timeout=60000)
            persistor.save_session(context, session_name)
            log.info("Sesión guardada con éxito.")
        else:
            log.info("Logueado automáticamente mediante cookies.")
            page.wait_for_timeout(5000)

        browser.close()

if __name__ == "__main__":
    run()
