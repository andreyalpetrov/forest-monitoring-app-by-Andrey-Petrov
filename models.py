from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FireAlert(db.Model):
    """Таблица алертов о пожарах"""
    __tablename__ = 'fire_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now, nullable=False)
    fire_detected = db.Column(db.Boolean, default=False, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    
    # Связь с изображениями
    images = db.relationship('AlertImage', backref='alert', 
                            lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<FireAlert {self.id} - {self.timestamp}>'

class AlertImage(db.Model):
    """Таблица для хранения информации об изображениях"""
    __tablename__ = 'alert_images'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('fire_alerts.id'), 
                        nullable=False)
    file_id = db.Column(db.String(36), unique=True, nullable=False)  # UUID
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)  # Путь на диске
    uploaded_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<AlertImage {self.file_id}>'
