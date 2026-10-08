import qrcode
import sys


def create_qr_code(link, filename="qrcode.png", box_size=10, border=4):
    """
    Membuat QR code dari sebuah link.
    
    Args:
        link (str): URL atau teks yang akan diubah menjadi QR code
        filename (str): Nama file output (default: qrcode.png)
        box_size (int): Ukuran setiap kotak QR code (default: 10)
        border (int): Lebar border dalam kotak (default: 4)
    
    Returns:
        str: Nama file yang telah dibuat
    """
    # Membuat objek QR code
    qr = qrcode.QRCode(
        version=1,  # Mengontrol ukuran QR code (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Tingkat koreksi error tinggi
        box_size=box_size,
        border=border,
    )
    
    # Menambahkan data ke QR code
    qr.add_data(link)
    qr.make(fit=True)
    
    # Membuat gambar dari QR code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Menyimpan gambar
    img.save(filename)
    print(f"QR code berhasil dibuat dan disimpan sebagai '{filename}'")
    
    return filename


def main():
    """Fungsi utama untuk menjalankan script dari command line."""
    print("=== QR Code Generator ===")
    
    # Cek apakah ada argumen dari command line
    if len(sys.argv) > 1:
        link = sys.argv[1]
        filename = sys.argv[2] if len(sys.argv) > 2 else "qrcode.png"
    else:
        # Input dari user
        link = input("Masukkan link atau teks: ").strip()
        if not link:
            print("Error: Link tidak boleh kosong!")
            sys.exit(1)
        
        filename_input = input("Masukkan nama file output (default: qrcode.png): ").strip()
        filename = filename_input if filename_input else "qrcode.png"
    
    # Membuat QR code
    create_qr_code(link, filename)


if __name__ == "__main__":
    main()
