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
        video_path = sys.argv[1].strip().strip('"').strip("'")
    else:
        video_path = input("Masukkan path/lokasi file video: ").strip().strip('"').strip("'")

    if not video_path:
        print("[PERINGATAN] Path video tidak boleh kosong.")
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

    convert_video_to_audio(video_path, audio_format=audio_format)

if __name__ == "__main__":
    main()
