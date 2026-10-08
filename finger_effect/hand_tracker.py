"""
hand_tracker.py
Modul wrapper untuk deteksi tangan & landmark jari pakai MediaPipe.
Dipakai berulang di tahap-tahap selanjutnya (finger counting, square drawing, dll).
"""

import cv2
import mediapipe as mp

# Index landmark ujung jari (fingertip) di MediaPipe Hands:
# 4 = ibu jari, 8 = telunjuk, 12 = tengah, 16 = manis, 20 = kelingking
FINGERTIP_IDS = [4, 8, 12, 16, 20]


class HandTracker:
    def __init__(self, max_hands=2, detection_conf=0.7, tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        self.results = None

    def find_hands(self, frame, draw_landmarks=True):
        """Deteksi tangan di satu frame. Return frame (opsional digambar) + hasil deteksi."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks and draw_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_styles.get_default_hand_landmarks_style(),
                    self.mp_styles.get_default_hand_connections_style(),
                )
        return frame

    def get_fingertip_positions(self, frame):
        """
        Ambil posisi pixel (x, y) semua ujung jari dari semua tangan yang terdeteksi.
        Return: list of dict, tiap dict = {landmark_id: (x, y)} untuk satu tangan.
        """
        h, w, _ = frame.shape
        all_tips = []

        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                tips = {}
                for tip_id in FINGERTIP_IDS:
                    lm = hand_landmarks.landmark[tip_id]
                    tips[tip_id] = (int(lm.x * w), int(lm.y * h))
                all_tips.append(tips)

        return all_tips

    def close(self):
        self.hands.close()
