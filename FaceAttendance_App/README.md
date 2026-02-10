# FaceAttendance — macOS Standalone App Build Guide (Apple Silicon)
Author: Lin Thant Kyaw
Project: FaceAttendance at Stamford International University
Full package google drive: https://drive.google.com/file/d/1wU3xUCG_f6R7FmmYQKFhqWK1V9yZymGN/view?usp=sharing

This document provides a complete, professional, and reproducible guide for converting the **FaceAttendance** Python application into a native **macOS `.app` bundle** on **Apple Silicon (M1/M2)**.

It is based on real development experience and includes:

* Exact build steps
* Architectural decisions
* Common failure modes encountered during development
* The rationale behind the final, working PyInstaller configuration

The intended audience is developers building **computer vision or machine learning desktop applications** on macOS.

---

## 1. Project Overview

**FaceAttendance** is a desktop-based face recognition attendance system with the following capabilities:

* Multi-angle face recording and dataset creation
* Face embedding generation using FaceNet
* Real-time face recognition using MTCNN and k-NN
* Attendance logging to CSV
* Tkinter-based graphical interface
* OpenCV-based live video capture and visualization

### Core Technologies

* Python 3.10.11 (ARM64)
* OpenCV
* MediaPipe (FaceMesh and FaceDetection)
* MTCNN
* FaceNet (keras-facenet)
* TensorFlow with Metal acceleration
* scikit-learn
* Tkinter

---

## 2. Target Platform

This guide applies specifically to:

* macOS
* Apple Silicon hardware (M1 / M2)
* Python ARM64 builds downloaded from python.org

Using Intel Python, Rosetta, or mixed Homebrew environments will result in build or runtime failures.

---

## 3. Python Environment Setup

### 3.1 Verify Python Architecture

```bash
python3 --version
python3 -c "import platform; print(platform.machine())"
```

Expected output:

```
Python 3.10.11
arm64
```

---

### 3.2 Create and Activate Virtual Environment

```bash
python3 -m venv faceapp_env
source faceapp_env/bin/activate

pip install --upgrade pip setuptools wheel
```

---

### 3.3 Install Required Packages

Package installation order is important:

```bash
pip install numpy==1.26.4
pip install opencv-python==4.9.0.80
pip install mediapipe==0.10.9
pip install mtcnn
pip install keras-facenet
pip install scikit-learn
pip install tensorflow-macos==2.15.0
pip install tensorflow-metal
pip install pillow
pip install pyinstaller
```

The `torch` package must not be installed; it is intentionally excluded from the final application.

---

## 4. Code-Level Adjustments for macOS Packaging

### 4.1 Matplotlib Stub

MediaPipe pulls matplotlib as a transitive dependency. In a frozen application this frequently causes crashes due to backend initialization.

A minimal matplotlib stub is injected at runtime to neutralize matplotlib imports. This is safe because the application does not perform any plotting.

---

### 4.2 OpenCV Window Stability

On macOS, OpenCV windows may freeze unless the window thread is explicitly started:

```python
cv2.startWindowThread()
```

This call must occur before any OpenCV window is shown.

---

### 4.3 Camera Backend Selection

Different capture backends are used intentionally:

* Face recording mode: `cv2.VideoCapture(0)`
* Attendance mode: `cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)`

This avoids backend conflicts and improves reliability on macOS.

---

## 5. PyInstaller Design Considerations

Several common PyInstaller approaches do not work reliably for macOS ML applications:

* One-file mode (`--onefile`)
* Embedding native libraries directly into the executable
* Relying on automatic hidden-import detection
* Treating `collect_all()` results as objects instead of tuples

These approaches lead to silent crashes, missing camera permissions, broken code signing, or TensorFlow runtime failures.

---

## 6. Final Working PyInstaller Architecture

The stable and supported structure for this application is:

```
EXE (Python bytecode only)
  → COLLECT (native libraries and data files)
    → BUNDLE (.app container)
```

This layout matches macOS expectations for hardened runtime applications and ensures correct dynamic library loading.

---

## 7. Final PyInstaller Specification File

The provided `FaceAttendance.spec` file represents the final, production-ready configuration.

Key properties:

* Explicit separation of binaries and data
* Controlled hidden imports
* Exclusion of test modules and unused backends
* Proper `.app` bundle generation

The specification file should not be simplified unless PyInstaller internals are fully understood.

---

## 8. Building the Application

```bash
rm -rf build dist
pyinstaller FaceAttendance.spec
```

The resulting application will be located at:

```
dist/FaceAttendance.app
```

---

## 9. Camera Permissions and Code Signing

### 9.1 Entitlements

The application requires camera access. An entitlements file must be provided:

```xml
<plist version="1.0">
<dict>
  <key>com.apple.security.device.camera</key>
  <true/>
  <key>com.apple.security.cs.allow-jit</key>
  <true/>
  <key>com.apple.security.cs.disable-library-validation</key>
  <true/>
</dict>
</plist>
```

---

### 9.2 Signing the Application

```bash
codesign --deep --force --sign - \
  --entitlements entitlements.plist \
  dist/FaceAttendance.app
```

Verification:

```bash
codesign --verify --deep --strict dist/FaceAttendance.app
```

---

### 9.3 Camera Permission Reset (If Required)

```bash
tccutil reset Camera
open dist/FaceAttendance.app
```

Enable camera access under:
System Settings → Privacy & Security → Camera

---

## 10. Debugging the Application

### 10.1 Run from Terminal

Running the executable directly exposes stdout and stderr:

```bash
./dist/FaceAttendance.app/Contents/MacOS/FaceAttendance
```

This is the primary method for diagnosing runtime issues.

---

### 10.2 PyInstaller Debug Mode

For verbose startup diagnostics, enable the following in the spec file:

```python
console=True
debug=True
```

Rebuild the application to view detailed logs.

---

## 11. Common Problems and Solutions

### collect_all API Errors

Cause: PyInstaller 6 returns tuples, not objects.

Solution:

```python
datas, binaries, hiddenimports = collect_all('module')
```

---

### tensorflow_macos Import Errors

Cause: Package distribution name differs from import name.

Solution: Use only `tensorflow` in hidden imports.

---

### Application Closes Immediately

Typical causes:

* Missing native libraries
* Incorrect executable layout
* Absence of COLLECT stage

Resolution: Use the EXE → COLLECT → BUNDLE architecture.

---

### Camera Not Accessible

Typical causes:

* Application not signed
* Entitlements applied to the executable instead of the bundle

Resolution: Sign the `.app` bundle with the correct entitlements.

---

## 12. Conclusion

This build process produces a stable, Apple Silicon–native macOS application that correctly integrates:

* OpenCV
* MediaPipe
* TensorFlow (Metal)
* Tkinter

The configuration reflects real-world constraints of shipping machine learning desktop applications on macOS.

---

## 13. Optional Next Steps

* Create a DMG installer
* Add a custom application icon (`.icns`)
* Apple notarization for distribution
* Application size reduction and dependency trimming

---

Author’s note: This documentation exists to address the lack of complete, accurate references for packaging ML-based Python applications on macOS. It is intentionally explicit and conservative to maximize reliability.
