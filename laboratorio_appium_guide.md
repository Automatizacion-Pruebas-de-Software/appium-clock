# Paso 1: Requisitos (todo gratis)

1. **Instala VSCode** → https://code.visualstudio.com/
2. **Instala Python 3.11 o 3.12** → https://www.python.org/downloads/
3. **Instala Node.js (viene con npm)** → https://nodejs.org/es/ (elige LTS)
4. **Android Studio (solo necesitas el SDK y un emulador)** → https://developer.android.com/studio

---

## Paso 2: Instalar Appium y dependencias (una sola terminal)

Abre una terminal (PowerShell o CMD como administrador) y pega esto de una vez:
```bash
npm install -g appium
npm install -g appium-doctor
pip install Appium-Python-Client
appium driver install uiautomator2
appium plugin install images
```

Luego verifica que todo esté bien:
```bash
appium-doctor --android
```

Si todo sale ✓ estás listo.

---

## Paso 3: Crear el proyecto en VSCode

1. Abre VSCode → **File** → **New Folder** → llámalo `appium-calculadora`
2. Abre ese folder en VSCode
3. Abre terminal integrada (Ctrl + ñ) y crea entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux
pip install Appium-Python-Client pytest
```

---

## Paso 4: Código completo (un solo archivo)

Crea un archivo llamado `test_calculadora.py`
```python
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración del dispositivo/emulador Android
desired_caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "emulator-5554",      # cambia si tu emulador tiene otro nombre
    "appPackage": "com.android.calculator2",
    "appActivity": "com.android.calculator2.Calculator"
}

# Inicia Appium (asegúrate de tener el servidor corriendo: appium &)
driver = webdriver.Remote("http://127.0.0.1:4723", desired_caps)

try:
    wait = WebDriverWait(driver, 15)

    # Pulsar 2
    btn2 = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.android.calculator2:id/digit_2")))
    btn2.click()

    # Pulsar +
    btn_plus = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "plus")
    btn_plus.click()

    # Pulsar 5
    driver.find_element(AppiumBy.ID, "com.android.calculator2:id/digit_5").click()

    # Pulsar =
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "equals").click()

    # Verificar resultado = 7
    resultado = wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.android.calculator2:id/result_final")))
    assert resultado.text == "7"
    print("¡Prueba pasada! 2 + 5 = 7")

    time.sleep(2)

finally:
    driver.quit()
```

---

## Paso 5: Ejecutar todo

1. Abre un emulador Android o conecta tu celular con modo desarrollador + USB debugging
```bash
emulator -avd Pixel_6_API_34
```

2. En una terminal ejecuta el servidor Appium:
```bash
appium
```

(deja esa terminal abierta)
3. En otra terminal (dentro de VSCode) ejecuta:
```bash
python test_calculadora.py
```