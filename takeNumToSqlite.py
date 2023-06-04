import pika
import sqlite3

def calculate_avg_sales(number):
    connection = sqlite3.connect('chinook.db')
    cursor = connection.cursor()
    
    query = """ 
    SELECT AVG(tracks.UnitPrice) FROM tracks
    JOIN albums ON tracks.AlbumId = albums.AlbumId
    WHERE albums.ArtistId = ?
    """

    cursor.execute("SELECT ArtistId FROM albums WHERE ArtistId = ?", (number,))
    result = cursor.fetchone()

    if result is not None:
        artist_id = result[0]

        cursor.execute(query,(artist_id,))
        avg_sales = cursor.fetchone()[0]

        print(f"Average sales from ArtistId {artist_id}: {avg_sales}")
    else:
        print("No matching ArtistId found")

    connection.close()

def consume_from_rabbitMQ():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='numbers')

    def callback(ch, method, properties, body):
        number = int(body)

        calculate_avg_sales(number)

    channel.basic_consume(queue='numbers', on_message_callback=callback, auto_ack=True)

    print("Waiting for message")
    channel.start_consuming()

consume_from_rabbitMQ()

