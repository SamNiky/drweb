# drweb
<b>"Хранилище файлов с доступом по http"</b>

<b>Для начала:</b>

  Виртуальное окружение Python необходимо установить в директории <b>drweb/backend/</b>
  
  Установить все зависимости из requirements.txt <br>
  <code>pip install -r requirements.txt</code>
  
  Установить глобальную переменную окружения <br>
  <code>export FLASK_APP=app</code>
  
  В файле <b>drweb/backend/app/settings</b> указать параметры для подключения к БД PostgreSQL
  
  Выполнить первоночальную установку менеджера миграций <br>
  <code>flask db init</code>
  
  Выполнить миграции <br>
  <code>flask db migrate && flask db upgrade</code>
  
  <b>Запуск в режиме DEBUG:</b><br>
  <code>flask run</code> по умолчанию будет использоваться порт <b>5000</b>
  
  <b>Запуск в режиме DAEMON:</b><br>
  <code>gunicorn app:app --daemon</code> по умолчанию будет использоваться порт <b>8000</b>
  
  <b>Запуск в режиме PRODUCTION:</b><br>
  <code>gunicorn -w 4 -b 0.0.0.0:5000 app:app</code>
