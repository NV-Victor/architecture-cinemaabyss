from flask import Flask, request, jsonify
from confluent_kafka import Producer, Consumer
from datetime import datetime
import socket
import json
import random
import os
import time
import logging


app = Flask(__name__)

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Чтение переменных окружения
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'kafka:9092')
PORT = int(os.environ.get('PORT', 8082)) 

producer = Producer({
    'bootstrap.servers': KAFKA_BROKER,
    'client.id': socket.gethostname()
})

@app.route('/api/events/health', methods=['GET'])
def health_check():
    return jsonify({"status": True}), 200

@app.route('/api/events/movie', methods=['POST'])
def send_movie_event():
    user_data = request.get_json(force=True) or {}

    movie_id = random.randint(100000, 999999)
    user_id = random.randint(100000, 999999)

    message = {
        "movie_id": movie_id,
        "title": user_data.get("title", "Test Movie Event"),
        "action": user_data.get("action", "viewed"),
        "user_id": user_id
    }

    try:
        producer.produce(
            topic='movie-events',
            key='movie-key',
            value=json.dumps(message)
        )
        producer.flush()

        # Инициализация Kafka consumer
        consumer = Consumer({
            'bootstrap.servers': KAFKA_BROKER,
            'group.id': f'health-check-{random.randint(1000, 9999)}',
            'auto.offset.reset': 'earliest'
        })

        consumer.subscribe(['movie-events'])
        time.sleep(3.0)
        msg = consumer.poll(3.0)

        if msg and not msg.error():
            try:
                event = json.loads(msg.value().decode('utf-8'))
                topic = msg.topic()
                partition = msg.partition()
                offset = msg.offset()
                logging.info(f"[Kafka Log] Read from topic '{topic}' [partition {partition}, offset {offset}]: {event}")
            except Exception as e:
                logging.error(f"[Kafka Log] Error decoding message: {e}")
        else:
            logging.warning("[Kafka Log] No message received or consumer error.")

        consumer.close()


        return jsonify({"status": "success", "event": message}), 201
    except Exception as e:
        return jsonify({"status": "Error", "details": str(e)}), 500

   
@app.route('/api/events/user', methods=['POST'])
def send_user_event():
    user_data = request.get_json(force=True) or {}

    user_id = random.randint(100000, 999999)

    message = {
        "user_id": user_id,
        "username": user_data.get("username", "testuser"),
        "action": user_data.get("action", "logged_in"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        producer.produce(
            topic='user-events',
            key='user-key',
            value=json.dumps(message)
        )
        producer.flush()

        # Инициализация Kafka consumer
        consumer = Consumer({
            'bootstrap.servers': KAFKA_BROKER,
            'group.id': f'health-check-{random.randint(1000, 9999)}',
            'auto.offset.reset': 'earliest'
        })

        consumer.subscribe(['user-events'])
        time.sleep(3.0)
        msg = consumer.poll(3.0)

        if msg and not msg.error():
            try:
                event = json.loads(msg.value().decode('utf-8'))
                topic = msg.topic()
                partition = msg.partition()
                offset = msg.offset()
                logging.info(f"[Kafka Log] Read from topic '{topic}' [partition {partition}, offset {offset}]: {event}")
            except Exception as e:
                logging.error(f"[Kafka Log] Error decoding message: {e}")
        else:
            logging.warning("[Kafka Log] No message received or consumer error.")

        consumer.close()


        return jsonify({"status": "success", "event": message}), 201
    except Exception as e:
        return jsonify({"status": "Error", "details": str(e)}), 500


@app.route('/api/events/payment', methods=['POST'])
def send_payment_event():
    user_data = request.get_json(force=True) or {}

    user_id = random.randint(100000, 999999)
    payment_id = random.randint(100000, 999999)

    message = {

        "payment_id": payment_id,
        "user_id": user_id,
        "amount": user_data.get("amount", 9.99),
        "status": user_data.get("status", "completed"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "method_type": user_data.get("method_type", "credit_card")
    }

    try:
        producer.produce(
            topic='payment-events',
            key='payment-key',
            value=json.dumps(message)
        )
        producer.flush()

        # Инициализация Kafka consumer
        consumer = Consumer({
            'bootstrap.servers': KAFKA_BROKER,
            'group.id': f'health-check-{random.randint(1000, 9999)}',
            'auto.offset.reset': 'earliest'
        })

        consumer.subscribe(['payment-events'])
        time.sleep(3.0)
        msg = consumer.poll(3.0)

        if msg and not msg.error():
            try:
                event = json.loads(msg.value().decode('utf-8'))
                topic = msg.topic()
                partition = msg.partition()
                offset = msg.offset()
                logging.info(f"[Kafka Log] Read from topic '{topic}' [partition {partition}, offset {offset}]: {event}")
            except Exception as e:
                logging.error(f"[Kafka Log] Error decoding message: {e}")
        else:
            logging.warning("[Kafka Log] No message received or consumer error.")

        consumer.close()


        return jsonify({"status": "success", "event": message}), 201
    except Exception as e:
        return jsonify({"status": "Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)