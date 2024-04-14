import asyncio
import pymesh
from flask import Flask, request

app = Flask(__name__)

# Define the function to take input from an object file and output the cost
async def calculate_cost(object_file):
    # Load the mesh from the object file
    mesh = pymesh.load_mesh(object_file)

    # Calculate the necessary dimensions
    largest_dimension = max(max(abs(vertices)) for vertices in mesh.vertices)
    volume = mesh.volume
    area = sum(max(abs(vertices)) for vertices in mesh.faces)

    # Divide the largest dimension by a factor
    divided_factor = largest_dimension / 10

    # Define the material type and filament used
    material_type = "PLA"
    filament_used = "1.75mm"

    # Calculate the cost based on the necessary dimensions
    cost = volume * 0.01 + area * 0.005

    # Return the cost as a floating digit
    return cost

# Define the Flask API endpoint
@app.route("/calculate_cost", methods=["POST"])
def calculate_cost_api():
    # Get the object file from the request
    object_file = request.files["object_file"].read()

    # Calculate the cost asynchronously
    cost = asyncio.run(calculate_cost(object_file))

    # Return the cost as a floating digit
    return str(cost)

# Run the Flask API
if __name__ == "__main__":
    app.run()