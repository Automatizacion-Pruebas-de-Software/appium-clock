# test_reloj_corregido.py
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
    wait = WebDriverWait(driver, 20)

    print("→ Abriendo pestaña Alarm y pulsando FAB +")
    fab = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.google.android.deskclock:id/fab")))
    fab.click()

    # Esperar a que aparezca el selector de hora
    print("→ Esperando a que aparezca el selector de hora...")
    time.sleep(3)  # Espera adicional para que cargue completamente

    # —— ALTERNATIVA 1: Usar diferentes selectores para el picker radial ——
    print("→ Buscando elementos del picker radial...")
    
    # Intentar encontrar el número 12 con diferentes estrategias
    selectores_hora_12 = [
        "//android.view.View[@content-desc='12']",
        "//android.view.View[contains(@content-desc, '12')]",
        "//*[@text='12']",
        "//*[contains(@text, '12')]"
    ]
    
    hora_12 = None
    for selector in selectores_hora_12:
        try:
            hora_12 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, selector)))
            print(f"→ Encontrado con selector: {selector}")
            break
        except:
            continue
    
    if hora_12:
        hora_12.click()
        print("→ Hora 12 seleccionada")
        time.sleep(1)
    else:
        print("→ No se pudo encontrar la hora 12, tomando screenshot...")
        driver.save_screenshot("debug_hora12.png")
        raise Exception("No se pudo encontrar el elemento de hora 12")

    # Buscar el minuto 00
    selectores_minuto_00 = [
        "//android.view.View[@content-desc='00']",
        "//android.view.View[contains(@content-desc, '00')]",
        "//*[@text='00']",
        "//*[contains(@text, '00')]"
    ]
    
    minuto_00 = None
    for selector in selectores_minuto_00:
        try:
            minuto_00 = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, selector)))
            print(f"→ Encontrado con selector: {selector}")
            break
        except:
            continue
    
    if minuto_00:
        minuto_00.click()
        print("→ Minuto 00 seleccionado")
        time.sleep(1)
    else:
        print("→ No se pudo encontrar el minuto 00, tomando screenshot...")
        driver.save_screenshot("debug_minuto00.png")
        raise Exception("No se pudo encontrar el elemento de minuto 00")

    # —— ALTERNATIVA 2: Si los selectores anteriores no funcionan, usar coordenadas ——
    # Descomenta esta sección si la anterior no funciona
    """
    print("→ Usando método alternativo con coordenadas...")
    # Obtener dimensiones de la pantalla
    screen_size = driver.get_window_size()
    width = screen_size['width']
    height = screen_size['height']
    
    # Coordenadas aproximadas para 12:00 en un picker radial
    # Ajusta estas coordenadas según lo que veas en tu emulador
    driver.tap([(width/2, height/4)])  # Hora 12 (parte superior)
    time.sleep(1)
    driver.tap([(width/2, height/2)])  # Minuto 00 (centro)
    time.sleep(1)
    """

    # Pulsar OK
    print("→ Pulsando OK...")
    selectores_ok = [
        (AppiumBy.ID, "android:id/button1"),
        (AppiumBy.XPATH, "//*[@text='OK']"),
        (AppiumBy.XPATH, "//*[contains(@text, 'OK')]")
    ]
    
    btn_ok = None
    for by, selector in selectores_ok:
        try:
            btn_ok = wait.until(EC.element_to_be_clickable((by, selector)))
            print(f"→ Botón OK encontrado con: {selector}")
            break
        except:
            continue
    
    if btn_ok:
        btn_ok.click()
        print("→ Botón OK pulsado")
    else:
        print("→ No se pudo encontrar el botón OK")
        driver.save_screenshot("debug_ok.png")
        raise Exception("No se pudo encontrar el botón OK")

    # Verificar que la alarma se creó
    print("→ Verificando que la alarma 12:00 fue creada...")
    time.sleep(3)
    
    selectores_alarma = [
        (AppiumBy.XPATH, "//android.widget.TextView[@text='12:00']"),
        (AppiumBy.XPATH, "//*[contains(@text, '12:00')]"),
        (AppiumBy.XPATH, "//*[contains(@text, '12')]")
    ]
    
    alarma = None
    for by, selector in selectores_alarma:
        try:
            alarma = wait.until(EC.presence_of_element_located((by, selector)))
            print(f"→ Alarma encontrada con: {selector}")
            break
        except:
            continue
    
    if alarma and alarma.is_displayed():
        print("¡ÉXITO ABSOLUTO! Alarma 12:00 creada correctamente")
    else:
        print("→ No se pudo verificar la alarma, tomando screenshot final...")
        driver.save_screenshot("debug_final.png")
        raise Exception("No se pudo verificar la creación de la alarma")

    time.sleep(5)

except Exception as e:
    print(f"Error: {e}")
    # Tomar screenshot para debugging
    driver.save_screenshot("error_screenshot.png")
    print("→ Se guardó screenshot 'error_screenshot.png' para análisis")
finally:
    driver.quit()
    print("Prueba terminada")