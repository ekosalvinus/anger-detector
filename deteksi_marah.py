"""
Aplikasi Deteksi Ekspresi Wajah Marah
--------------------------------------
Menggunakan webcam untuk mendeteksi wajah dan menganalisis ekspresi emosinya.
Jika ekspresi dominan yang terdeteksi adalah "marah" (angry), maka teks
"Saya akan Lawan" akan ditampilkan di layar.

Library yang digunakan:
- OpenCV (opencv-python)   -> menangani video/webcam & menggambar teks/kotak
- DeepFace (deepface)      -> deteksi wajah dan emosi dengan deep learning
- TensorFlow               -> backend untuk DeepFace

Cara menjalankan:
    1. Install dependency (lihat requirements.txt)
    2. Jalankan: python deteksi_marah.py
    3. Tekan tombol 'q' untuk keluar
"""

import cv2
from deepface import DeepFace
import pygame
import warnings
import os
import time
warnings.filterwarnings('ignore')

# Inisialisasi pygame mixer untuk audio
pygame.mixer.init()

# Path ke file MP3
mp3_file = os.path.join(os.path.dirname(__file__), 'saya-akan-lawan.mp3')

# Load audio file
if os.path.exists(mp3_file):
    sound = pygame.mixer.Sound(mp3_file)
    print(f"Audio loaded: {mp3_file}")
else:
    sound = None
    print(f"Warning: Audio file not found at {mp3_file}")

last_play_time = 0  # Untuk mencegah audio diputar terlalu sering

# Buka webcam (0 = kamera default)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Tidak bisa mengakses webcam. Pastikan kamera tersambung dan tidak dipakai aplikasi lain.")

print("Aplikasi berjalan. Tekan 'q' pada jendela video untuk keluar.")

last_play_time = 0  # Inisialisasi ulang untuk tracking waktu pemutaran audio

while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membaca frame dari webcam.")
        break

    try:
        current_time = time.time()
        
        # Deteksi wajah + skor emosi menggunakan DeepFace
        hasil_deteksi = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        
        for wajah in hasil_deteksi:
            # Dapatkan koordinat wajah dari hasil deteksi
            x = wajah['region']['x']
            y = wajah['region']['y']
            w = wajah['region']['w']
            h = wajah['region']['h']
            
            emosi_scores = wajah['emotion']
            
            # Ambil emosi dengan skor tertinggi (emosi dominan)
            emosi_dominan = max(emosi_scores, key=emosi_scores.get)
            skor = emosi_scores[emosi_dominan]

            # Gambar kotak di sekitar wajah
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Tampilkan label emosi + skor di atas kotak wajah
            label = f"{emosi_dominan} ({skor:.2f})"
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Jika emosi dominan adalah "angry" -> putar audio
            if emosi_dominan == "angry" and sound is not None:
                # Putar audio hanya jika belum diputar dalam 3 detik terakhir
                if current_time - last_play_time > 3:
                    sound.play()
                    last_play_time = current_time
                    print("🎵 Audio dimainkan: Saya akan Lawan")
                
                # Tampilkan indikator di layar
                cv2.putText(frame, "[PLAYING AUDIO]", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    except Exception as e:
        # Jika ada error deteksi, lanjutkan saja
        pass

    cv2.imshow("Deteksi Ekspresi Wajah", frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
