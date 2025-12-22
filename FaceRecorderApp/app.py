import cv2
import mediapipe as mp
import os
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
from pathlib import Path


# ----------------- SAFE OUTPUT FOLDER (Works in .app) -----------------
def get_output_base_dir():
    """
    Always save to ~/Documents/FaceRecorder/data
    so packaged .app and Terminal runs behave the same.
    """
    base = Path.home() / "Documents" / "FaceRecorder" / "data"
    base.mkdir(parents=True, exist_ok=True)
    return str(base)


DATA_BASE_DIR = get_output_base_dir()


def sanitize_name(name: str) -> str:
    if not name:
        return ""
    # keep letters/numbers/space/_/-
    cleaned = "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).strip()
    # avoid empty folder name
    return cleaned if cleaned else "Unknown"


# ----------------- GUI INPUTS -----------------
def ask_person_name():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    person = simpledialog.askstring("New Person", "Enter person name:")
    root.destroy()
    if person is None:
        return None
    return sanitize_name(person)


def ask_continue():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    answer = messagebox.askyesno("Add Another?", "Do you want to add another person?")
    root.destroy()
    return answer


def show_error(title, msg):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showerror(title, msg)
    root.destroy()


# ----------------- FACE ORIENTATION (EYES + NOSE) -----------------
def get_face_orientation(landmarks_3d, img_w, img_h):
    """
    Estimate yaw & pitch using eyes + nose in pixel coordinates.

    yaw   < 0 -> looking left
    yaw   > 0 -> looking right
    pitch < 0 -> nose above eye-line
    pitch > 0 -> nose below eye-line
    """
    left_eye_idx = 33      # left eye outer
    right_eye_idx = 263    # right eye outer
    nose_tip_idx = 1       # nose tip

    left_eye = landmarks_3d[left_eye_idx]
    right_eye = landmarks_3d[right_eye_idx]
    nose_tip = landmarks_3d[nose_tip_idx]

    p_left = np.array([left_eye.x * img_w, left_eye.y * img_h], dtype=np.float32)
    p_right = np.array([right_eye.x * img_w, right_eye.y * img_h], dtype=np.float32)
    p_nose = np.array([nose_tip.x * img_w, nose_tip.y * img_h], dtype=np.float32)

    mid_eye = (p_left + p_right) / 2.0
    eye_dist = np.linalg.norm(p_right - p_left) + 1e-6

    yaw = (p_nose[0] - mid_eye[0]) / eye_dist
    pitch = (p_nose[1] - mid_eye[1]) / eye_dist

    return yaw, pitch, (int(p_nose[0]), int(p_nose[1]))


def classify_angle_bucket(yaw, pitch_adj):
    """
    9 buckets:
      center, up, down, left, right,
      up_left, up_right, down_left, down_right.
    """
    yaw_thresh = 0.18
    pitch_thresh = 0.06

    # LEFT / CENTER / RIGHT
    if abs(yaw) < yaw_thresh:
        col = "center"
    elif yaw > 0:
        col = "right"
    else:
        col = "left"

    # UP / CENTER / DOWN
    if pitch_adj < -pitch_thresh:
        row = "up"
    elif pitch_adj > pitch_thresh:
        row = "down"
    else:
        row = "center"

    if row == "center" and col == "center":
        return "center"
    if row == "up" and col == "center":
        return "up"
    if row == "down" and col == "center":
        return "down"
    if row == "center" and col == "left":
        return "left"
    if row == "center" and col == "right":
        return "right"
    if row == "up" and col == "left":
        return "up_left"
    if row == "up" and col == "right":
        return "up_right"
    if row == "down" and col == "left":
        return "down_left"
    if row == "down" and col == "right":
        return "down_right"
    return "center"


