from kafka import  KafkaProducer, KafkaConsumer,TopicPartition

class BrokerCommunication():

    def Producer(self, message):

        message_encoded = message.value.encode('utf-8')
        bootstrap_servers =['localhost:29092']
        topicName = 'core'
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        try:
            ack = producer.send(topicName, message_encoded)
            metadata = ack.get()
        except Exception as e:
            print(e)

    def Consumer(self):

        topic = 'core'
        bootstrap_servers = 'localhost:29092'
        partition = 0   
        consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
        topic_partition = TopicPartition(topic, partition)
        consumer.assign([topic_partition])
        consumer.seek_to_end(topic_partition)

        for message in consumer:
            return message.value.decode('utf-8')