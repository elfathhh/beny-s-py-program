import os
from PIL import Image


def kompres_ke_webp(folder_input, folder_output):
    # Buat folder output jika belum ada
    if not os.path.exists(folder_output):
        os.makedirs(folder_output)

    # Ambil semua file di folder input
    for nama_file in os.listdir(folder_input):
        if nama_file.lower().endswith((".png", ".jpg", ".jpeg")):
            jalur_input = os.path.join(folder_input, nama_file)

            # Buka gambar
            img = Image.open(jalur_input)

            # Ubah ukuran ke maksimal 400x400 (proporsional agar tidak gepeng)
            img.thumbnail((400, 400))

            # Siapkan nama file baru dengan ekstensi .webp
            nama_baru = os.path.splitext(nama_file)[0] + ".webp"
            jalur_output = os.path.join(folder_output, nama_baru)

            # Simpan dengan format WebP dan kualitas 75%
            img.save(jalur_output, "WEBP", quality=75)
            print(f"Berhasil mengompres: {nama_file} -> {nama_baru}")


# Jalankan fungsi (titik . berarti folder saat ini)
kompres_ke_webp(folder_input=".", folder_output="./hasil_webp")