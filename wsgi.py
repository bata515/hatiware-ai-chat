"""WSGI エントリーポイント - Gunicornなどの本番WSGIサーバー用"""
from app import app

if __name__ == "__main__":
    app.run()