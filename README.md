# Приложение Flask для Статистики VK

Это веб-приложение на Python Flask, которое извлекает информацию о лайках и комментариях из указанной группы ВКонтакте (VK, популярной российской социальной сети), высчитывает очки каждого пользователя (на основе лайков и комментариев) и представляет данные в форме сортируемой, поисковой таблицы.

## Особенности

- Подключается к API VK для извлечения лайков и комментариев из группы VK
- Вычисляет очки для пользователей на основе лайков и комментариев
- Параллельно обрабатывает сообщения с помощью ThreadPoolExecutor для более быстрой работы
- Предоставляет веб-интерфейс Flask для просмотра и поиска данных
- Автоматически обновляет статистику каждые 15 секунд (настраиваемо)
- Сохраняет извлеченные данные в виде файла CSV

## Начало работы

Эти инструкции помогут вам получить копию проекта и запустить его на вашем локальном компьютере для разработки и тестирования.

### Предварительные требования

- Python 3.x
- Flask
- Аккаунт VK для доступа к API VK

### Установка

```bash
git clone https://github.com/cotafei/vk-statistics-flask-app.git
cd vk-statistics-flask-app
pip install -r requirements.txt
```

### Конфигурация

Вам потребуется установить токен API VK и id группы, из которой вы хотите собирать данные:

```python
TOKEN = '' # Токен API VK
GROUP_ID =  # ID группы VK
```

Вы также можете настроить значение очков за лайки и комментарии, а также интервал обновления статистики:

```python
LIKES_VALUE = 5 # очки за лайк
COMMENTS_VALUE = 10 # очки за комментарий
UPDATE_INTERVAL = 15 # интервал обновления в секундах
```

### Запуск приложения

Запустите сервер Flask:

```bash
python app.py
```

По умолчанию приложение будет запущено на

- '0.0.0.0:5000'

## Лицензия

Данный проект лицензирован в соответствии с лицензией Apache, версия 2.0. Подробности смотрите в файле [LICENSE](LICENSE).
