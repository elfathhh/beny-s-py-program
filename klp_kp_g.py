import random

def bagi_kelompok():
    nama = ["juan", "ali", "kevi", "oci",
            "nida", "cahya", "hanin", "faty",
            "intan", "izul", "zizah", "dian",
            "mira", "zin", "lisma", "pipah", "aku", "hendra", "dony"]

    tema = ["AI untuk pendidikan islam", "dakwah digital", "etika sosial media", "teknologi dan ekonomi syarian"]

    # Acak urutan nama
    random.shuffle(nama)

    # Hitung jumlah anggota per kelompok
    total_nama = len(nama)
    jumlah_kelompok = len(tema)
    
    # Pembagian merata: 19 nama / 4 kelompok = 4, 5, 5, 5
    anggota_per_kelompok = [total_nama // jumlah_kelompok] * jumlah_kelompok
    sisa = total_nama % jumlah_kelompok
    
    # Distribusikan sisa anggota ke kelompok awal
    for i in range(sisa):
        anggota_per_kelompok[i] += 1

    # Bagi nama ke kelompok
    kelompok = []
    idx = 0
    for i in range(jumlah_kelompok):
        anggota = nama[idx:idx + anggota_per_kelompok[i]]
        kelompok.append(anggota)
        idx += anggota_per_kelompok[i]

    # Tampilkan hasil
    print("=" * 70)
    print("HASIL PEMBAGIAN KELOMPOK DAN TEMA".center(70))
    print("=" * 70)
    
    for i in range(jumlah_kelompok):
        print(f"\n🔹 KELOMPOK {i+1}")
        # print(f"   Tema: {tema[i]}")
        print(f"   Anggota ({len(kelompok[i])} orang):")
        for j, nama_anggota in enumerate(kelompok[i], 1):
            print(f"      {j}. {nama_anggota.capitalize()}")
    
    print("\n" + "=" * 70)

# Jalankan program
if __name__ == "__main__":
    bagi_kelompok()