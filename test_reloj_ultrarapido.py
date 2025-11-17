# test_reloj_ultrarapido.py
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "emulator-5554"
options.app_package = "com.google.android.deskclock"
options.app_activity = "com.android.deskclock.DeskClock"
options.no_reset = True

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

try:
    wait = WebDriverWait(driver, 8)  # Solo 8 segundos máximo

    print("→ Abriendo pestaña Alarm y pulsando FAB +")
    fab = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.google.android.deskclock:id/fab")))
    fab.click()

    print("→ Configurando 12:00 en el picker radial")

    # Sin delays entre clicks - WebDriverWait es suficiente
    hora_12 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='12']")))
    hora_12.click()

    minuto_00 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='00']")))
    minuto_00.click()

    btn_ok = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='OK']")))
    btn_ok.click()

    print("→ Verificando que la alarma 12:00 fue creada...")
    alarma = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@text, '12:00')]")))
    assert alarma.is_displayed()
    print("¡ÉXITO ABSOLUTO! Alarma 12:00 creada correctamente")

    time.sleep(1)  # Solo 1 segundo final para ver el resultado

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
    print("Prueba terminada")