from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import text  # 追加
import bcrypt
import qrcode
import io
import base64
from datetime import datetime, date, timedelta
import os

app = Flask(__name__)

# データベースのパスを修正（日本語パス対応）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'  # シンプルなパスに変更
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# CORS設定
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:5173"]}})

# データベースモデル
class User(db.Model):
    __tablename__ = 'user'
    
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_info = db.Column(db.Text)
    company_dept_club = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーションシップ
    attendances = db.relationship('Attendance', backref='user', lazy=True)
    exceptions = db.relationship('ExceptionRecord', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Subject(db.Model):
    __tablename__ = 'subject'
    
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String(100), nullable=False)
    attendance_time = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーションシップ
    attendances = db.relationship('Attendance', backref='subject', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    attendance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    attendance_status = db.Column(db.String(20), nullable=False)
    attendance_time = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ExceptionRecord(db.Model):
    __tablename__ = 'exception'
    
    exception_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Health check route
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        # データベース接続テスト
        db.session.execute(text('SELECT 1'))
        
        # オプションライブラリの確認
        optional_libs = {}
        try:
            import pandas
            optional_libs['pandas'] = 'available'
        except ImportError:
            optional_libs['pandas'] = 'not installed'
        
        try:
            import openpyxl
            optional_libs['openpyxl'] = 'available'
        except ImportError:
            optional_libs['openpyxl'] = 'not installed'
        
        return jsonify({
            'status': 'ok',
            'database': 'connected',
            'optional_libraries': optional_libs,
            'excel_import': 'available' if all(lib == 'available' for lib in optional_libs.values()) else 'disabled'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# Error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization token is required'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token'}), 401

# Auth Routes
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_name = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user_info = data.get('user_info', '')
        company_dept_club = data.get('company_dept_club', '')
        
        if not user_name or not email or not password:
            return jsonify({'error': 'All required fields must be provided'}), 400
        
        if User.query.filter_by(user_name=user_name).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            user_name=user_name, 
            email=email,
            user_info=user_info,
            company_dept_club=company_dept_club
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        print(f"Registration error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_name = data.get('username')
        password = data.get('password')
        
        if not user_name or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(user_name=user_name).first()
        
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.user_id))
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user.user_id,
                    'username': user.user_name,
                    'email': user.email,
                    'user_info': user.user_info,
                    'company_dept_club': user.company_dept_club
                }
            }), 200
        
        return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.user_id,
            'username': user.user_name,
            'email': user.email,
            'user_info': user.user_info,
            'company_dept_club': user.company_dept_club
        }), 200
    except Exception as e:
        print(f"Profile error: {e}")
        return jsonify({'error': 'Failed to get profile'}), 500

# 科目管理
@app.route('/api/subjects', methods=['GET'])
@jwt_required()
def get_subjects():
    try:
        subjects = Subject.query.all()
        result = []
        for subject in subjects:
            result.append({
                'id': subject.subject_id,
                'name': subject.subject_name,
                'attendance_time': subject.attendance_time,
                'description': subject.description or ''
            })
        return jsonify(result), 200
    except Exception as e:
        print(f"Get subjects error: {e}")
        return jsonify({'error': 'Failed to get subjects'}), 500

