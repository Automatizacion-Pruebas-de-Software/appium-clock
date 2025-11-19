# test_reloj_rapido_0730.py
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
    wait = WebDriverWait(driver, 10)

    print("→ Abriendo pestaña Alarm y pulsando FAB +")
    fab = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.google.android.deskclock:id/fab")))
    fab.click()

    # —— PICKER RAPIDO para 07:30 AM ——
    print("→ Configurando 07:30 AM en el picker radial")

    # 1. Toca el número 7 (hora)
    hora_7 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='7']")))
    hora_7.click()
    time.sleep(0.3)

    # 2. Toca el número 30 (minutos)
    minuto_30 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='30']")))
    minuto_30.click()
    time.sleep(0.3)

    # 3. Verificar que esté en AM (si no lo está, cambiar a AM)
    try:
        # Buscar el indicador AM/PM y asegurarse que sea AM
        am_pm_indicator = driver.find_element(AppiumBy.XPATH, "//*[contains(@text, 'AM') or contains(@text, 'PM')]")
        current_am_pm = am_pm_indicator.text
        
        if "PM" in current_am_pm:
            print("→ Cambiando de PM a AM")
            am_pm_indicator.click()  # Click para cambiar AM/PM
            time.sleep(0.3)
    except:
        print("→ No se encontró selector AM/PM, continuando...")

    # 4. Pulsa OK
    btn_ok = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@text='OK']")))
    btn_ok.click()

    # 5. Verifica que la alarma 07:30 AM aparece en la lista
    print("→ Verificando que la alarma 07:30 AM fue creada...")
    
    # Buscar diferentes formatos posibles de la hora
    selectores_hora = [
        "//*[contains(@text, '7:30')]",
        "//*[contains(@text, '07:30')]",
        "//*[contains(@text, '7:30 AM')]",
        "//*[contains(@text, '07:30 AM')]"
    ]
    
    alarma = None
    for selector in selectores_hora:
        try:
            alarma = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, selector)))
            print(f"→ Alarma encontrada con selector: {selector}")
            break
        except:
            continue
    
    if alarma and alarma.is_displayed():
        print("¡ÉXITO ABSOLUTO! Alarma 07:30 AM creada correctamente")
    else:
        print("❌ No se pudo verificar la alarma 07:30 AM")

    time.sleep(2)

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
    print("Prueba terminada")