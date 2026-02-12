# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

mp_datas, mp_bins, mp_hidden = collect_all('mediapipe')
cv_datas, cv_bins, cv_hidden = collect_all('cv2')
mtcnn_datas, mtcnn_bins, mtcnn_hidden = collect_all('mtcnn')
kf_datas, kf_bins, kf_hidden = collect_all('keras_facenet')
sk_datas, sk_bins, sk_hidden = collect_all('sklearn')

block_cipher = None

all_binaries = (
    mp_bins
    + cv_bins
    + mtcnn_bins
    + kf_bins
    + sk_bins
)

all_datas = (
    mp_datas
    + cv_datas
    + mtcnn_datas
    + kf_datas
    + sk_datas
    + [("models", "models")]
)


hidden_imports = set(
    mp_hidden
    + cv_hidden
    + mtcnn_hidden
    + kf_hidden
    + sk_hidden
)
hidden_imports.update([
    'tensorflow',
    'keras',
    'sklearn.neighbors',
    'sklearn.preprocessing',
    # Some sklearn builds require these explicitly
    'sklearn.utils._cython_blas',
    'sklearn.utils._weight_vector',
])

a = Analysis(
    ['face_attendance.py'],
    pathex=['.'],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=list(hidden_imports),
    excludes=[
        'torch',
        'mediapipe.model_maker',   # silence warning
        'sklearn.tests',           # MASSIVE size reduction
    ],
    hookspath=[],
    runtime_hooks=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    name='FaceAttendance',
    exclude_binaries=True,
    argv_emulation=True,
    console=False,
    strip=False,
    upx=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='FaceAttendance',
)

app = BUNDLE(
    coll,
    name='FaceAttendance.app',
    bundle_identifier='com.yourname.faceattendance',
    entitlements_file='entitlements.plist',
    info_plist={
        'NSCameraUsageDescription': 'Camera access is required for face recognition attendance.',
        'LSUIElement': False,
    },
)
