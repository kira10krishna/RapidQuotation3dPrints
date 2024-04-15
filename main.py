import asyncio
import pymesh
import aio_pika

# Define the RabbitMQ connection parameters
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
RABBITMQ_QUEUE = "object_file_queue"

# Define the function to take input from RabbitMQ
async def take_input_from_rabbitmq():
    # Create a connection to RabbitMQ
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/",
        loop=asyncio.get_event_loop(),
    )

    # Create a queue to receive messages
    queue = await connection.declare_queue(RABBITMQ_QUEUE, auto_delete=True)

    # Define the message handler
    async def handle_message(message: aio_pika.IncomingMessage):
        # Acknowledge the message
        await message.ack()

        # Get the object file name from the message body
        object_file_name = message.body.decode()

        # Load the mesh from the object file
        mesh = pymesh.load_mesh("airboat.obj")

        # Calculate the necessary dimensions and cost
        largest_dimension = max(max(abs(vertices)) for vertices in mesh.vertices)
        divided_factor = largest_dimension / 10
        volume = mesh.volume
        area = sum(max(abs(vertices)) for vertices in mesh.faces)
        material_type = "PLA"
        filament_used = "1.75mm"
        cost = volume * 0.01 + area * 0.005

        # Output the results
        print(f"Object File Name: {object_file_name}")
        print(f"Largest Dimension: {largest_dimension}")
        print(f"Divided Factor: {divided_factor}")
        print(f"Volume: {volume}")
        print(f"Area: {area}")
        print(f"Material Type: {material_type}")
        print(f"Filament Used: {filament_used}")
        print(f"Cost: {cost}")

    # Start consuming messages
    await queue.consume(handle_message)

# Run the program
loop = asyncio.get_event_loop()
loop.run_until_complete(take_input_from_rabbitmq())
loop.run_forever()