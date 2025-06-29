from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import text
import bcrypt
import qrcode
import io
import base64
from datetime import datetime, date, timedelta
import os
import tempfile
import json

app = Flask(__name__)

# データベースのパスを修正（日本語パス対応）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
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
    teacher_name = db.Column(db.String(100))
    department = db.Column(db.String(100))
    credits = db.Column(db.Float)
    excel_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーションシップ
    attendances = db.relationship('Attendance', backref='subject', lazy=True)
    schedules = db.relationship('SubjectSchedule', backref='subject', lazy=True)

class SubjectSchedule(db.Model):
    __tablename__ = 'subject_schedule'
    
    schedule_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'), nullable=False)
    schedule_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    hours = db.Column(db.Float)
    location = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
            
        try:
            import xlrd
            optional_libs['xlrd'] = 'available'
        except ImportError:
            optional_libs['xlrd'] = 'not installed'
        
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
                'description': subject.description or '',
                'teacher_name': subject.teacher_name or '',
                'department': subject.department or '',
                'credits': subject.credits
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

# 科目詳細情報の取得
@app.route('/api/subjects/<int:subject_id>', methods=['GET'])
@jwt_required()
def get_subject_detail(subject_id):
    try:
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({'error': '科目が見つかりません'}), 404
        
        # スケジュール情報も取得
        schedules = SubjectSchedule.query.filter_by(subject_id=subject_id).order_by(SubjectSchedule.schedule_date).all()
        
        result = {
            'id': subject.subject_id,
            'name': subject.subject_name,
            'attendance_time': subject.attendance_time,
            'description': subject.description,
            'teacher_name': subject.teacher_name,
            'department': subject.department,
            'credits': subject.credits,
            'excel_data': subject.excel_data,
            'schedules': []
        }
        
        for schedule in schedules:
            result['schedules'].append({
                'id': schedule.schedule_id,
                'date': schedule.schedule_date.isoformat() if schedule.schedule_date else None,
                'start_time': schedule.start_time.strftime('%H:%M') if schedule.start_time else None,
                'end_time': schedule.end_time.strftime('%H:%M') if schedule.end_time else None,
                'hours': schedule.hours,
                'location': schedule.location,
                'notes': schedule.notes
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Get subject detail error: {e}")
        return jsonify({'error': '科目詳細の取得に失敗しました'}), 500

# エクセルファイルのインポート機能
@app.route('/api/import-excel', methods=['POST'])
@jwt_required()
def import_excel():
    try:
        # オプションライブラリのチェック
        try:
            import pandas as pd
            import openpyxl
            import xlrd
        except ImportError as e:
            missing_lib = str(e).split("'")[1] if "'" in str(e) else "pandas, openpyxl, または xlrd"
            return jsonify({
                'error': f'必要なライブラリ "{missing_lib}" がインストールされていません。\n以下のコマンドを実行してください:\npip install pandas openpyxl xlrd'
            }), 500
        
        if 'file' not in request.files:
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'ファイル名が空です'}), 400
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'エクセルファイル(.xlsx, .xls)を選択してください'}), 400
        
        # ファイルサイズをチェック
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # ファイルポインタを先頭に戻す
        
        if file_size == 0:
            return jsonify({'error': 'ファイルが空です'}), 400
        
        if file_size > 10 * 1024 * 1024:  # 10MB制限
            return jsonify({'error': 'ファイルサイズが大きすぎます（10MB以下にしてください）'}), 400
        
        # ファイル内容を読み込んで検証
        file_content = file.read()
        file.seek(0)  # ファイルポインタを再び先頭に戻す
        
        # HTMLファイルかどうかをチェック（より厳密に）
        content_start = file_content[:100].lower()
        if b'<!doctype html' in content_start or b'<html' in content_start or b'<head>' in content_start:
            return jsonify({'error': 'HTMLファイルが選択されています。エクセルファイル(.xlsx, .xls)を選択してください'}), 400
        
        # ファイルの先頭バイトをチェックしてフォーマットを確認
        if file.filename.lower().endswith('.xlsx'):
            # .xlsxファイルはZIPファイルとして始まる（PKまたはZIPヘッダー）
            if not (file_content.startswith(b'PK\x03\x04') or file_content.startswith(b'PK\x05\x06') or file_content.startswith(b'PK\x07\x08')):
                # より緩い検証：先頭がPKで始まっていればOK
                if not file_content.startswith(b'PK'):
                    return jsonify({'error': 'この.xlsxファイルは正しい形式ではありません。Excelで保存し直してください。'}), 400
        elif file.filename.lower().endswith('.xls'):
            # .xlsファイルの検証を緩くする
            valid_xls_headers = [
                b'\xd0\xcf\x11\xe0',  # OLE2 Document
                b'\x09\x08',          # BIFF5/BIFF8
                b'\x09\x00',          # BIFF2
                b'\x09\x02',          # BIFF3
                b'\x09\x04',          # BIFF4
                b'\x08\x05',          # BIFF5
                b'\x08\x08'           # BIFF8
            ]
            
            is_valid_xls = any(file_content.startswith(header) for header in valid_xls_headers)
            if not is_valid_xls:
                # さらに緩い検証：ファイルサイズが妥当で、明らかにテキストファイルでなければOK
                if len(file_content) < 512:
                    return jsonify({'error': 'ファイルが小さすぎます。正しいエクセルファイルを選択してください。'}), 400
                
                # テキストファイルかどうかの簡易チェック
                try:
                    file_content[:1024].decode('utf-8')
                    # デコードできた場合はテキストファイルの可能性が高い
                    return jsonify({'error': 'テキストファイルが選択されています。エクセルファイル(.xlsx, .xls)を選択してください。'}), 400
                except UnicodeDecodeError:
                    # デコードできない場合はバイナリファイル（エクセルファイルの可能性）
                    pass
        
        # 一時ファイルに保存
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
        try:
            file.save(temp_file.name)
            temp_file.close()  # ファイルハンドルを閉じる
            
            subjects_created = 0
            schedules_created = 0
            excel_content = {}
            
            # ファイル拡張子に応じてエンジンを選択
            file_extension = file.filename.lower().split('.')[-1]
            engine = 'openpyxl' if file_extension == 'xlsx' else 'xlrd'
            
            # 全体のエクセルファイル内容を保存用に読み込み
            try:
                df_all_sheets = pd.read_excel(temp_file.name, sheet_name=None, engine=engine)
                for sheet_name, df in df_all_sheets.items():
                    excel_content[sheet_name] = df.to_dict('records')
            except Exception as e:
                print(f"Excel reading error: {e}")
                error_msg = str(e)
                if 'Unsupported format' in error_msg or 'corrupt file' in error_msg:
                    return jsonify({'error': 'エクセルファイルの形式が正しくないか、ファイルが破損しています。別のファイルを試してください。'}), 400
                elif 'No such file or directory' in error_msg:
                    return jsonify({'error': 'ファイルの保存に失敗しました。もう一度試してください。'}), 400
                else:
                    return jsonify({'error': f'エクセルファイルの読み込みに失敗しました: {error_msg}'}), 400
            
            # シート名を確認
            if not excel_content:
                return jsonify({'error': 'エクセルファイルにシートが見つかりません'}), 400
            
            # Sheet1: 科目基本情報を読み込み
            try:
                df_sheet1 = pd.read_excel(temp_file.name, sheet_name=0, header=None, engine=engine)
                
                # データが存在するかチェック
                if df_sheet1.empty:
                    return jsonify({'error': 'Sheet1にデータが見つかりません'}), 400
                
                # エクセルファイルの構造に基づいて科目情報を抽出
                if len(df_sheet1) >= 3 and len(df_sheet1.columns) >= 4:
                    # 科目名はB3から取得
                    subject_name = str(df_sheet1.iloc[2, 1]) if pd.notna(df_sheet1.iloc[2, 1]) else 'Unknown Subject'
                    teacher_name = str(df_sheet1.iloc[0, 1]) if pd.notna(df_sheet1.iloc[0, 1]) else ''
                    department = str(df_sheet1.iloc[1, 1]) if pd.notna(df_sheet1.iloc[1, 1]) else ''
                    attendance_time = str(df_sheet1.iloc[2, 3]) if pd.notna(df_sheet1.iloc[2, 3]) else ''
                    schedule_info = str(df_sheet1.iloc[0, 3]) if pd.notna(df_sheet1.iloc[0, 3]) else ''
                    
                    # 科目名が有効かチェック
                    if subject_name == 'Unknown Subject' or subject_name.strip() == '':
                        return jsonify({'error': 'エクセルファイルから科目名を取得できませんでした。ファイル形式を確認してください。'}), 400
                    
                    # 既存の科目をチェック
                    existing_subject = Subject.query.filter_by(subject_name=subject_name).first()
                    if not existing_subject:
                        # 新しい科目を作成
                        subject = Subject(
                            subject_name=subject_name,
                            attendance_time=attendance_time,
                            description=f"{schedule_info}\n{str(df_sheet1.iloc[1, 3]) if pd.notna(df_sheet1.iloc[1, 3]) else ''}".strip(),
                            teacher_name=teacher_name,
                            department=department,
                            credits=2.0,  # デフォルト値
                            excel_data=json.dumps(excel_content, ensure_ascii=False)  # JSONとして保存
                        )
                        
                        db.session.add(subject)
                        subjects_created += 1
                        
                        # 新しく作成した科目のIDを取得するためにflush
                        db.session.flush()
                        new_subject_id = subject.subject_id
                    else:
                        # 既存科目のエクセルデータを更新
                        existing_subject.excel_data = json.dumps(excel_content, ensure_ascii=False)
                        new_subject_id = existing_subject.subject_id
                else:
                    return jsonify({'error': 'Sheet1のデータ形式が正しくありません。必要なセル（A1:D3）にデータがあることを確認してください。'}), 400
                
            except Exception as e:
                print(f"Sheet1 processing error: {e}")
                return jsonify({'error': f'Sheet1の処理中にエラーが発生しました: {str(e)}'}), 400
            
            # Sheet2: スケジュール情報を読み込み
            try:
                if len(excel_content) > 1:  # Sheet2が存在する場合
                    df_sheet2 = pd.read_excel(temp_file.name, sheet_name=1, header=0, engine=engine)
                    
                    if new_subject_id and not df_sheet2.empty:
                        for _, row in df_sheet2.iterrows():
                            # 出講日の列（B列）からデータを取得
                            if len(row) > 1 and pd.notna(row.iloc[1]) and str(row.iloc[1]).strip():
                                date_str = str(row.iloc[1]).strip()
                                
                                # 日付を解析
                                schedule_date = None
                                try:
                                    # "4月8日"形式を2024年の日付に変換
                                    import re
                                    match = re.match(r'(\d+)月(\d+)日', date_str)
                                    if match:
                                        month = int(match.group(1))
                                        day = int(match.group(2))
                                        # 年度を推定（4月以降は当年、1-3月は翌年）
                                        year = 2024 if month >= 4 else 2025
                                        schedule_date = datetime(year, month, day).date()
                                except:
                                    pass
                                
                                if schedule_date:
                                    # 時間数を取得（F列）
                                    hours = 2.0  # デフォルト値
                                    if len(row) > 5 and pd.notna(row.iloc[5]):
                                        try:
                                            hours = float(row.iloc[5])
                                        except:
                                            hours = 2.0
                                    
                                    # 備考を取得（G列）
                                    notes = str(row.iloc[6]) if len(row) > 6 and pd.notna(row.iloc[6]) else ''
                                    
                                    # 既存スケジュールをチェック
                                    existing_schedule = SubjectSchedule.query.filter_by(
                                        subject_id=new_subject_id,
                                        schedule_date=schedule_date
                                    ).first()
                                    
                                    if not existing_schedule:
                                        schedule = SubjectSchedule(
                                            subject_id=new_subject_id,
                                            schedule_date=schedule_date,
                                            hours=hours,
                                            location='',
                                            notes=notes
                                        )
                                        
                                        db.session.add(schedule)
                                        schedules_created += 1
                                        
            except Exception as e:
                print(f"Sheet2 processing error: {e}")
                # Sheet2のエラーは警告として扱い、処理を継続
            
            db.session.commit()
            
            return jsonify({
                'message': 'インポートが完了しました',
                'subjects_created': subjects_created,
                'schedules_created': schedules_created
            }), 200
            
        finally:
            # 一時ファイルを削除
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            
    except Exception as e:
        db.session.rollback()
        print(f"Import error: {e}")
        return jsonify({'error': f'インポートに失敗しました: {str(e)}'}), 500