@app.route('/api/subjects', methods=['POST'])
@jwt_required()
def create_subject():
    try:
        data = request.get_json()
        subject_name = data.get('name')
        attendance_time = data.get('attendance_time', '')
        description = data.get('description', '')
        
        if not subject_name:
            return jsonify({'error': 'Subject name is required'}), 400
        
        subject = Subject(
            subject_name=subject_name,
            attendance_time=attendance_time,
            description=description
        )
        
        db.session.add(subject)
        db.session.commit()
        
        return jsonify({'message': 'Subject created successfully'}), 201
    except Exception as e:
        print(f"Create subject error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create subject'}), 500

# 出勤記録
@app.route('/api/attendance', methods=['POST'])
@jwt_required()
def record_attendance():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        subject_id = data.get('subject_id')
        date_str = data.get('date', str(date.today()))
        attendance_status = data.get('status', '出勤')
        attendance_time = data.get('time', '')
        
        if not subject_id:
            return jsonify({'error': 'Subject ID is required'}), 400
        
        # 既存の記録をチェック
        existing = Attendance.query.filter_by(
            user_id=user_id,
            subject_id=subject_id,
            date=datetime.strptime(date_str, '%Y-%m-%d').date()
        ).first()
        
        if existing:
            return jsonify({'error': 'Attendance already recorded for this date and subject'}), 400
        
        attendance = Attendance(
            user_id=user_id,
            subject_id=subject_id,
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            attendance_status=attendance_status,
            attendance_time=attendance_time
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({'message': 'Attendance recorded successfully'}), 201
    except Exception as e:
        print(f"Record attendance error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to record attendance'}), 500

@app.route('/api/attendance', methods=['GET'])
@jwt_required()
def get_attendance():
    try:
        user_id = int(get_jwt_identity())
        attendances = db.session.query(Attendance, Subject).join(Subject).filter(
            Attendance.user_id == user_id
        ).order_by(Attendance.date.desc()).all()
        
        result = []
        for attendance, subject in attendances:
            result.append({
                'id': attendance.attendance_id,
                'date': attendance.date.isoformat(),
                'subject_name': subject.subject_name,
                'status': attendance.attendance_status,
                'time': attendance.attendance_time
            })
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Get attendance error: {e}")
        return jsonify({'error': 'Failed to get attendance'}), 500

@app.route('/api/exceptions', methods=['POST'])
@jwt_required()
def create_exception():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        date_str = data.get('date', str(date.today()))
        reason = data.get('reason', '')
        notes = data.get('notes', '')
        
        exception_record = ExceptionRecord(
            user_id=user_id,
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            reason=reason,
            notes=notes
        )
        
        db.session.add(exception_record)
        db.session.commit()
        
        return jsonify({'message': 'Exception recorded successfully'}), 201
    except Exception as e:
        print(f"Create exception error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create exception'}), 500

@app.route('/api/exceptions', methods=['GET'])
@jwt_required()
def get_exceptions():
    try:
        user_id = int(get_jwt_identity())
        exceptions = ExceptionRecord.query.filter_by(user_id=user_id).order_by(ExceptionRecord.date.desc()).all()
        
        result = []
        for exc in exceptions:
            result.append({
                'id': exc.exception_id,
                'date': exc.date.isoformat(),
                'reason': exc.reason,
                'notes': exc.notes
            })
        
        return jsonify(result), 200
    except Exception as e:
        print(f"Get exceptions error: {e}")
        return jsonify({'error': 'Failed to get exceptions'}), 500

# QRコード生成
@app.route('/api/generate-qr', methods=['POST'])
@jwt_required()
def generate_qr():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json() or {}
        target_date = data.get('date', str(date.today()))
        
        qr_data = f"{user.user_name}:{target_date}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode()
        
        return jsonify({
            'qr_code': f"data:image/png;base64,{img_base64}",
            'data': qr_data,
            'date': target_date
        }), 200
    except Exception as e:
        print(f"QR generation error: {e}")
        return jsonify({'error': 'QR generation failed'}), 500

# データベース初期化用のルート
@app.route('/api/init-db', methods=['POST'])
def init_database():
    try:
        # 既存のテーブルを削除
        db.drop_all()
        print("Existing tables dropped")
        
        # 新しいテーブルを作成
        db.create_all()
        print("New tables created")
        
        # デフォルトの科目を追加
        default_subjects = [
            {'name': '数学', 'time': '9:00-10:30', 'description': '基礎数学'},
            {'name': '英語', 'time': '10:45-12:15', 'description': '英語コミュニケーション'},
            {'name': '物理', 'time': '13:15-14:45', 'description': '物理学基礎'},
            {'name': '化学', 'time': '15:00-16:30', 'description': '化学実験'}
        ]
        
        for subject_data in default_subjects:
            subject = Subject(
                subject_name=subject_data['name'],
                attendance_time=subject_data['time'],
                description=subject_data['description']
            )
            db.session.add(subject)
        
        db.session.commit()
        print("Default subjects added")
        
        return jsonify({'message': 'Database initialized successfully'}), 200
    except Exception as e:
        print(f"Database initialization error: {e}")
        db.session.rollback()
        return jsonify({'error': 'Database initialization failed'}), 500

if __name__ == '__main__':
    try:
        with app.app_context():
            # 自動的にテーブルを作成（初回起動時）
            db.create_all()
            print("Database tables created successfully")
        print("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Failed to start application: {e}")
        print("Please check your dependencies and database configuration")