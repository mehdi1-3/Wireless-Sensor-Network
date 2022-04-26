from kafka import KafkaConsumer
import json

if __name__ == "__main__":
    consumer = KafkaConsumer(
        "registered_user",                    #registered_user   is my topic
        bootstrap_servers='192.168.1.9:9092', #192.168.1.9  is the Address of my producer
        auto_offset_reset='earliest')
    print("starting the consumer")
    for msg in consumer:
        print("Registered User = {}".format(json.loads(msg.value)))
