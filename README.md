# forest-monitoring-app-by-Andrey-Petrov
Back-end приложение на Python, отвечающее за хранения и обработку данных мониторинга лесных пожаров

**Примеры использования API**
1. Создание алерта с изображениями
curl -X POST http://localhost:5000/api/alerts \
  -F "fire_detected=true" \
  -F "comment=Обнаружен дым на координатах 55.7558° N, 37.6173° E" \
  -F "images=@photo1.png" \
  -F "images=@photo2.png"

2. Получение алертов за 48 часов
curl http://localhost:5000/api/alerts?hours=48

Пример ответа:
[{"comment":"\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u043e \u0432\u043e\u0437\u0433\u043e\u0440\u0430\u043d\u0438\u0435 \u043d\u0430 \u043a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430\u0445 55.7558\u00b0 N, 37.6173\u00b0 E","fire_detected":true,"id":5,"images":[{"id":"cb249afe-4214-4e76-8b61-55fac97addce"},{"id":"b6b6a742-c20d-450f-86d6-c2e3ad257140"},{"id":"0c24cf65-d814-447b-a7b1-c0bb5b81255e"}],"images_count":3,"timestamp":"2026-01-25T16:49:16.503847"},{"comment":"\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u043e \u0432\u043e\u0437\u0433\u043e\u0440\u0430\u043d\u0438\u0435 \u043d\u0430 \u043a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430\u0445 55.7558\u00b0 N, 37.6173\u00b0 E","fire_detected":true,"id":4,"images":[{"id":"9ef1f2b8-2210-4b47-af38-796538124bf0"},{"id":"11064079-7c8b-49fa-836f-4a0406eece7e"},{"id":"100033dd-9b5e-40fa-8a71-d8b41337b5c9"}],"images_count":3,"timestamp":"2026-01-25T16:48:43.883536"},{"comment":"\u041f\u043e\u043b\u0451\u0442 \u0437\u0430\u0432\u0435\u0440\u0448\u0451\u043d, \u043f\u0440\u0438\u0437\u043d\u0430\u043a\u043e\u0432 \u0432\u043e\u0437\u0433\u043e\u0440\u0430\u043d\u0438\u044f \u043d\u0435 \u043e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u043e","fire_detected":false,"id":3,"images":[],"images_count":0,"timestamp":"2026-01-25T16:44:48.035868"},{"comment":"\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d \u0434\u044b\u043c \u043d\u0430 \u043a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430\u0445 55.7558\u00b0 N, 37.6173\u00b0 E","fire_detected":true,"id":2,"images":[{"id":"824f07b9-0100-44c1-9136-99fc4504873b"},{"id":"37f5fd0c-f3ce-47df-99f1-b90c9288b1c0"}],"images_count":2,"timestamp":"2026-01-24T17:25:56.676189"}]

3. Скачивание изображения
curl -o <file_id>.png http://localhost:5000/api/images/<file_id>

Хранилище данных
pgdata volume: Все данные PostgreSQL сохраняются в /var/lib/docker/volumes/pgdata/_data
uploads volume: Все изображения сохраняются в /var/lib/docker/volumes/uploads/_data
