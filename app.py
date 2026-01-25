from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from models import db, FireAlert, AlertImage
from config import Config
import uuid

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config.from_object(Config)
CORS(app)

db.init_app(app)

# Создаем папку для загрузок если её нет
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.before_request
def create_tables():
    """Создаёт таблицы при первом запуске"""
    with app.app_context():
        db.create_all()

# ===== 1. Сохранение нового алерта о пожаре =====
@app.route('/api/alerts', methods=['POST'])
def create_alert():
    """
    POST /api/alerts
    Создает новое сообщение мониторинга с опциональными файлами
    
    JSON body:
    {
        "fire_detected": true/false,
        "comment": "текст комментария",
        "images": [base64 или файлы]
    }
    """
    try:
        data = request.form
        files = request.files.getlist('images')
        
        # Создаём новый алерт
        alert = FireAlert(
            timestamp=datetime.now(),
            fire_detected=data.get('fire_detected', 'false').lower() == 'true',
            comment=data.get('comment', '')
        )
        
        db.session.add(alert)
        db.session.flush()  # Получить ID алерта без коммита
        
        # Обработка загруженных файлов
        image_records = []
        for file in files:
            if file and file.filename.endswith('.png'):
                # Генерируем уникальное имя
                file_id = str(uuid.uuid4())
                filename = f"{file_id}.png"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                # Сохраняем файл
                file.save(filepath)
                
                # Создаём запись в БД
                image = AlertImage(
                    alert_id=alert.id,
                    file_id=file_id,
                    filename=filename,
                    file_path=filepath
                )
                image_records.append(image)
                db.session.add(image)
        
        db.session.commit()
        
        return jsonify({
            'id': alert.id,
            'timestamp': alert.timestamp.isoformat(),
            'images_count': len(image_records),
            'images': [{'id': img.file_id} for img in image_records]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ===== 2. Получение алертов за период =====
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """
    GET /api/alerts?hours=24
    Получает алерты за последние N часов (по умолчанию 24)
    """
    try:
        hours = request.args.get('hours', 24, type=int)
        since = datetime.now() - timedelta(hours=hours)
        
        alerts = FireAlert.query.filter(
            FireAlert.timestamp >= since
        ).order_by(FireAlert.timestamp.desc()).all()
        
        result = []
        for alert in alerts:
            images = AlertImage.query.filter_by(alert_id=alert.id).all()
            result.append({
                'id': alert.id,
                'timestamp': alert.timestamp.isoformat(),
                'fire_detected': alert.fire_detected,
                'comment': alert.comment,
                'images_count': len(images),
                'images': [{'id': img.file_id} for img in images]
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===== 3. Скачивание файла по ID =====
@app.route('/api/images/<file_id>', methods=['GET'])  # ← Path-параметр <file_id>
def download_image(file_id):
    """
    GET /api/images/{file_id}
    Скачивает изображение по его идентификатору
    """
    try:
        image = AlertImage.query.filter_by(file_id=file_id).first()
        
        if not image or not os.path.exists(image.file_path):
            return jsonify({'error': 'Image not found'}), 404
        
        return send_file(
            image.file_path,
            mimetype='image/png',
            as_attachment=True,
            download_name=image.filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
