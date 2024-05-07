import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0', port=5672))
    channel = connection.channel()
    channel.exchange_declare(
        exchange='direct_logs',
        exchange_type='direct'  # broadcasts all the messages by routing key
    )

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    # we need a fresh, empty queue, because we dont want to send historical logs
    # if queue name is "" Rabbit will generate random name.
    # exclusive=True will delete the queue after connection closes

    channel.queue_bind(exchange='logs', queue=queue_name)
    # docker exec -it rabbitmq-learn rabbitmqctl list_bindings
    # exchange                amq.gen-TMiv0_-jrzioOedebSuJzA  queue   amq.gen-TMiv0_-jrzioOedebSuJzA      []
    # logs    exchange        amq.gen-TMiv0_-jrzioOedebSuJzA  queue   amq.gen-TMiv0_-jrzioOedebSuJzA      []

    def callback(ch, method, properties, body):
        print(" [x] Modified by receiver 1 %r" % body)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    main()
