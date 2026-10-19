import os
import sys
import subprocess
import shutil
from pathlib import Path

def get_ffmpeg_path():
    ffmpeg_sys = shutil.which("ffmpeg")
    if ffmpeg_sys:
        return ffmpeg_sys
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass
    return None

def convert_video_to_audio(input_file: str, output_file: str = None, audio_format: str = "mp3", bitrate: str = "192k"):
    ffmpeg_exe = get_ffmpeg_path()
    if not ffmpeg_exe:
        print("[ERROR] FFmpeg tidak ditemukan!")
        print("Silakan install FFmpeg di sistem atau jalankan: pip install imageio-ffmpeg")
        return False

    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"[ERROR] File input tidak ditemukan: {input_path}")
        return False

    if not output_file:
        output_path = input_path.with_suffix(f".{audio_format.lstrip('.')}")
    else:
        output_path = Path(output_file).resolve()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[INFO] Memulai konversi...")
    print(f"  Input  : {input_path}")
    print(f"  Output : {output_path}")
    print(f"  Format : {audio_format.upper()} ({bitrate})")

    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", str(input_path),
        "-vn",
        "-b:a", bitrate,
        str(output_path)
    ]

    try:
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode == 0:
            print("\n[SUKSES] Konversi selesai!")
            print(f"File tersimpan di: {output_path}")
            return True
        else:
            print(f"\n[ERROR] FFmpeg gagal mengeksekusi.")
            print(process.stderr)
            return False
    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")
        return False

def main():
    print("=" * 50)
    print("      VIDEO TO AUDIO CONVERTER (PYTHON)")
    print("=" * 50)

    if len(sys.argv) > 1:
        folder_path = sys.argv[1].strip().strip('"').strip("'")
    else:
        folder_path = input("Masukkan path/lokasi folder: ").strip().strip('"').strip("'")

    if not folder_path:
        print("[PERINGATAN] Path folder tidak boleh kosong.")
        return

    dir_path = Path(folder_path).resolve()
    if not dir_path.is_dir():
        # Jika user memasukkan langsung path file yang valid, tetap toleransi atau cek
        if dir_path.is_file():
            video_path = dir_path
        else:
            print(f"[ERROR] Folder tidak ditemukan: {dir_path}")
            return
    else:
        file_name = input("Masukkan nama file yang ingin di-convert (misal: video.mp4): ").strip().strip('"').strip("'")
        if not file_name:
            print("[PERINGATAN] Nama file tidak boleh kosong.")
            return
        video_path = dir_path / file_name

    if not video_path.exists():
        print(f"[ERROR] File tidak ditemukan di folder tersebut: {video_path}")
        return

    print("\nPilih format audio output:")
    print("1. MP3 (Default)")
    print("2. WAV")
    print("3. AAC")
    print("4. FLAC")
    print("5. OGG")
    pilihan = input("Masukkan nomor pilihan (tekan Enter untuk MP3): ").strip()

    format_mapping = {
        "1": "mp3",
        "2": "wav",
        "3": "aac",
        "4": "flac",
        "5": "ogg"
    }
    audio_format = format_mapping.get(pilihan, "mp3")

    convert_video_to_audio(str(video_path), audio_format=audio_format)

if __name__ == "__main__":
    main()
