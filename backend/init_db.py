#!/usr/bin/env python3
"""
シンプルなデータベース初期化スクリプト
"""

import os
import sys
from datetime import date, datetime

# Flaskアプリのパスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """必要な依存関係をチェック"""
    missing_deps = []
    
    try:
        import flask
    except ImportError:
        missing_deps.append('Flask')
    
    try:
        import flask_sqlalchemy
    except ImportError:
        missing_deps.append('Flask-SQLAlchemy')
    
    try:
        import flask_cors
    except ImportError:
        missing_deps.append('Flask-CORS')
    
    try:
        import flask_jwt_extended
    except ImportError:
        missing_deps.append('Flask-JWT-Extended')
    
    try:
        import bcrypt
    except ImportError:
        missing_deps.append('bcrypt')
    
    try:
        import qrcode
    except ImportError:
        missing_deps.append('qrcode')
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append('Pillow')
    
    if missing_deps:
        print("❌ 以下の必須パッケージがインストールされていません:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\n以下のコマンドでインストールしてください:")
        print("pip install Flask Flask-SQLAlchemy Flask-CORS Flask-JWT-Extended bcrypt qrcode Pillow")
        return False
    
    print("✅ すべての必須パッケージがインストールされています")
    return True

def init_database():
    """データベースを初期化する"""
    if not check_dependencies():
        return False
    
    try:
        # app.pyからモデルをインポート
        from app import app, db, User, Subject, Attendance, ExceptionRecord
        
        with app.app_context():
            print("🗄️  データベースを初期化しています...")
            
            # 既存のデータベースファイルを削除
            db_path = 'attendance.db'
            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"🗑️  既存のデータベースファイル '{db_path}' を削除しました")
            
            # 新しいテーブルを作成（drop_allは使わない）
            db.create_all()
            print("🏗️  新しいテーブルを作成しました")
            
            # サンプルデータを作成
            create_sample_data(db, User, Subject, Attendance, ExceptionRecord)
            
            print("✅ データベースの初期化が完了しました！")
            return True
        
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("必要なモジュールがインストールされていない可能性があります")
        return False
    except Exception as e:
        print(f"❌ データベース初期化エラー: {e}")
        return False

def create_sample_data(db, User, Subject, Attendance, ExceptionRecord):
    """サンプルデータを作成する"""
    try:
        print("📝 サンプルデータを作成しています...")
        
        # デフォルトの科目を追加
        subjects_data = [
            {'name': '数学', 'time': '9:00-10:30', 'description': '基礎数学'},
            {'name': '英語', 'time': '10:45-12:15', 'description': '英語コミュニケーション'},
            {'name': '物理', 'time': '13:15-14:45', 'description': '物理学基礎'},
            {'name': '化学', 'time': '15:00-16:30', 'description': '化学実験'},
            {'name': 'プログラミング', 'time': '19:00-20:30', 'description': 'プログラミング基礎'}
        ]
        
        for subject_data in subjects_data:
            subject = Subject(
                subject_name=subject_data['name'],
                attendance_time=subject_data['time'],
                description=subject_data['description']
            )
            db.session.add(subject)
        
        # テストユーザーを作成
        test_users = [
            {
                'username': 'test_user',
                'email': 'test@example.com',
                'password': 'password123',
                'user_info': 'テストユーザー1',
                'company': 'テスト会社'
            },
            {
                'username': 'student1',
                'email': 'student1@school.com',
                'password': 'password123',
                'user_info': '学生ユーザー',
                'company': '○○大学'
            }
        ]
        
        for user_data in test_users:
            user = User(
                user_name=user_data['username'],
                email=user_data['email'],
                user_info=user_data['user_info'],
                company_dept_club=user_data['company']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        
        # 変更をコミット
        db.session.commit()
        
        print("📚 登録された科目:")
        for subject_data in subjects_data:
            print(f"   - {subject_data['name']} ({subject_data['time']})")
        
        print("\n👥 テストユーザー:")
        for user_data in test_users:
            print(f"   - {user_data['username']} ({user_data['email']})")
        
    except Exception as e:
        print(f"❌ サンプルデータ作成エラー: {e}")
        db.session.rollback()
        raise

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 勤怠管理システム データベース初期化")
    print("=" * 50)
    
    # 確認プロンプト
    response = input("\n既存のデータはすべて削除されます。続行しますか？ (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        if init_database():
            print("\n" + "=" * 50)
            print("🎉 初期化完了!")
            print("=" * 50)
            print("以下の認証情報でテストできます:")
            print("ユーザー名: test_user")
            print("パスワード: password123")
            print("\nまたは")
            print("ユーザー名: student1") 
            print("パスワード: password123")
            print("\n次に以下のコマンドでサーバーを起動してください:")
            print("python app.py")
        else:
            print("\n❌ 初期化に失敗しました")
            sys.exit(1)
    else:
        print("初期化をキャンセルしました")