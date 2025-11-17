# Instalación de Simulador Android

**Command Line Tools + SDK Manager + AVD Manager**

**Peso final instalado:** ~1.5 – 2.5 GB (vs 10 GB de Android Studio completo)

## Pasos detallados para Windows 11/10 y macOS (2025)

---

## OPCIÓN A – WINDOWS (la más ligera)

### 1. Descarga solo las Command Line Tools (700 MB)

* **URL oficial (siempre actualizada):** https://developer.android.com/studio → baja hasta "Command line tools only"
* **Descarga:** `commandlinetools-win-xxxx_latest.zip`

### 2. Crea la carpeta e instala
```powershell
# Abre PowerShell como usuario normal (no necesitas admin)
cd C:\          # o donde quieras, yo uso C:\Android
mkdir Android
cd Android
# Descomprime el zip aquí → crea una subcarpeta llamada "cmdline-tools"
# La estructura final debe quedar:
# C:\Android\cmdline-tools\tools\...
# ↳ MUY IMPORTANTE: renombra la carpeta descomprimida a "tools"
# Final: C:\Android\cmdline-tools\tools
```

### 3. Configura variables de entorno (Windows)

* Presiona **Win** → escribe "Variables de entorno" → "Editar las variables de entorno del sistema"
* En "Variables del sistema" → haz clic en "Nuevo…" tres veces y agrega:

| Nombre de variable | Valor (ajusta si cambiaste ruta) |
|-------------------|----------------------------------|
| ANDROID_HOME | C:\Android |
| PATH (agregar al final) | C:\Android\cmdline-tools\tools\bin |
| PATH (agregar al final) | C:\Android\cmdline-tools\tools\lib |

También agrega al PATH estas dos (cuando las crees más adelante):
```text
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\emulator
```

### 4. Instala el SDK desde consola
```powershell
# Verifica que funcione
sdkmanager --version

# Acepta licencias automáticamente
sdkmanager --licenses --sdk_root=C:\Android

# Instala lo mínimo necesario (platform-tools + una versión de Android + emulator)
sdkmanager --sdk_root=C:\Android `
  "platform-tools" `
  "platforms;android-34" `
  "emulator" `
  "system-images;android-34;google_apis;x86_64"
```

### 5. Crea un emulador (AVD) ligero
```powershell
avdmanager create avd -n Pixel_6_API_34 -k "system-images;android-34;google_apis;x86_64" -d pixel_6
```

### 6. Inicia el emulador
```powershell
emulator -avd Pixel_6_API_34
```

(La primera vez tarda 2-3 minutos, luego es rápido)

---

## OPCIÓN B – macOS (Intel o Apple Silicon)

### 1. Descarga Command Line Tools para Mac

https://developer.android.com/studio → "Command line tools only" → mac

### 2. Descomprime y estructura
```bash
cd ~
mkdir -p ~/Android
cd ~/Android
unzip ~/Downloads/commandlinetools-mac-xxxx_latest.zip
mkdir -p cmdline-tools
mv cmdline-tools/tools cmdline-tools/tools   # renombrar
```

### 3. Variables de entorno (macOS)

Abre la terminal y edita tu shell:

Si usas **zsh** (macOS por defecto desde 2019):
```bash
nano ~/.zshrc
```

Agrega estas líneas:
```bash
export ANDROID_HOME=$HOME/Android
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/emulator
```

Guarda (Ctrl+O → Enter → Ctrl+X) y aplica:
```bash
source ~/.zshrc
```

### 4. Instala SDK (igual que Windows)
```bash
sdkmanager --version
sdkmanager --licenses --sdk_root=$HOME/Android
sdkmanager --sdk_root=$HOME/Android \
  "platform-tools" \
  "platforms;android-34" \
  "emulator" \
  "system-images;android-34;google_apis;arm64-v8a"    # Apple Silicon
  # o usa x86_64 si es Intel Mac
```

### 5. Crea y abre emulador
```bash
avdmanager create avd -n Pixel_6_API_34 -k "system-images;android-34;google_apis;arm64-v8a" -d pixel_6
emulator -avd Pixel_6_API_34
```

---

## Resumen: ¿Qué instalaste y cuánto pesa?

| Componente | Peso aproximado |
|-----------|----------------|
| Command line tools | 700 MB |
| platform-tools | 50 MB |
| emulator + imagen Android 34 | 800 MB – 1.2 GB |
| **Total** | **~2 GB máximo** |

---

¡Listo! Ya tienes todo lo necesario para que Appium funcione perfectamente (`adb`, `emulator`, `avd`, etc.) sin instalar Android Studio completo.