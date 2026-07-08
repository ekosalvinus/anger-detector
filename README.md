## membuat virtual environment terlebih dahulu
``` bash
python3 -m venv venv

```

## Kemudian aktifkan virtual environment:
``` bash
source venv/bin/activate

```

## Setelah itu install dependencies (jika belum diinstal / pertama kasli dijalankan):
``` bash
pip install -r requirements.txt

```

## Start aplikasi

Tips: Setiap kali Anda membuka terminal baru, ingat untuk aktifkan virtual environment dengan menjalankan perintah `source venv/bin/activate` sebelum menjalankan program.

## Penjelasan:

- `python3 -m venv venv` → Membuat folder virtual environment bernama `venv`
- `source venv/bin/activate` → Mengaktifkan virtual environment (prompt akan berubah ke `(venv)`)
- Sekarang `pip install` akan berjalan di dalam virtual environment, bukan system-wide

## Setelah install selesai, jalankan program:
``` bash
python3 deteksi_marah.py

```