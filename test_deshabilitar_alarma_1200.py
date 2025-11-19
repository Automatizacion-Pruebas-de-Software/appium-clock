# test_deshabilitar_alarma_1200.py
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

    print("→ Buscando la alarma 12:00 para deshabilitarla...")
    
    # Buscar la alarma 12:00 en diferentes formatos
    selectores_alarma = [
        "//*[contains(@text, '12:00')]",
        "//*[contains(@text, '12:00 AM')]",
        "//*[contains(@text, '12:00 PM')]"
    ]
    
    alarma_1200 = None
    for selector in selectores_alarma:
        try:
            alarma_1200 = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, selector)))
            print(f"→ Alarma 12:00 encontrada con: {selector}")
            break
        except:
            continue

    if alarma_1200:
        # Buscar el toggle switch de la alarma (usualmente cerca del texto de la hora)
        # Estrategia 1: Buscar el switch por ID común
        try:
            toggle_switch = alarma_1200.find_element(AppiumBy.XPATH, "./following-sibling::*//android.widget.Switch")
        except:
            # Estrategia 2: Buscar en el mismo contenedor
            try:
                toggle_switch = alarma_1200.find_element(AppiumBy.XPATH, "../..//android.widget.Switch")
            except:
                # Estrategia 3: Buscar por ID específico de Google Clock
                try:
                    toggle_switch = driver.find_element(AppiumBy.ID, "com.google.android.deskclock:id/onoff")
                except:
                    # Estrategia 4: Buscar cualquier switch en la lista de alarmas
                    try:
                        toggle_switch = driver.find_element(AppiumBy.XPATH, "//android.widget.Switch")
                    except:
                        toggle_switch = None

        if toggle_switch:
            # Verificar estado actual del switch
            estado_actual = toggle_switch.get_attribute("checked")
            if estado_actual == "true":
                print("→ Alarma está ACTIVA, deshabilitando...")
                toggle_switch.click()
                time.sleep(1)
                
                # Verificar que se deshabilitó
                estado_nuevo = toggle_switch.get_attribute("checked")
                if estado_nuevo == "false":
                    print("✅ ÉXITO: Alarma 12:00 deshabilitada correctamente")
                else:
                    print("❌ No se pudo deshabilitar la alarma")
            else:
                print("→ La alarma 12:00 ya está deshabilitada")
        else:
            print("❌ No se encontró el toggle switch para deshabilitar")
    else:
        print("❌ No se encontró la alarma 12:00")

    time.sleep(2)

except Exception as e:
    print(f"Error: {e}")
    # Tomar screenshot para debugging
    driver.save_screenshot("error_deshabilitar.png")
finally:
    driver.quit()
    print("Prueba terminada")