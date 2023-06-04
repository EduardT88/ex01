import pika

def send_number_to_rabbitmq(number):
    # Establish a connection:
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='numbers')
    channel.basic_publish(exchange='', routing_key='numbers', body=str(number))

    print("Number sent to RabbitMQ")

    connection.close()

while True:
    try:
        number = int(input("Please insert your number: "))
        break
    except ValueError:
        print("Invalid input. Please insert an intenger")

send_number_to_rabbitmq(number)