# ----------------- TIGHT 1:1 HEAD CROP -----------------
def get_square_head_crop(frame, rel_box):
    """
    Square crop around face + some hair, no stretching.
    Uses mediapipe face-detection relative bbox.
    """
    h, w, _ = frame.shape

    x = rel_box.xmin
    y = rel_box.ymin
    bw = rel_box.width
    bh = rel_box.height

    margin_x = 0.03
    margin_y_top = 0.08
    margin_y_bottom = 0.03

    x = x - margin_x
    y = y - margin_y_top
    bw = bw + 2 * margin_x
    bh = bh + margin_y_top + margin_y_bottom

    x1 = int(x * w)
    y1 = int(y * h)
    x2 = int((x + bw) * w)
    y2 = int((y + bh) * h)

    if x2 <= x1 or y2 <= y1:
        return None, None

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    rect_w = x2 - x1
    rect_h = y2 - y1
    side = max(rect_w, rect_h)

    sq_x1 = cx - side // 2
    sq_y1 = cy - side // 2
    sq_x2 = sq_x1 + side
    sq_y2 = sq_y1 + side

    # keep inside frame
    if sq_x1 < 0:
        sq_x2 -= sq_x1
        sq_x1 = 0
    if sq_y1 < 0:
        sq_y2 -= sq_y1
        sq_y1 = 0
    if sq_x2 > w:
        diff = sq_x2 - w
        sq_x1 -= diff
        sq_x2 = w
    if sq_y2 > h:
        diff = sq_y2 - h
        sq_y1 -= diff
        sq_y2 = h

    if sq_x1 < 0 or sq_y1 < 0 or sq_x2 > w or sq_y2 > h \
       or sq_x2 <= sq_x1 or sq_y2 <= sq_y1:
        return None, None

    crop = frame[sq_y1:sq_y2, sq_x1:sq_x2]
    return crop, (sq_x1, sq_y1, sq_x2, sq_y2)


