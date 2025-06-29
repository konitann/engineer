## 🚀 機能

- **ユーザー管理**: アカウント登録・ログイン
- **科目管理**: 科目の追加・削# 勤怠管理システム

Flask + Svelte + SQLite + SQLAlchemy を使用したシンプルな勤怠管理システムです。

## 🚀 機能

- **ユーザー管理**: アカウント登録・ログイン
- **科目管理**: 科目の追加・削除・管理
- **出勤記録**: 科目別の出勤・欠勤・遅刻・早退記録
- **例外記録**: 特別な事情の記録管理
- **履歴表示**: 出勤履歴・例外履歴の表示
- **QRコード生成**: 日付とユーザー名のQRコード生成
- **レスポンシブUI**: モバイル対応

## 📊 データベース構造

- **User**: ユーザー情報（ID、名前、メール、所属など）
- **Subject**: 科目情報（ID、科目名、授業時間、説明）
- **Attendance**: 出勤記録（ユーザー、科目、日付、状況）
- **ExceptionRecord**: 例外記録（ユーザー、日付、理由、備考）

## 🛠️ セットアップ

### Docker を使用する場合（推奨）

```bash
# リポジトリをクローン
git clone https://github.com/konitann/engineer.git
cd engineer

# Docker Compose でアプリケーションを起動
docker-compose up --build

# データベースを初期化（別ターミナルで）
docker-compose exec backend python init_db.py
```

### ローカル環境で実行する場合

#### バックエンド (Flask)

```bash
cd backend

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 基本依存関係をインストール
pip install Flask Flask-SQLAlchemy Flask-CORS Flask-JWT-Extended bcrypt qrcode Pillow

# データベースを初期化
python init_db.py

# サーバーを起動
python app.py
```

サーバーは http://localhost:5000 で起動します。

#### フロントエンド (Svelte)

```bash
cd frontend

# 依存関係をインストール
npm install

# 開発サーバーを起動
npm run dev
```

フロントエンドは http://localhost:3000 で起動します。

## 🔑 テストアカウント

- **ユーザー名**: `test_user`
- **パスワード**: `password123`

または

- **ユーザー名**: `student1`
- **パスワード**: `password123`

## 💻 使用方法

1. ブラウザで http://localhost:3000 にアクセス
2. 新規登録でアカウントを作成するか、テストアカウントでログイン
3. ログイン後、以下の機能が利用可能：
   - **データベース初期化**: 新しい構造でDBを再作成
   - **科目管理**: 科目の追加・削除・表示
   - **出勤記録**: 日付・科目・状況を選択して記録
   - **例外記録**: 特別な事情がある日の記録
   - **QRコード生成**: 日付を選択してQRコードを生成
   - **履歴表示**: 過去の記録を確認

## 📂 エクセルインポート機能

### ファイル形式
- 対応フォーマット: `.xlsx`, `.xls`
- 必要なシート: `Sheet1`（基本情報）, `Sheet2`（出勤スケジュール）

### Sheet1の構造
```
氏名       | 青木　立            | 曜日・時限    | 火曜日 1〜2 限
所属       | ものづくり工学科    | 開講期間・クラス | 前期 606162637...
授業科目   | ディジタル制御システム | 授業時間     | 08:40〜10:10
```

### Sheet2の構造
```
区分 | 出講日  | 印 | 出勤時刻 | 退勤時刻 | 時間数 | 備考
     | 4月8日  |    | 時　分   | 時　分   | 2     |
     | 4月15日 |    | 時　分   | 時　分   | 2     |
```

### 使用手順
1. 📁 **エクセルファイルを選択**
2. 📊 **インポート実行**をクリック
3. または📄 **テンプレートダウンロード**でサンプル取得

## 🌐 API エンドポイント

### 認証
- `POST /api/register` - ユーザー登録
- `POST /api/login` - ログイン
- `GET /api/profile` - ユーザー情報取得

### 科目管理
- `GET /api/subjects` - 科目一覧取得
- `POST /api/subjects` - 科目追加
- `DELETE /api/subjects/<id>` - 科目削除

### 出勤記録
- `POST /api/attendance` - 出勤記録追加
- `GET /api/attendance` - 出勤履歴取得

### 例外記録
- `POST /api/exceptions` - 例外記録追加
- `GET /api/exceptions` - 例外履歴取得

### その他
- `POST /api/generate-qr` - QRコード生成
- `POST /api/init-db` - データベース初期化
- `GET /api/health` - ヘルスチェック

## 🗃️ データベース

SQLiteを使用し、以下のテーブルが自動作成されます：

- `user` (ユーザー情報)
- `subject` (科目情報)
- `attendance` (出勤記録)
- `exception` (例外記録)

データベースファイルは `backend/attendance.db` に保存されます。

## 🐳 Docker構成

- **backend**: Flask API サーバー
- **frontend**: Svelte 開発サーバー
- **volumes**: SQLiteデータの永続化

## 📦 依存関係

### バックエンド（必須）
- Flask==2.3.3
- Flask-SQLAlchemy==3.0.5
- Flask-CORS==4.0.0
- Flask-JWT-Extended==4.5.3
- qrcode==7.4.2
- Pillow==10.0.1
- bcrypt==4.0.1

### フロントエンド
- Svelte 4.0.5
- Vite 4.4.5

## 🔧 開発

### 新機能の追加

1. バックエンド: `backend/app.py` にAPIエンドポイントを追加
2. フロントエンド: `frontend/src/components/` にコンポーネントを追加
3. データベース: モデルを追加し、`init_db.py` でマイグレーション

### デバッグ

```bash
# バックエンドのログ確認
python app.py

# フロントエンドのビルド
cd frontend
npm run build

# クリーンアップ
cd backend
python cleanup.py
```

## 🆔 バージョン情報

- **Version**: 2.0.0
- **Last Updated**: 2025年1月
- **Python**: 3.10+
- **Node.js**: 18+

## 📄 ライセンス

MIT License

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📞 サポート

質問や問題がある場合は、Issuesを作成してください。

---

**注意**: このシステムはシンプルで使いやすい勤怠管理を目的としており、基本的な依存関係のみで動作します。