# test_reloj_rapido.py
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
    wait = WebDriverWait(driver, 10)  # Reducido de 15 a 10 segundos

    print("→ Abriendo pestaña Alarm y pulsando FAB +")
    fab = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.google.android.deskclock:id/fab")))
    fab.click()

    # —— PICKER RAPIDO ——
    print("→ Configurando 12:00 en el picker radial")

    # 1. Toca el número 12 (selector directo ya que sabemos que funciona)
    hora_12 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='12']")))
    hora_12.click()
    time.sleep(0.3)  # Reducido de 0.5 a 0.3

    # 2. Toca el número 00 (selector directo)
    minuto_00 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='00']")))
    minuto_00.click()
    time.sleep(0.3)  # Reducido de 0.5 a 0.3

    # 3. Pulsa OK (selector directo)
    btn_ok = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='OK']")))
    btn_ok.click()

    # 4. Verifica que la alarma 12:00 aparece en la lista
    print("→ Verificando que la alarma 12:00 fue creada...")
    alarma = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@text, '12:00')]")))
    assert alarma.is_displayed()
    print("¡ÉXITO ABSOLUTO! Alarma 12:00 creada correctamente")

    time.sleep(2)  # Reducido de 5 a 2 segundos

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
    print("Prueba terminada")