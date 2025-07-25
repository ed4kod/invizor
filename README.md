# Как запустить проект

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/ed4kod/invizor.git
   cd invizor
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   # Важно: убедитесь, что установился пакет flask-migrate
   ```

4. Инициализируйте и создайте базу данных:
   ```bash
   flask db init         # только при первом запуске
   flask db migrate -m "init"
   flask db upgrade
   ```

5. Запустите сервер:
   ```bash
   python main.py
   ```

Откройте http://127.0.0.1:5000 в браузере.