# ----------------- CAPTURE LOOP WITH PER-ANGLE QUOTAS -----------------
def capture_for_person(person_name, start_index=0):
    """
    Per-angle quotas:
      center: 12
      others: 11 each
      total: 100
    """
    person_dir = os.path.join(DATA_BASE_DIR, person_name)
    os.makedirs(person_dir, exist_ok=True)

    angle_targets = {
        "center": 12,
        "up": 11, "down": 11, "left": 11, "right": 11,
        "up_left": 11, "up_right": 11,
        "down_left": 11, "down_right": 11,
    }
    angle_names = list(angle_targets.keys())
    angle_counts = {k: 0 for k in angle_names}
    max_total = sum(angle_targets.values())

    mp_mesh = mp.solutions.face_mesh
    mp_fd = mp.solutions.face_detection

    # --- IMPORTANT FOR MAC: use AVFOUNDATION ---
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

    if not cap.isOpened():
        show_error(
            "Camera not found",
            "OpenCV could not open the camera.\n\n"
            "Check:\n"
            "1) System Settings → Privacy & Security → Camera\n"
            "2) Allow camera for this app/Terminal\n"
            "3) Close other apps using the camera (Zoom/Meet/etc.)"
        )
        return start_index

    current_index = start_index

    # Quality thresholds
    BLUR_THRESHOLD = 80.0
    BRIGHTNESS_MIN = 60.0
    OVEREXPOSE_RATIO_MAX = 0.40
    NOISE_STD_MAX = 40.0

    MIN_INTERVAL_PER_BUCKET = 0.20
    last_save_time = {k: 0.0 for k in angle_names}

    yaw_smooth = 0.0
    pitch_smooth = 0.0
    alpha = 0.5

    print(f"--- Recording for {person_name} ---")
    print(f"Saving to: {person_dir}")

    with mp_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh, mp_fd.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.6
    ) as face_det:

        # -------- 1s CALIBRATION --------
        pitch_samples = []
        calib_start = time.time()
        while time.time() - calib_start < 1.0:
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mesh_results = face_mesh.process(rgb)

            if mesh_results.multi_face_landmarks:
                face_landmarks = mesh_results.multi_face_landmarks[0]
                landmarks_list = face_landmarks.landmark
                _, pitch_tmp, _ = get_face_orientation(landmarks_list, w, h)
                pitch_samples.append(pitch_tmp)

            cv2.putText(frame, "Look straight to calibrate...",
                        (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 255, 255), 2)
            cv2.imshow("FaceRecorder (calibration)", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return current_index

        pitch_center = float(np.mean(pitch_samples)) if pitch_samples else 0.0
        print(f"Calibrated pitch_center = {pitch_center:.4f}")

        # -------- MAIN LOOP --------
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            mesh_results = face_mesh.process(rgb)
            det_results = face_det.process(rgb)

            bbox = None
            current_bucket = "center"
            nose_px = None
            yaw_raw = 0.0
            pitch_raw = 0.0
            pitch_adj = 0.0

            if mesh_results.multi_face_landmarks and det_results.detections:
                face_landmarks = mesh_results.multi_face_landmarks[0]
                landmarks_list = face_landmarks.landmark

                yaw_raw, pitch_raw, nose_px = get_face_orientation(landmarks_list, w, h)
                pitch_adj = pitch_raw - pitch_center

                yaw_smooth = alpha * yaw_raw + (1 - alpha) * yaw_smooth
                pitch_smooth = alpha * pitch_adj + (1 - alpha) * pitch_smooth

                current_bucket = classify_angle_bucket(yaw_smooth, pitch_smooth)

                detection = det_results.detections[0]
                rel_box = detection.location_data.relative_bounding_box
                square_crop, bbox = get_square_head_crop(frame, rel_box)

                now = time.time()
                total_saved = sum(angle_counts.values())

                if (
                    square_crop is not None
                    and square_crop.size != 0
                    and total_saved < max_total
                    and angle_counts[current_bucket] < angle_targets[current_bucket]
                    and (now - last_save_time[current_bucket]) >= MIN_INTERVAL_PER_BUCKET
                ):
                    gray = cv2.cvtColor(square_crop, cv2.COLOR_BGR2GRAY)

                    # 1) Blur
                    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                    if fm >= BLUR_THRESHOLD:
                        # 2) Brightness
                        mean_brightness = gray.mean()
                        if mean_brightness >= BRIGHTNESS_MIN:
                            # 3) Overexposure
                            bright_ratio = np.count_nonzero(gray >= 245) / float(gray.size)
                            if bright_ratio <= OVEREXPOSE_RATIO_MAX:
                                # 4) Noise
                                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                                diff = gray.astype(np.float32) - blurred.astype(np.float32)
                                noise_std = diff.std()
                                if noise_std <= NOISE_STD_MAX:
                                    current_index += 1
                                    angle_counts[current_bucket] += 1
                                    last_save_time[current_bucket] = now

                                    square_resized = cv2.resize(square_crop, (256, 256))
                                    filename = os.path.join(
                                        person_dir,
                                        f"{person_name}_{current_index:04d}.jpg"
                                    )
                                    cv2.imwrite(filename, square_resized)

            # Draw bbox + arrow
            if bbox is not None:
                x1, y1, x2, y2 = bbox
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                if nose_px is not None:
                    arrow_len = int(min(w, h) * 0.14)
                    dx = int(yaw_smooth * arrow_len)
                    dy = int(pitch_smooth * arrow_len)
                    end_pt = (nose_px[0] + dx, nose_px[1] + dy)
                    cv2.arrowedLine(frame, nose_px, end_pt, (0, 255, 255), 2, tipLength=0.4)

                cv2.putText(frame, f"Angle: {current_bucket}",
                            (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            # HUD
            total_saved = sum(angle_counts.values())
            cv2.putText(frame, f"{person_name} | Total: {total_saved}/{max_total}",
                        (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame,
                        f"yaw={yaw_raw:+.2f} pitch_raw={pitch_raw:+.2f} pitch_adj={pitch_adj:+.2f}",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
            cv2.putText(frame,
                        "Move head | Press 'q' to finish",
                        (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            y0 = 95
            for name in angle_names:
                txt = f"{name}: {angle_counts[name]}/{angle_targets[name]}"
                cv2.putText(frame, txt, (10, y0),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
                y0 += 18

            cv2.imshow("FaceRecorder (recording)", frame)

            if total_saved >= max_total:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Finished {person_name}: {total_saved}/{max_total} images")
    print("Per-angle counts:", angle_counts)
    return current_index


# ----------------- MAIN -----------------
def main():
    while True:
        name = ask_person_name()
        if name is None:
            print("Cancelled. Exiting.")
            break
        if not name:
            print("No name entered. Exiting.")
            break

        _ = capture_for_person(name, start_index=0)

        again = ask_continue()
        if not again:
            print("Stopping program.")
            break


if __name__ == "__main__":
    main()