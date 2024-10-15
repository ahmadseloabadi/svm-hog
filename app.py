from flask import Flask,render_template,request,redirect,jsonify
import predict as pred
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)


# Fungsi utama untuk memproses gambar dan menampilkan prediksi
def predik(image_path=None,filename=None):
    if image_path:
        latters=pred.recognize_and_display_image(image_path,filename)
    else:
        latters="gagal bro"
    return latters

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

@app.route('/', methods=['GET', 'POST'])
def index():
   

    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        # Simpan file dengan aman
        filename = secure_filename(file.filename)
        file_path = os.path.join( "static/img/uploads/", filename)
        file.save(file_path)

        # membuat sub folder di dalam folder output
        file_output=os.path.join('static/img/output/', filename)
        create_folder(file_output)

        if os.path.exists(f'static/img/output/{filename}'):
            file_prepro=os.path.join(file_output, 'prepro')
            create_folder(file_prepro)
            print("file_prepro: ",file_prepro)
            file_gif=os.path.join(file_output, 'gif')
            create_folder(file_gif)
            file_result=os.path.join(file_output, 'result')
            create_folder(file_result)

        predict=predik(image_path=file_path,filename=filename)
        predict = ' '.join([str(item) for item in predict])
        return jsonify({'prediction': str(predict), 'file_name': filename,'result_images': os.listdir(os.path.join(file_output, 'result')),'prepro_images': os.listdir(os.path.join(file_output, 'prepro')),'gif_images': os.listdir(os.path.join(file_output, 'gif'))})
        

if __name__ == '__main__':
    app.run(debug=True)