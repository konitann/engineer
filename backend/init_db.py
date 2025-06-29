#!/usr/bin/env python3
"""
データベース初期化スクリプト
既存のデータベースを削除して、新しいER図に基づいた構造で再作成します。
"""

import os
import sys
from datetime import date, datetime

# Flaskアプリのパスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 必要なモジュールがインストールされているかチェック
try:
    from app import app, db, User, Subject, Attendance, Exception
except ImportError as e:
    print(f"エラー: 必要なモジュールがインストールされていません")
    print(f"詳細: {e}")
    print("\n以下のコマンドを実行してください:")
    print("pip install -r requirements.txt")
    print("\nまたは個別にインストール:")
    print("pip install Flask Flask-SQLAlchemy Flask-CORS Flask-JWT-Extended qrcode Pillow bcrypt")
    sys.exit(1)

def init_database():
    """データベースを初期化する"""
    with app.app_context():
        print("データベースを初期化しています...")
        
        # 既存のデータベースファイルを削除
        db_path = 'attendance.db'
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"既存のデータベースファイル '{db_path}' を削除しました")
        
        # 既存のテーブルを削除（念のため）
        try:
            db.drop_all()
            print("既存のテーブルを削除しました")
        except Exception as e:
            print(f"テーブル削除時の警告: {e}")
        
        # 新しいテーブルを作成
        db.create_all()
        print("新しいテーブルを作成しました")
        
        # サンプルデータを作成
        create_sample_data()
        
        print("データベースの初期化が完了しました！")

def create_sample_data():
    """サンプルデータを作成する"""
    try:
        print("サンプルデータを作成しています...")
        
        # デフォルトの科目を追加
        subjects_data = [
            {'name': '数学', 'time': '9:00-10:30'},
            {'name': '英語', 'time': '10:45-12:15'},
            {'name': '物理', 'time': '13:15-14:45'},
            {'name': '化学', 'time': '15:00-16:30'},
            {'name': '国語', 'time': '16:45-18:15'},
            {'name': 'プログラミング', 'time': '19:00-20:30'}
        ]
        
        for subject_data in subjects_data:
            subject = Subject(
                subject_name=subject_data['name'],
                attendance_time=subject_data['time']
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
        
        print("科目データを追加しました:")
        for subject_data in subjects_data:
            print(f"  - {subject_data['name']} ({subject_data['time']})")
        
        print("\nテストユーザーを追加しました:")
        for user_data in test_users:
            print(f"  - {user_data['username']} ({user_data['email']})")
        
        print("\nサンプル出勤記録を作成しています...")
        create_sample_attendance()
        
    except Exception as e:
        print(f"サンプルデータ作成エラー: {e}")
        db.session.rollback()

def create_sample_attendance():
    """サンプルの出勤記録を作成する"""
    try:
        # 作成したユーザーと科目を取得
        users = User.query.all()
        subjects = Subject.query.all()
        
        if not users or not subjects:
            print("ユーザーまたは科目が見つかりません")
            return
        
        # 過去1週間のサンプル出勤記録を作成
        import datetime
        today = datetime.date.today()
        
        sample_records = []
        for i in range(7):  # 過去7日間
            record_date = today - datetime.timedelta(days=i)
            
            for user in users:
                for j, subject in enumerate(subjects[:3]):  # 最初の3つの科目のみ
                    if (i + j) % 3 != 0:  # すべての記録を作らず、ランダム性を持たせる
                        continue
                    
                    status_options = ['出勤', '遅刻', '欠勤']
                    status = status_options[j % len(status_options)]
                    
                    attendance = Attendance(
                        user_id=user.user_id,
                        subject_id=subject.subject_id,
                        date=record_date,
                        attendance_status=status,
                        attendance_time=subject.attendance_time if status != '欠勤' else ''
                    )
                    sample_records.append(attendance)
        
        # サンプル例外記録も作成
        for user in users:
            exception = Exception(
                user_id=user.user_id,
                date=today - datetime.timedelta(days=2),
                reason='体調不良',
                notes='風邪のため欠席'
            )
            sample_records.append(exception)
        
        # 一括でデータベースに追加
        for record in sample_records:
            db.session.add(record)
        
        db.session.commit()
        print(f"サンプル記録 {len(sample_records)} 件を追加しました")
        
    except Exception as e:
        print(f"サンプル出勤記録作成エラー: {e}")
        db.session.rollback()

def verify_database():
    """データベースの内容を確認する"""
    with app.app_context():
        print("\n=== データベース内容確認 ===")
        
        print(f"ユーザー数: {User.query.count()}")
        print(f"科目数: {Subject.query.count()}")
        print(f"出勤記録数: {Attendance.query.count()}")
        print(f"例外記録数: {Exception.query.count()}")
        
        print("\n登録済みユーザー:")
        for user in User.query.all():
            print(f"  - {user.user_name} ({user.email}) - {user.company_dept_club}")
        
        print("\n登録済み科目:")
        for subject in Subject.query.all():
            print(f"  - {subject.subject_name} ({subject.attendance_time})")

if __name__ == '__main__':
    print("=== 勤怠管理システム データベース初期化 ===")
    print("新しいER図に基づいたデータベース構造で再構築します")
    
    # 確認プロンプト
    response = input("\n既存のデータはすべて削除されます。続行しますか？ (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        init_database()
        verify_database()
        
        print("\n=== 初期化完了 ===")
        print("以下の認証情報でテストできます:")
        print("ユーザー名: test_user")
        print("パスワード: password123")
        print("\nまたは")
        print("ユーザー名: student1") 
        print("パスワード: password123")
        
    else:
        print("初期化をキャンセルしました")