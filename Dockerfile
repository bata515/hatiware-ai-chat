# Python 3.11のslimイメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# Pythonの依存関係ファイルをコピー
COPY requirements.txt .

# Pythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY . .

# ポート5000を公開
EXPOSE 5000

# 本番環境用の環境変数設定
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Gunicornで本番用アプリケーションを起動
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]