# テンプレートファイルのダウンロード
@app.route('/api/download-template', methods=['GET'])
@jwt_required()
def download_template():
    try:
        # オプションライブラリのチェック
        try:
            import pandas as pd
        except ImportError:
            return jsonify({
                'error': '必要なライブラリがインストールされていません。pip install pandas openpyxl を実行してください'
            }), 500
        
        # テンプレートデータを作成
        subjects_data = {
            '科目名': ['数学', '英語', '物理'],
            '授業時間': ['9:00-10:30', '10:45-12:15', '13:15-14:45'],
            '説明': ['基礎数学', '英語コミュニケーション', '物理学基礎'],
            '担当者': ['田中先生', 'スミス先生', '佐藤先生'],
            '学部': ['理工学部', '文学部', '理工学部'],
            '単位数': [2, 2, 3]
        }
        
        schedules_data = {
            '科目名': ['数学', '数学', '英語'],
            '日付': ['2024-01-15', '2024-01-22', '2024-01-16'],
            '時間数': [1.5, 1.5, 1.5],
            '場所': ['A101', 'A101', 'B205'],
            '備考': ['第1回', '第2回', '第1回']
        }
        
        # 一時ファイルを作成
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        
        with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
            pd.DataFrame(subjects_data).to_excel(writer, sheet_name='科目基本情報', index=False)
            pd.DataFrame(schedules_data).to_excel(writer, sheet_name='スケジュール', index=False)
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name='attendance_template.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        print(f"Template download error: {e}")
        return jsonify({'error': f'テンプレートダウンロードに失敗しました: {str(e)}'}), 500

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