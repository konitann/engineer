#!/usr/bin/env python3
"""
データベースファイルとキャッシュをクリーンアップするスクリプト
"""

import os
import shutil

def cleanup_files():
    """不要なファイルを削除"""
    files_to_remove = [
        'attendance.db',
        'data/attendance.db'
    ]
    
    dirs_to_remove = [
        'data',
        '__pycache__',
        '.pytest_cache'
    ]
    
    print("🧹 クリーンアップを開始します...")
    
    # ファイルを削除
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑️  削除: {file_path}")
    
    # ディレクトリを削除
    for dir_path in dirs_to_remove:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"🗑️  削除: {dir_path}/")
    
    print("✅ クリーンアップ完了!")

if __name__ == '__main__':
    cleanup_files()