from kafka import KafkaConsumer

# 从Kafka消费数据
consumer = KafkaConsumer('student_topic', bootstrap_servers='localhost:9092')
for message in consumer:
    print("从Kafka获取到的数据:")
    print("-" * 30)
    print(message.value.decode('utf-8'))
    print("-" * 30)