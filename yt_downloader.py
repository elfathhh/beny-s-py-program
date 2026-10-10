import os
import shutil
import subprocess
import sys
from pathlib import Path
import yt_dlp


def get_ffmpeg_path() -> str | None:
    """
    Mencari lokasi FFmpeg.
    1. Cek di PATH sistem.
    2. Cek paket imageio-ffmpeg jika ada.
    3. Jika belum ada, coba instal imageio-ffmpeg secara otomatis.
    """
    # 1. Cek di PATH sistem
    if shutil.which("ffmpeg"):
        return "ffmpeg"

    # 2. Cek imageio_ffmpeg
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.exists(exe):
            return exe
    except ImportError:
        pass

    # 3. Upayakan auto-install imageio-ffmpeg jika belum ada
    try:
        print("[INFO] Menginstal dependensi FFmpeg portable (imageio-ffmpeg)...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "imageio-ffmpeg", "--quiet"]
        )
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def download_media(url: str, audio_only: bool = False, output_dir: str = "downloads") -> bool:
    """
    Mengunduh video atau audio dari YouTube.
    Mendukung unduhan video tunggal maupun playlist.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    ffmpeg_path = get_ffmpeg_path()

    # Template penamaan file:
    # - Jika playlist: downloads/Nama Playlist - 01 - Judul Video.ext
    # - Jika video tunggal: downloads/Judul Video.ext
    outtmpl_pattern = str(
        output_path / "%(playlist_title&{} - |)s%(playlist_index&{:02d} - |)s%(title)s.%(ext)s"
    )

    ydl_opts = {
        "outtmpl": outtmpl_pattern,
        "noplaylist": False,  # Mengizinkan download seluruh isi playlist jika link adalah playlist
        "quiet": False,
        "no_warnings": False,
        "paths": {"home": str(output_path)},
    }

    # Konfigurasi JS Runtime menggunakan Node.js jika terpasang (menghindari warning YouTube JS runtime)
    if shutil.which("node"):
        ydl_opts["js_runtimes"] = {"node": {}}

    # Konfigurasi FFmpeg
    if ffmpeg_path:
        ydl_opts["ffmpeg_location"] = ffmpeg_path

    if audio_only:
        # Mode: Hanya Audio
        ydl_opts["format"] = "bestaudio/best"
        if ffmpeg_path:
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }
            ]
        else:
            # Fallback jika tanpa FFmpeg: unduh stream m4a/audio langsung tanpa konversi
            ydl_opts["format"] = "bestaudio[ext=m4a]/bestaudio/best"
    else:
        # Mode: Download Video
        if ffmpeg_path:
            # Download video & audio kualitas terbaik lalu gabungkan (merge) ke MP4
            ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
            ydl_opts["merge_output_format"] = "mp4"
        else:
            # Jika tidak ada FFmpeg, coba ambil video dengan audio langsung
            ydl_opts["format"] = "best[ext=mp4]/best"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            retcode = ydl.download([url])
            if retcode == 0:
                print(f"\n[INFO] File berhasil disimpan di: {output_path.resolve()}")
                return True
            else:
                print(f"\n[WARNING] Proses unduh selesai dengan kode status: {retcode}")
                return False
    except yt_dlp.utils.DownloadError as exc:
        print(f"\n[ERROR] Gagal mengunduh: {exc}")
        return False
    except Exception as exc:
        print(f"\n[ERROR] Terjadi kesalahan tak terduga: {exc}")
        return False


def main():
    while True:
        print("\n" + "=" * 50)
        print("             YOUTUBE DOWNLOADER")
        print("       (Mendukung Video & Playlist)")
        print("=" * 50)
        print("Pilih Menu:")
        print("1. Download Video")
        print("2. Hanya Audio")
        print("3. Keluar")
        print("=" * 50)

        pilihan = input("Pilihan Menu (1/2/3): ").strip()

        if pilihan == "1":
            print("\n--- Download Video ---")
            link = input("Input Link Video/Playlist: ").strip()
            if not link:
                print("[Peringatan] Link tidak boleh kosong!")
                continue
            if link.lower() in ("batal", "cancel", "q"):
                print("[Batal] Kembali ke menu utama.")
                continue

            print("\n[Proses Unduh Video]")
            success = download_media(link, audio_only=False)
            if success:
                print("\n[Selesai] Proses unduh video selesai.")
            else:
                print("\n[Selesai] Proses unduh selesai dengan catatan/kendala.")

        elif pilihan == "2":
            print("\n--- Hanya Audio ---")
            link = input("Input Link Video/Playlist: ").strip()
            if not link:
                print("[Peringatan] Link tidak boleh kosong!")
                continue
            if link.lower() in ("batal", "cancel", "q"):
                print("[Batal] Kembali ke menu utama.")
                continue

            print("\n[Proses Unduh Audio]")
            success = download_media(link, audio_only=True)
            if success:
                print("\n[Selesai] Proses unduh audio selesai.")
            else:
                print("\n[Selesai] Proses unduh selesai dengan catatan/kendala.")

        elif pilihan in ("3", "keluar", "exit", "q"):
            print("\n[Selesai] Keluar dari program. Terima kasih!")
            break
        else:
            print("[Error] Pilihan menu tidak valid. Silakan pilih 1, 2, atau 3.")
            continue

        # Tanya user apakah ingin unduh lagi
        lagi = input("\nIngin mengunduh lagi? (y/n): ").strip().lower()
        if lagi not in ("y", "ya", "yes"):
            print("\n[Selesai] Program selesai. Sampai jumpa!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Dibatalkan] Program dihentikan pengguna.")
        sys.exit(0)
