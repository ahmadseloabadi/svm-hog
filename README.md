# Klasifikasi Aksara Jawa menggunakan SVM dan Ekstraksi Fitur HOG

![image](https://github.com/user-attachments/assets/a2918e95-8cd4-4804-8f6c-72a25e453b60)

## Deskripsi Proyek

Proyek ini bertujuan untuk mengklasifikasikan aksara Jawa menggunakan metode Support Vector Machine (SVM) dengan ekstraksi fitur Histogram of Oriented Gradients (HOG). Aksara Jawa merupakan salah satu warisan budaya Indonesia yang perlu dilestarikan. Melalui aplikasi ini, pengenalan aksara Jawa dapat dilakukan secara otomatis menggunakan teknik machine learning.

## Fitur Utama

- Ekstraksi fitur menggunakan Histogram of Oriented Gradients (HOG)
- Klasifikasi menggunakan algoritma Support Vector Machine (SVM)
- Antarmuka aplikasi yang user-friendly
- Kemampuan untuk mengenali 20 karakter dasar aksara Jawa (aksara nglegena)
- Preprocessing gambar untuk meningkatkan akurasi klasifikasi

## Teknologi yang Digunakan

- Python 3.x
- OpenCV untuk pemrosesan gambar
- Scikit-learn untuk implementasi SVM
- Scikit-image untuk ekstraksi fitur HOG
- Tkinter untuk antarmuka grafis
- Pickle untuk menyimpan model terlatih

## Struktur Proyek

```
svm-hog/
│
├── app.py                      # Aplikasi utama (web interface)
├── predict.py                  # Modul prediksi karakter aksara Jawa
├── svm_hog.ipynb               # Notebook untuk pelatihan dan eksplorasi model
├── requirements.txt            # Daftar dependensi proyek
│
├── static/                     # File statis untuk web (CSS, JS, gambar)
│   └── styles.css
│
├── templates/                  # Template HTML untuk antarmuka web
│   └── index.html
│
└── README.md                   # Dokumentasi proyek (file ini)
```

## Cara Instalasi

1. Clone repository ini:
   ```
   git clone https://github.com/ahmadseloabadi/svm-hog.git
   ```

2. Masuk ke direktori proyek:
   ```
   cd svm-hog
   ```

3. Instal dependensi yang diperlukan:
   ```
   pip install -r requirements.txt
   ```

## Cara Penggunaan

### Menjalankan Aplikasi

1. Jalankan aplikasi melalui command line:
   ```
   python src/app.py
   ```

2. Gunakan antarmuka aplikasi untuk:
   - Memilih gambar aksara Jawa yang akan diklasifikasikan
   - Melihat hasil klasifikasi dan nilai confidence
   - Mencoba berbagai parameter HOG dan SVM

### Melatih Model

1. Siapkan dataset dalam format yang sesuai di direktori `dataset/`
2. Jalankan script pelatihan:
   ```
   python training/train_model.py
   ```

3. Model yang telah dilatih akan disimpan di direktori `models/`

## Metode Klasifikasi

### Ekstraksi Fitur HOG

Histogram of Oriented Gradients (HOG) adalah metode ekstraksi fitur yang menghitung histogram gradien lokal dari citra. Metode ini efektif untuk mendeteksi struktur dalam citra aksara Jawa dengan langkah-langkah:

1. Menghitung gradien citra pada arah x dan y
2. Menghitung magnitude dan orientasi gradien
3. Membagi citra menjadi sel-sel kecil
4. Menghitung histogram orientasi gradien untuk setiap sel
5. Menormalisasi histogram untuk mendapatkan fitur HOG

### Support Vector Machine (SVM)

SVM adalah algoritma pembelajaran mesin yang mencari hyperplane optimal untuk memisahkan data dari kelas-kelas berbeda. Dalam proyek ini, SVM dengan kernel RBF (Radial Basis Function) digunakan untuk klasifikasi aksara Jawa berdasarkan fitur HOG.

## Dataset

Dataset terdiri dari gambar aksara Jawa nglegena (aksara dasar) dengan 20 kelas karakter. Dataset diaugmentasi untuk meningkatkan performa model dengan teknik:
- Rotasi
- Scaling
- Translasi
- Perubahan kecerahan

## Hasil dan Evaluasi

Hasil evaluasi model menunjukkan:
- Akurasi: 86%
- Presisi rata-rata: 87%
- Recall rata-rata: 86%

Confusion matrix dan laporan klasifikasi lengkap dapat dilihat pada notebook evaluasi.

## Kontribusi

Kontribusi untuk pengembangan proyek ini sangat diterima. Silakan fork repository ini dan kirimkan pull request dengan perubahan yang Anda usulkan.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## Kontak

Ahmad Selo Abadi - [ahmadseloabadi@gmail.com](mailto:ahmadseloabadi@gmail.com)

Link Proyek: [https://github.com/ahmadseloabadi/svm-hog](https://github.com/ahmadseloabadi/svm-hog)
