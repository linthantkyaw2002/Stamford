# --- MediaPipe matplotlib stub (for standalone macOS app) ---
import sys
import types

if 'matplotlib' not in sys.modules:
    matplotlib_stub = types.ModuleType("matplotlib")
    pyplot_stub = types.ModuleType("matplotlib.pyplot")

    def _noop(*args, **kwargs):
        return None

    pyplot_stub.figure = _noop
    pyplot_stub.imshow = _noop
    pyplot_stub.show = _noop
    pyplot_stub.plot = _noop
    pyplot_stub.axis = _noop

    matplotlib_stub.pyplot = pyplot_stub

    sys.modules['matplotlib'] = matplotlib_stub
    sys.modules['matplotlib.pyplot'] = pyplot_stub
# ================= IMPORTS =================
# Standard Libraries
import cv2
import os
import csv
import time
import threading
import platform
import numpy as np
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import simpledialog, messagebox

# AI & Processing Libraries
import mediapipe as mp
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import Normalizer

# ================= GLOBAL CONFIGURATION =================
BASE_DIR = Path.home() / "Documents" / "FaceRecorder"
DATASET_DIR = BASE_DIR / "data"
ATTENDANCE_FILE = BASE_DIR / "attendance.csv"

# Attendance Tuning
DISTANCE_THRESHOLD = 0.58
REQUIRED_STREAK = 3
N_NEIGHBORS = 5
ATTENDANCE_COOLDOWN = 60

# Initialize Global AI Models
# Initialize Global AI Models
detector_mtcnn = MTCNN()

if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).resolve().parent

embedder = FaceNet(cache_folder=str(base_path / "models"))
l2_norm = Normalizer(norm='l2')
mp_mesh = mp.solutions.face_mesh
mp_fd = mp.solutions.face_detection

# Global State for Attendance
last_seen = {}
current_results = []
is_processing = False
knn_model = None
face_streaks = {}


# ================= 1. EMBEDDING LOGIC (build_embedding.py) =================

def get_embedding(face):
    face = face.astype("float32")
    face = np.expand_dims(face, axis=0)
    emb = embedder.embeddings(face)[0]
    return l2_norm.transform([emb])[0]


def build_embeddings():
    if not DATASET_DIR.exists():
        DATASET_DIR.mkdir(parents=True, exist_ok=True)
        return

    for person in os.listdir(DATASET_DIR):
        person_dir = DATASET_DIR / person
        if not person_dir.is_dir(): continue

        embedding_file = person_dir / "embedding.npy"
        if embedding_file.exists():
            print(f"[SKIP] Embeddings already exist for {person}")
            continue

        print(f"[*] Processing new person: {person}...")
        embeddings = []
        for img_name in os.listdir(person_dir):
            if not img_name.lower().endswith(".jpg"): continue

            img = cv2.imread(str(person_dir / img_name))
            if img is None: continue

            face = cv2.resize(img, (160, 160))
            embeddings.append(get_embedding(face))

        if embeddings:
            np.save(embedding_file, np.array(embeddings))
            print(f"[OK] Saved {len(embeddings)} optimized embeddings for {person}")


# ================= 2. RECORDING LOGIC (record.py) =================

def sanitize_name(name):
    if not name: return ""
    cleaned = "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).strip()
    return cleaned if cleaned else "Unknown"


def get_face_orientation(landmarks_3d, img_w, img_h):
    left_eye = landmarks_3d[33]
    right_eye = landmarks_3d[263]
    nose_tip = landmarks_3d[1]

    p_left = np.array([left_eye.x * img_w, left_eye.y * img_h])
    p_right = np.array([right_eye.x * img_w, right_eye.y * img_h])
    p_nose = np.array([nose_tip.x * img_w, nose_tip.y * img_h])

    mid_eye = (p_left + p_right) / 2.0
    eye_dist = np.linalg.norm(p_right - p_left) + 1e-6

    return (p_nose[0] - mid_eye[0]) / eye_dist, (p_nose[1] - mid_eye[1]) / eye_dist, (int(p_nose[0]), int(p_nose[1]))


def classify_angle_bucket(yaw, pitch_adj):
    yaw_thresh, pitch_thresh = 0.18, 0.06
    col = "center" if abs(yaw) < yaw_thresh else ("right" if yaw > 0 else "left")
    row = "center" if abs(pitch_adj) < pitch_thresh else ("down" if pitch_adj > pitch_thresh else "up")

    if row == "center" and col == "center": return "center"
    return f"{row}_{col}".replace("center_", "").replace("_center", "")


