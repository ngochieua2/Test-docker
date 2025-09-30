# API
- CHAT_GPTs_API_KEY: <Open AI Key>

# Kafka
- SET_UP_CLUSTER_ID: 
+ docker exec -it <Kafka_Container> /usr/bin/kafka-storage random-uuid
+ docker exec -it <Kafka_Container> /usr/bin/kafka-storage format --config /etc/kafka/kraft/server.properties --cluster-id <random-uuid>

# Startup
- docker compose up -d