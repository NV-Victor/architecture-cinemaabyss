#!/bin/bash

# Ждём, пока Kong будет готов (порт 8001 — админский API)
until curl -s http://proxy-service:8001/status > /dev/null; do
  echo "Ждём, пока Kong станет доступен на :8001..."
  sleep 2
done

echo "Kong доступен. Регистрируем сервисы и маршруты..."

# 1. Создаём Upstream (назовём proxy)
curl -i -X POST http://proxy-service:8001/upstreams \
  --data name=proxy

# 2. Добавляем оба target (по 50%)

# Monolith на 8080
curl -i -X POST http://proxy-service:8001/upstreams/proxy/targets \
  --data target=monolith:8080 \
  --data weight=100

# Movies-service на 8081
curl -i -X POST http://proxy-service:8001/upstreams/proxy/targets \
  --data target=movies-service:8081 \
  --data weight=0

# 3. Создаём сервис load-balanced-service, указывающий на Upstream
curl -i -X POST http://proxy-service:8001/services \
  --data name=load-balanced-service \
  --data url=http://proxy

# 4. Привязываем маршрут на корень / и сохраняем путь
curl -i -X POST http://proxy-service:8001/services/load-balanced-service/routes \
  --data paths[]=/ \
  --data strip_path=false

echo "Конфигурация Kong завершена."