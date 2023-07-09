exec pip install django gunicorn uvicorn psycopg2-binary channels django-extensions

FILE_PATH="./db.sqlite3"

if [[ ! -f $FILE_PATH ]]; then
    echo "DB does not exist. Creating one..."
    exec sqlite3 db.sqlite3
else
    echo "DB exists."
fi