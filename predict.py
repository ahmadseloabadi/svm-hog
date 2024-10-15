import cv2
from PIL import Image as PILImage
from skimage.feature import hog
from PIL import Image 
from joblib import dump, load
import imageio  # For creating GIFs
import imutils
import numpy as np
import os
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import matplotlib.image as plt_image

best_svm_classifier = load('static/model/svm_classifier.joblib')
label_encoder = load('static/model/label_encoder.joblib')

# Fungsi untuk mengurutkan kontur (kiri ke kanan atau atas ke bawah)
def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)

# Fungsi untuk praproses gambar
def preprocess_image(image):
    image = cv2.resize(image, (64, 64))  # Resize image to 64 x 64
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)  # Gaussian Blur to reduce noise
    _, thresh_image = cv2.threshold(blurred_image, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)  # Thresholding
    scaled_image = thresh_image / 255.0  # Normalize using Min-Max Scaling
    return scaled_image

# Fungsi untuk ekstraksi fitur HOG
def extract_hog_features(image):
    features,hog_image = hog(image, pixels_per_cell=(8, 8), cells_per_block=(4, 4), block_norm='L2-Hys', feature_vector=True,visualize=True)
    return features,hog_image

# Fungsi untuk menghitung ukuran fitur HOG yang diharapkan
def calculate_expected_hog_feature_size(image_size, pixels_per_cell, cells_per_block, orientations):
    n_cells = (image_size[0] // pixels_per_cell[0], image_size[1] // pixels_per_cell[1])
    block_size = cells_per_block[0] * cells_per_block[1] * orientations
    n_blocks = (n_cells[0] - cells_per_block[0] + 1, n_cells[1] - cells_per_block[1] + 1)
    return n_blocks[0] * n_blocks[1] * block_size

# Fungsi untuk memprediksi satu karakter
def recognize_single_character(image, expected_feature_size):
    preprocessed_image = preprocess_image(image)  # Preprocessing gambar
    hog_features,hog_image = extract_hog_features(preprocessed_image)  # Ekstraksi fitur HOG

    if hog_features.size != expected_feature_size:  # Pastikan dimensi fitur sesuai dengan model
        raise ValueError(f'Ketidakcocokan ukuran fitur: Diharapkan {expected_feature_size}, tetapi didapat {hog_features.size}')

    hog_features = hog_features.reshape(1, -1)  # Reshape untuk model SVM
    prediction = best_svm_classifier.predict(hog_features)  # Prediksi karakter menggunakan model SVM
    character = label_encoder.inverse_transform(prediction)  # Transformasikan prediksi ke label aslinya
    return character[0], preprocessed_image,hog_image

# Fungsi untuk mendapatkan karakter dari bounding box
# Fungsi untuk mendapatkan karakter dari bounding box
def get_letters(img_path,filename):

    letters = []
    frames = []  # Store frames for GIF creation

    # Konversi gambar ke skala abu-abu dan binarisasi
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian Blurring
    ret, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)

    # Increase dilation to close gaps within characters
    kernel = np.ones((5,5), np.uint8)  # Larger kernel
    dilated = cv2.dilate(thresh1, kernel, iterations=2)

    # mendapatkan contours
    cnts = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]
    i=0
    # Loop melalui kontur dan ekstrak karakter
    for c in cnts:
        if cv2.contourArea(c) > 10:
            i=i+1
            (x, y, w, h) = cv2.boundingRect(c)
            roi = image[y:y + h, x:x + w]  # Ambil gambar di dalam bounding box

            # Tambahkan padding untuk meningkatkan prediksi
            bordersize = int(0.1 * x)
            roi = cv2.copyMakeBorder(
                roi,
                top=bordersize,
                bottom=bordersize,
                left=bordersize,
                right=bordersize,
                borderType=cv2.BORDER_CONSTANT,
                value=[255, 255, 255]
            )

            # Resize dan praproses karakter
            resized = cv2.resize(roi, (64, 64))
            preprocessed_image = preprocess_image(resized)

            # Ekstraksi fitur HOG dan prediksi karakter
            expected_feature_size = calculate_expected_hog_feature_size((64, 64), (8, 8), (4, 4), 9)
            predicted_character,preprocessed_image,hog_image = recognize_single_character(resized, expected_feature_size)

            # Konversi gambar dari skala abu-abu ke RGB untuk tampilan
            preprocessed_image_rgb = (preprocessed_image * 255).astype(np.uint8)
            preprocessed_image_rgb = cv2.cvtColor(preprocessed_image_rgb, cv2.COLOR_GRAY2RGB)

            # Tampilkan gambar dan hasil deteksi dalam tampilan menyamping
            plt.figure(figsize=(10, 4))
            plt.subplot(1, 4, 1)
            plt.imshow(resized)  # Tampilkan gambar asli
            plt.title(f'bounding box ke- {i}')
            plt.axis('off')

            plt.subplot(1, 4, 2)
            plt.imshow(preprocessed_image_rgb)  # Tampilkan gambar asli
            plt.title(f'preprocessing')
            plt.axis('off')

            plt.subplot(1, 4, 3)
            plt.imshow(hog_image)
            plt.title(f'HOG')
            plt.axis('off')

            plt.subplot(1, 4, 4)
            plt.imshow(preprocessed_image)
            plt.title(f'Hasil Deteksi: {predicted_character}')
            plt.axis('off')
            # Simpan gambar sebagai file PNG
            plt.savefig(f'static/img/output/{filename}/prepro/{"".join(predicted_character)}_bounding_box_{i}.png', bbox_inches='tight')
            plt.close()


            # Simpan prediksi karakter
            letters.append(predicted_character)

            # Gambarkan bounding box dan label
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, predicted_character, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
          
            # Convert image for GIF
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for PIL
            frames.append(PILImage.fromarray(frame))
    gif_filename = f'static/img/output/{filename}/gif/{"".join(letters)}.gif'
    # Buat GIF dari semua frame yang ditangkap
    frames[0].save(gif_filename, save_all=True, append_images=frames[1:], duration=500, loop=0)

    return letters, image

# Fungsi untuk memproses gambar dan menampilkan hasil
def recognize_and_display_image(image_path,filename):
    
    image = cv2.imread(image_path)
    if image is None:
        print(f'Error: Gambar tidak ditemukan di {image_path}')
        return
    else:
        letters, image_with_boxes = get_letters(image_path,filename)
        # Tampilkan gambar dengan kotak dan prediksi
        plt.figure(figsize=(10, 6))
        plt.imshow(cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB))
        plt.title(f'Hasil Deteksi: {"".join(letters)}')
        plt.axis('off')
        plt.savefig(f'static/img/output/{filename}/result/{"".join(letters)}.png', bbox_inches='tight')
        plt.close()
        return letters


    # except ValueError as e:
    #     print(f'Error processing {image_path}: {e}')


