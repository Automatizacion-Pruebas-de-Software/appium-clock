# Integración Completa en GitHub Actions

Te proporciono la integración completa con todos los tests:

## 1. Workflow completo para GitHub Actions

```yaml
# .github/workflows/appium-android-tests.yml
name: Appium Android Tests

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]
  schedule:
    - cron: '0 6 * * *'  # Ejecutar diariamente a las 6 AM UTC

jobs:
  appium-tests:
    name: Run Appium Android Tests
    runs-on: ubuntu-latest
    
    steps:
    # Paso 1: Checkout del código
    - name: Checkout repository
      uses: actions/checkout@v4

    # Paso 2: Configurar Java
    - name: Set up JDK 17
      uses: actions/setup-java@v4
      with:
        java-version: '17'
        distribution: 'temurin'

    # Paso 3: Configurar Android SDK
    - name: Setup Android SDK
      uses: android-actions/setup-android@v3

    # Paso 4: Crear y ejecutar emulador
    - name: Run Android Emulator
      uses: reactivecircus/android-emulator-runner@v2
      with:
        api-level: 34
        arch: x86_64
        profile: pixel_6
        target: google_apis
        emulator-options: -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim -camera-back none -camera-front none
        disable-animations: false
        script: |
          adb devices
          adb shell pm list packages | grep deskclock

    # Paso 5: Configurar Node.js
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'

    # Paso 6: Instalar Appium y dependencias
    - name: Install Appium and Python dependencies
      run: |
        npm install -g appium
        appium driver install uiautomator2
        pip install appium-python-client selenium

    # Paso 7: Iniciar Appium Server
    - name: Start Appium Server
      run: |
        appium --log-level info --relaxed-security --allow-insecure=adb_shell &
        APPIUM_PID=$!
        echo "APPIUM_PID=$APPIUM_PID" >> $GITHUB_ENV
        sleep 10
        echo "🚀 Appium server started"

    # Paso 8: Esperar a que el emulador esté listo
    - name: Wait for emulator
      run: |
        adb wait-for-device
        adb shell input keyevent 82
        echo "Emulator is ready"
        adb shell dumpsys window | grep -E 'mCurrentFocus'

    # Paso 9: Ejecutar suite de tests
    - name: Run Test Suite
      run: |
        python run_test_suite.py

    # Paso 10: Subir resultados y screenshots
    - name: Upload Test Artifacts
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-results
        path: |
          test-reports/
          *.png
        retention-days: 7

    # Paso 11: Limpiar proceso Appium
    - name: Cleanup Appium
      if: always()
      run: |
        if [ ! -z "$APPIUM_PID" ]; then
          kill $APPIUM_PID 2>/dev/null || true
        fi
```

## 2. Script de ejecución de tests completo

