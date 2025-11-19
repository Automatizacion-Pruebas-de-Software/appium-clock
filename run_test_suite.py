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