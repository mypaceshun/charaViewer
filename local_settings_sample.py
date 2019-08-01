DEBUG = True

# collectstaticコマンドを利用したときに、
# staticファイルをデプロイする先
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')