```python
# run_test_suite.py
import subprocess
import sys
import time
import os

def run_test(test_file, test_name):
    """Ejecuta un test individual y retorna el resultado"""
    print(f"\n{'='*60}")
    print(f"🚀 EJECUTANDO: {test_name}")
    print(f"📁 Archivo: {test_file}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos timeout
        )
        
        execution_time = time.time() - start_time
        
        print(result.stdout)
        if result.stderr:
            print(f"❌ ERRORES:\n{result.stderr}")
        
        success = result.returncode == 0
        status = "✅ PASÓ" if success else "❌ FALLÓ"
        
        print(f"\n⏱️  Tiempo ejecución: {execution_time:.2f}s")
        print(f"📊 Resultado: {status}")
        
        return success, execution_time
        
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT: {test_name} excedió el tiempo límite")
        return False, 300
    except Exception as e:
        print(f"💥 ERROR inesperado: {e}")
        return False, time.time() - start_time

def main():
    # Crear directorio para reportes
    os.makedirs("test-reports", exist_ok=True)
    
    # Suite de tests en orden de ejecución
    test_suite = [
        {
            "file": "test_crear_alarma_0730.py",
            "name": "Crear Alarma 07:30 AM"
        },
        {
            "file": "test_deshabilitar_alarma_1200.py", 
            "name": "Deshabilitar Alarma 12:00"
        }
    ]
    
    print("🎯 INICIANDO SUITE DE PRUEBAS APPIUM")
    print("📍 Entorno: GitHub Actions + Android Emulator")
    print(f"📋 Total de tests: {len(test_suite)}")
    
    results = []
    total_time = 0
    
    # Ejecutar cada test
    for test in test_suite:
        if os.path.exists(test["file"]):
            success, exec_time = run_test(test["file"], test["name"])
            results.append({
                "test": test["name"],
                "file": test["file"], 
                "success": success,
                "time": exec_time
            })
            total_time += exec_time
            
            # Pequeña pausa entre tests
            time.sleep(2)
        else:
            print(f"❌ Archivo no encontrado: {test['file']}")
            results.append({
                "test": test["name"],
                "file": test["file"],
                "success": False,
                "time": 0
            })
    
    # Generar reporte final
    print(f"\n{'='*60}")
    print("📊 REPORTE FINAL DE EJECUCIÓN")
    print(f"{'='*60}")
    
    passed = 0
    failed = 0
    
    for result in results:
        status = "✅ PASÓ" if result["success"] else "❌ FALLÓ"
        print(f"{result['test']}: {status} ({result['time']:.2f}s)")
        
        if result["success"]:
            passed += 1
        else:
            failed += 1
    
    print(f"\n🎯 RESUMEN:")
    print(f"   Total tests: {len(results)}")
    print(f"   ✅ Exitosos: {passed}")
    print(f"   ❌ Fallidos: {failed}")
    print(f"   ⏱️  Tiempo total: {total_time:.2f}s")
    print(f"   📈 Tasa de éxito: {(passed/len(results))*100:.1f}%")
    
    # Escribir reporte en archivo
    with open("test-reports/test-summary.md", "w") as f:
        f.write("# Reporte de Tests Appium\n\n")
        f.write(f"- **Fecha ejecución**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"- **Total tests**: {len(results)}\n")
        f.write(f"- **Tests exitosos**: {passed}\n")
        f.write(f"- **Tests fallidos**: {failed}\n")
        f.write(f"- **Tiempo total**: {total_time:.2f}s\n\n")
        
        f.write("## Detalle por test\n")
        for result in results:
            status = "PASÓ" if result["success"] else "FALLÓ"
            f.write(f"- {result['test']}: {status} ({result['time']:.2f}s)\n")
    
    # Exit code basado en resultados
    exit_code = 0 if failed == 0 else 1
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
```

## 3. Requirements.txt actualizado

```txt
# requirements.txt
appium-python-client>=2.0.0
selenium>=4.0.0
```

## 4. Archivos de tests individuales

- `test_crear_alarma_0730.py` (el que ya tienes adaptado para 07:30 AM)
- `test_deshabilitar_alarma_1200.py` (el que creamos para deshabilitar)

## 5. README.md con badge

```markdown
# Appium Android Tests

![Appium Tests](https://github.com/tu-usuario/tu-repositorio/actions/workflows/appium-android-tests.yml/badge.svg)

Suite de pruebas automatizadas para Google Clock en Android usando Appium.

## Tests incluidos

- ✅ Crear alarma 07:30 AM
- ✅ Deshabilitar alarma 12:00 PM

## Ejecución local

```bash
pip install -r requirements.txt
python run_test_suite.py
```

## Estructura

```
📁 .github/workflows/
└── appium-android-tests.yml  # CI/CD Pipeline

📁 test-reports/              # Resultados generados
├── test-summary.md
└── screenshots/

🐍 *.py                       # Scripts de tests
```

## Configuración

Requiere:
- Android Emulator (API 34)
- Appium Server
- Python 3.8+
```

## 6. Comandos para implementar

```bash
# Crear estructura de archivos
mkdir -p .github/workflows test-reports

# Crear/actualizar archivos
touch .github/workflows/appium-android-tests.yml
touch run_test_suite.py
touch requirements.txt
touch README.md

# Hacer commit y push
git add .
git commit -m "feat: Add complete Appium test suite with GitHub Actions"
git push origin main
```