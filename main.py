from app import create_app, db
from app import migrate  # экспортируем migrate для CLI

app = create_app()

# Экспорт для flask CLI
# flask --app main db ...
# (Flask сам найдёт app, db, migrate)

if __name__ == '__main__':
    app.run(debug=True) 