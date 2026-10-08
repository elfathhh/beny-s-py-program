"""
main.py
TAHAP 1: Setup kamera + deteksi tangan/jari dasar.

Yang dilakukan tahap ini:
- Buka webcam
- Deteksi landmark tangan pakai MediaPipe (lewat hand_tracker.py)
- Gambar skeleton tangan
- Tandai ujung-ujung jari (fingertip) dengan lingkaran berwarna
- Tampilkan jumlah tangan yang terdeteksi (debug info)

Tekan 'q' untuk keluar.
"""

import sys
import traceback
import cv2
from hand_tracker import HandTracker

def main():
    print("Membuka kamera...", flush=True)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Tidak bisa membuka kamera. Pastikan webcam terhubung & tidak dipakai app lain.", flush=True)
        return

    print("Kamera terbuka. Membuat HandTracker...", flush=True)
    tracker = HandTracker(max_hands=2)
    print("HandTracker siap. Masuk ke loop utama...", flush=True)

    while True:
        success, frame = cap.read()
        if not success:
            print("Gagal membaca frame dari kamera.", flush=True)
            break

        # Mirror biar seperti cermin (lebih natural buat user)
        frame = cv2.flip(frame, 1)

        # Deteksi tangan + gambar skeleton
        frame = tracker.find_hands(frame, draw_landmarks=True)

        # Ambil posisi semua ujung jari, lalu tandai dengan lingkaran
        all_tips = tracker.get_fingertip_positions(frame)
        for hand_tips in all_tips:
            for tip_id, (x, y) in hand_tips.items():
                cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)

        # Debug info di layar
        num_hands = len(all_tips)
        cv2.putText(
            frame,
            f"Tangan terdeteksi: {num_hands}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Tahap 1 - Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    tracker.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("=== TERJADI ERROR, TRACEBACK LENGKAP DI BAWAH ===", flush=True)
        traceback.print_exc()
        input("Tekan Enter untuk keluar...")
        sys.exit(1)