def get_square_head_crop(frame, rel_box):
    h, w, _ = frame.shape
    x, y, bw, bh = rel_box.xmin, rel_box.ymin, rel_box.width, rel_box.height
    x1, y1 = int((x - 0.03) * w), int((y - 0.08) * h)
    x2, y2 = int((x + bw + 0.03) * w), int((y + bh + 0.03) * h)

    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    side = max(x2 - x1, y2 - y1)
    sq_x1, sq_y1 = max(0, cx - side // 2), max(0, cy - side // 2)

    crop = frame[sq_y1:sq_y1 + side, sq_x1:sq_x1 + side]
    return crop, (sq_x1, sq_y1, sq_x1 + side, sq_y1 + side) if crop.size != 0 else (None, None)


def capture_for_person(person_name):
    person_dir = DATASET_DIR / person_name
    person_dir.mkdir(parents=True, exist_ok=True)

    # Specific angle targets configuration
    angle_targets = {
        "center": 12, "up": 11, "down": 11, "left": 11, "right": 11,
        "up_left": 11, "up_right": 11, "down_left": 11, "down_right": 11
    }
    angle_counts = {k: 0 for k in angle_targets.keys()}
    max_total = sum(angle_targets.values())

    # --- STABILITY FIX: Initialize Window Early ---
    window_name = "Face Recording - " + person_name
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    cv2.startWindowThread() # Helps prevent window hanging on macOS/Linux
    
    # Use index 0; remove CAP_AVFOUNDATION unless specifically needed for hardware issues
    cap = cv2.VideoCapture(0)

    # Smoothing and Quality Config
    yaw_smooth = pitch_smooth = 0.0
    alpha = 0.5
    BLUR_THRESHOLD = 80.0
    BRIGHTNESS_MIN = 60.0

    with mp_mesh.FaceMesh(refine_landmarks=True) as mesh, \
            mp_fd.FaceDetection(min_detection_confidence=0.6) as fd:

        # -------- 1s Calibration Phase --------
        p_samples = []
        cal_st = time.time()
        while time.time() - cal_st < 1.0:
            ret, frame = cap.read()
            if not ret: break
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = mesh.process(rgb)
            if res.multi_face_landmarks:
                _, p, _ = get_face_orientation(res.multi_face_landmarks[0].landmark, frame.shape[1], frame.shape[0])
                p_samples.append(p)
            
            cv2.putText(frame, "Look straight to calibrate...", (30, 40), 1, 1.5, (0, 255, 255), 2)
            cv2.imshow(window_name, frame)
            cv2.waitKey(1)
            
        p_center = np.mean(p_samples) if p_samples else 0.0

        # -------- Main Capture Loop --------
        while sum(angle_counts.values()) < max_total:
            ret, frame = cap.read()
            if not ret: break
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process AI models
            m_res, d_res = mesh.process(rgb), fd.process(rgb)

            if m_res.multi_face_landmarks and d_res.detections:
                y_raw, p_raw, nose = get_face_orientation(m_res.multi_face_landmarks[0].landmark, w, h)

                yaw_smooth = alpha * y_raw + (1 - alpha) * yaw_smooth
                pitch_smooth = alpha * (p_raw - p_center) + (1 - alpha) * pitch_smooth

                bucket = classify_angle_bucket(yaw_smooth, pitch_smooth)
                crop, bbox = get_square_head_crop(frame, d_res.detections[0].location_data.relative_bounding_box)

                if crop is not None and angle_counts[bucket] < angle_targets[bucket]:
                    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                    blur_val = cv2.Laplacian(gray, cv2.CV_64F).var()
                    bright_val = gray.mean()

                    # Quality Check and Auto-Save
                    if blur_val >= BLUR_THRESHOLD and bright_val >= BRIGHTNESS_MIN:
                        angle_counts[bucket] += 1
                        filename = person_dir / f"{person_name}_{sum(angle_counts.values()):04d}.jpg"
                        cv2.imwrite(str(filename), cv2.resize(crop, (256, 256)))

                # Draw Visuals (BBox & Directional Arrow)
                if bbox:
                    cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
                    arrow_len = int(min(w, h) * 0.14)
                    end_pt = (nose[0] + int(yaw_smooth * arrow_len), nose[1] + int(pitch_smooth * arrow_len))
                    cv2.arrowedLine(frame, nose, end_pt, (0, 255, 255), 2, tipLength=0.4)
                    cv2.putText(frame, f"Angle: {bucket}", (bbox[0], bbox[1] - 10), 1, 1, (0, 255, 255), 2)

            # --- HUD Rendering ---
            cv2.putText(frame, f"{person_name} | Total: {sum(angle_counts.values())}/{max_total}", (10, 25), 1, 1, (0, 255, 0), 2)
            y_offset = 60
            for ang, count in angle_counts.items():
                color = (0, 255, 0) if count >= angle_targets[ang] else (255, 255, 255)
                cv2.putText(frame, f"{ang}: {count}/{angle_targets[ang]}", (10, y_offset), 1, 0.8, color, 1)
                y_offset += 18

            # --- Display and Force Focus ---
            cv2.imshow(window_name, frame)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break

    # --- Cleanup ---
    cap.release()
    cv2.destroyWindow(window_name)
    # Important: Small delay for the OS to finalize window closing
    for _ in range(10): cv2.waitKey(1)


# ================= 3. ATTENDANCE LOGIC (attendance.py) =================

def ensure_attendance_file():
    ATTENDANCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not ATTENDANCE_FILE.exists():
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Name", "Date", "Time"])


def load_knn():
    global knn_model
    X, y = [], []
    if not DATASET_DIR.exists(): return False
    for p in os.listdir(DATASET_DIR):
        p_dir = DATASET_DIR / p
        if p_dir.is_dir() and (p_dir / "embedding.npy").exists():
            for e in np.load(p_dir / "embedding.npy"):
                X.append(e);
                y.append(p)
    if len(X) < N_NEIGHBORS: return False
    knn_model = KNeighborsClassifier(n_neighbors=N_NEIGHBORS, metric='euclidean', weights='distance')
    knn_model.fit(l2_norm.transform(X), y)
    return True


def recognize_async(crops, bboxes):
    global current_results, is_processing, face_streaks
    res = []
    for i, crop in enumerate(crops):
        emb = l2_norm.transform([embedder.embeddings(np.expand_dims(crop.astype("float32"), 0))[0]])[0]
        dist, _ = knn_model.kneighbors([emb], n_neighbors=1)
        pred = knn_model.predict([emb])[0] if dist[0][0] <= DISTANCE_THRESHOLD else "Unknown"

        face_streaks[i] = {"name": pred,
                           "count": face_streaks.get(i, {}).get("count", 0) + 1 if face_streaks.get(i, {}).get(
                               "name") == pred else 1}
        final = pred if face_streaks[i]["count"] >= REQUIRED_STREAK and pred != "Unknown" else "Unknown"

        if final != "Unknown":
            now = time.time()
            if final not in last_seen or now - last_seen[final] > ATTENDANCE_COOLDOWN:
                last_seen[final] = now
                with open(ATTENDANCE_FILE, "a", newline="") as f:
                    csv.writer(f).writerow([final, datetime.now().date(), datetime.now().strftime("%H:%M:%S")])

        res.append({"name": final, "dist": dist[0][0], "bbox": bboxes[i]})
    current_results, is_processing = res, False


def run_attendance():
    global is_processing
    ensure_attendance_file()
    if not load_knn(): return
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    f_count = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        f_count += 1
        if f_count % 5 == 0 and not is_processing:
            faces = detector_mtcnn.detect_faces(cv2.resize(frame, (0, 0), fx=0.5, fy=0.5))
            crops, bboxes = [], []
            for f in faces:
                x, y, w, h = [v * 2 for v in f["box"]]
                bboxes.append((x, y, w, h))
                crop = frame[max(0, y):y + h, max(0, x):x + w]
                if crop.size != 0: crops.append(cv2.resize(crop, (160, 160)))
            if crops:
                is_processing = True
                threading.Thread(target=recognize_async, args=(crops, bboxes), daemon=True).start()
            else:
                face_streaks.clear()

        for r in current_results:
            x, y, w, h = r["bbox"]
            color = (0, 255, 0) if r["name"] != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{r['name']} (D:{r['dist']:.2f})", (x, y - 10), 1, 1, color, 2)

        # HUD
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (260, 45 + (len(last_seen) * 25)), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        cv2.putText(frame, "LIVE ATTENDANCE", (15, 25), 1, 1.2, (0, 255, 255), 2)
        for i, (n, ts) in enumerate(sorted(last_seen.items(), key=lambda x: x[1], reverse=True)[:10]):
            cv2.putText(frame, f"• {n} [{datetime.fromtimestamp(ts).strftime('%H:%M:%S')}]", (15, 55 + (i * 20)), 1,
                        0.9, (0, 255, 0), 1)

        cv2.imshow("Attendance Monitor", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release();
    cv2.destroyAllWindows()


# ================= 4. MAIN INTERFACE (main.py) =================

def view_attendance():
    if ATTENDANCE_FILE.exists():
        cmd = "open" if platform.system() == "Darwin" else ("start" if platform.system() == "Windows" else "xdg-open")
        os.system(f'{cmd} "{ATTENDANCE_FILE}"')


def run_manual_embedding():
    root.withdraw()
    build_embeddings()
    messagebox.showinfo("Done", "Face embeddings have been rebuilt.")
    root.deiconify()


def start_record():
    root.withdraw()
    root.update()
    time.sleep(0.2)

    name = simpledialog.askstring("New Person", "Enter person name:")
    if name:
        capture_for_person(sanitize_name(name))
        build_embeddings()
    root.deiconify()


def start_attendance():
    root.withdraw()
    run_attendance()
    root.deiconify()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("FaceAttendance")
    root.geometry("360x340")
    root.attributes("-topmost", True)

    tk.Label(root, text="FaceAttendance", font=("Helvetica", 18, "bold")).pack(pady=20)
    tk.Button(root, text="🎥 Record Faces", font=("Helvetica", 14), width=20, height=2, command=start_record).pack(
        pady=5)
    tk.Button(root, text="📝 Attendance", font=("Helvetica", 14), width=20, height=2, command=start_attendance).pack(
        pady=5)

    # New Manual Embedding Button
    tk.Button(root, text="⚙️ Build Embeddings", font=("Helvetica", 14), width=20, height=2,
              command=run_manual_embedding).pack(
        pady=5)

    tk.Button(root, text="📊 View Attendance", font=("Helvetica", 14), width=20, height=2, command=view_attendance).pack(
        pady=5)

    root.mainloop()
