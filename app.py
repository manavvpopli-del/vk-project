import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import face_recognition
import numpy as np
import cv2

app = Flask(__name__)
# Digər saytlardan (sənin əsas saytından) gələn sorğulara icazə vermək üçün
CORS(app)

@app.route('/')
def home():
    return "OSINT Face Analyzer API is Running!"

@app.route('/analyze-face', methods=['POST'])
def analyze_face():
    # 1. Şəklin gəlib-gəlmədiyini yoxla
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "Şəkil yüklənməyib"}), 400
    
    file = request.files['image']
    
    try:
        # 2. Şəkli yaddaşa yüklə və emal et
        image_data = face_recognition.load_image_file(file)
        
        # 3. Üzün yerini tap
        face_locations = face_recognition.face_locations(image_data)
        
        if not face_locations:
            return jsonify({"status": "error", "message": "Şəkildə üz tapılmadı"}), 404

        # 4. Üzün 128 nöqtəli biometrik kodunu (encoding) çıxar
        face_encodings = face_recognition.face_encodings(image_data, face_locations)
        
        # İlk tapılan üzün kodunu list formatına salıb qaytarırıq
        vector_id = face_encodings[0].tolist()

        return jsonify({
            "status": "success",
            "face_count": len(face_locations),
            "face_vector": vector_id,
            "message": "Analiz tamamlandı"
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Serverin portunu dinamik təyin edirik (Render üçün vacibdir)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)