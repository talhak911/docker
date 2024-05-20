#! /bin/bash

wait_for_kafka() {
  echo "Waiting for Kafka to be ready..."
  while ! nc -z broker 19092; do
    echo "$(date) - waiting for Kafka broker at broker:19092..."
    sleep 1
  done
  echo "Kafka broker is ready!"
}

# Wait for Kafka to be ready
wait_for_kafka

/opt/kafka/bin/kafka-topics.sh --create --topic order --bootstrap-server localhost:19092