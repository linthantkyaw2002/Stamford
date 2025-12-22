# FaceRecorder (macOS)

**Author:** Lin Thant Kyaw  
**Affiliation:** Stamford International University  

FaceRecorder is a macOS application for collecting **high-quality face image datasets** using a webcam.
It can run as a **Python script** or be packaged as a **clickable macOS `.app`** using PyInstaller.

This README is a **step-by-step full guide**:
- install from zero (no Homebrew required)
- run the script
- build the `.app`
- fix common macOS camera / MediaPipe issues
- use the app correctly to capture datasets

## Download full package
https://drive.google.com/drive/folders/1L7SADejKKrF1rZjrFCaZEuse95eGR_X-?usp=sharing

## 1) What this app does ##

For each person:
- asks for a name (Tkinter popup)
- calibrates neutral head pose (~1 second)
- captures images while you move your head
- saves to:
~/Documents/FaceRecorder/data/<PersonName>/

Images:
- **100 images per person**
- **256 × 256**
- JPG format
- cropped to a tight 1:1 face/head square

## 2) Requirements ##

### macOS
- macOS (Apple Silicon or Intel)
- Camera/webcam available
- Camera permission enabled

### Python
- Python **3.10 – 3.11** recommended  
Check your version:

python3 --version

### Python packages (must)
- `mediapipe == 0.10.14` (important)
- `opencv-python`
- `numpy`
- `pyinstaller` (only needed for building the `.app`)

 **Why mediapipe must be pinned:**  
Some MediaPipe builds install but do !not expose `mp.solutions`!, causing:
`AttributeError: module 'mediapipe' has no attribute 'solutions'`

## 3) Project structure ##

Recommended folder:
FaceRecorderApp/
  app.py
  .venv/
Your script file should be named:
- `app.py`

## 4) Setup (from zero, no Homebrew) ##

### 4.1 Create folder and go inside
mkdir -p ~/FaceRecorderApp
cd ~/FaceRecorderApp

### 4.2 Put your code into `app.py`
(Your FaceRecorder code goes in this file.)

### 4.3 Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

You should see `(.venv)` in Terminal.

### 4.4 Upgrade pip
pip install --upgrade pip

### 4.5 Install dependencies (IMPORTANT pinned MediaPipe)
pip uninstall -y mediapipe
pip install mediapipe==0.10.14 opencv-python numpy

(Optional but recommended for building later)
pip install pyinstaller


## 5) Verify installation ##

### 5.1 Confirm MediaPipe exposes `solutions`
python - <<'PY'
import mediapipe as mp
print("MediaPipe file:", mp.__file__)
print("Has solutions:", hasattr(mp, "solutions"))
PY

Expected:
Has solutions: True


If it prints `False`, reinstall MediaPipe exactly:
pip uninstall -y mediapipe
pip install mediapipe==0.10.14

### 5.2 Confirm OpenCV loads and camera backend works
python - <<'PY'
import cv2
print("OpenCV version:", cv2.__version__)
PY

## 6) Run as a Python script ##

From inside the project folder:

source .venv/bin/activate
python app.py

### 6.1 macOS camera permission (script mode)
The first time you run it, macOS may ask for camera permission for:
- Terminal (or your Python IDE)
- allow it in: **System Settings → Privacy & Security → Camera**

If the camera is busy:
- close Zoom / Google Meet / FaceTime
- then run again

## 7) How to use the app (dataset recording) ##

1. When prompted, enter the person name  
2. Look straight at the camera for ~1 second (calibration)
3. Slowly move head:
   - center, left, right, up, down
   - diagonals (up-left, up-right, down-left, down-right)
4. The app automatically saves images when quality is OK
5. Press **Q** to stop early
6. Confirm if you want to add another person

### Output check
Open Finder → Documents → FaceRecorder → data  
You should see:
data/
  Alice/
    Alice_0001.jpg
    ...


## 8) Build a clickable macOS `.app` (PyInstaller) ##

### 8.1 Clean previous builds
From project folder:

rm -rf build dist *.spec

If your shell says `no matches found: *.spec`, that’s OK (it means no spec file exists yet).

### 8.2 Build the `.app`
**Important:** MediaPipe includes model files (`.binarypb`) that must be bundled.

Run:
pyinstaller --noconfirm --windowed \
  --name FaceRecorder \
  --osx-bundle-identifier com.facerecorder.app \
  --collect-all mediapipe \
  --collect-data mediapipe \
  --collect-submodules mediapipe \
  app.py

After success, you will get:
dist/FaceRecorder.app

### 8.3 Add camera permission to Info.plist (required)
macOS requires `NSCameraUsageDescription` or your app will not request permission.

Run:

/usr/libexec/PlistBuddy -c "Add :NSCameraUsageDescription string 'This app needs camera access to record face images.'" \
"dist/FaceRecorder.app/Contents/Info.plist" 2>/dev/null || \
/usr/libexec/PlistBuddy -c "Set :NSCameraUsageDescription 'This app needs camera access to record face images.'" \
"dist/FaceRecorder.app/Contents/Info.plist"

Verify:
/usr/libexec/PlistBuddy -c "Print :NSCameraUsageDescription" "dist/FaceRecorder.app/Contents/Info.plist"

### 8.4 Remove quarantine (Gatekeeper)
xattr -dr com.apple.quarantine dist/FaceRecorder.app


### 8.5 Ad-hoc sign the app (recommended)
This prevents many “crash on open” issues and helps permissions behave better.

codesign --force --deep --sign - dist/FaceRecorder.app


### 8.6 Run the app

open dist/FaceRecorder.app


### 8.7 Debug if it closes immediately
Run the internal executable directly to see errors:

./dist/FaceRecorder.app/Contents/MacOS/FaceRecorder

## 9) Common problems & fixes ##

### Problem A: `AttributeError: module 'mediapipe' has no attribute 'solutions'`
Cause: wrong/broken MediaPipe version installed.

Fix:
pip uninstall -y mediapipe
pip install mediapipe==0.10.14

### Problem B: App opens then closes, missing `.binarypb`
Example error:
`FileNotFoundError: ... face_landmark_front_cpu.binarypb`

Cause: PyInstaller did not bundle MediaPipe models.

Fix:
Rebuild with:
- `--collect-all mediapipe`
- `--collect-data mediapipe`
- `--collect-submodules mediapipe`

Then rebuild from clean:
rm -rf build dist *.spec
pyinstaller --noconfirm --windowed \
  --name FaceRecorder \
  --osx-bundle-identifier com.facerecorder.app \
  --collect-all mediapipe \
  --collect-data mediapipe \
  --collect-submodules mediapipe \
  app.py

### Problem C: No camera permission prompt for `.app`
Cause: missing `NSCameraUsageDescription` in Info.plist.

Fix: run Section 8.3 again, then:
xattr -dr com.apple.quarantine dist/FaceRecorder.app
codesign --force --deep --sign - dist/FaceRecorder.app
open dist/FaceRecorder.app

### Problem D: Camera not opening
Fix checklist:
- System Settings → Privacy & Security → Camera → allow FaceRecorder (and/or Terminal)
- Close any app using camera (Zoom, Meet, FaceTime)
- Reboot if the camera driver is stuck

## 10) Notes for reproducibility ##

Recommended pinned versions (works well on macOS):
- `mediapipe==0.10.14`
- `opencv-python` (latest)
- `numpy` (latest)
- `pyinstaller` (latest)

To freeze current versions:

pip freeze > requirements.txt

To reinstall later:

pip install -r requirements.txt

## 11) License ##
Educational and personal use only.
