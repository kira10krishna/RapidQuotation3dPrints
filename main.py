import asyncio
import pymesh

# Define a class to represent the 3D object
class Object3D:
    def __init__(self, file, material, filament_cost_per_unit):
        self.file = file
        self.material = material
        self.filament_cost_per_unit = filament_cost_per_unit

    async def calculate_volume(self):
        # Load the mesh using PyMesh
        mesh = pymesh.load_mesh(self.file)

        # Calculate the volume of the mesh
        volume = mesh.volume

        return volume

    async def calculate_largest_dimension(self):
        # Load the mesh using PyMesh
        mesh = pymesh.load_mesh(self.file)

        # Calculate the bounding box of the mesh
        bbox = mesh.bbox

        # Calculate the largest dimension of the bounding box
        largest_dimension = max(bbox[1] - bbox[0])

        return largest_dimension

    async def calculate_cost(self):
        volume = await self.calculate_volume()
        largest_dimension = await self.calculate_largest_dimension()

        # Calculate the cost based on the volume and largest dimension
        cost = volume * self.filament_cost_per_unit * (largest_dimension / DIVISION_FACTOR)

        return cost

# Define the division factor
DIVISION_FACTOR = 10

# Define the material and filament cost per unit
MATERIAL = "PLA"
FILAMENT_COST_PER_UNIT = 0.02

# Create an instance of the Object3D class
obj = Object3D("object_file.stl", MATERIAL, FILAMENT_COST_PER_UNIT)

# Run the calculate_cost function asynchronously
cost = asyncio.run(obj.calculate_cost())

print(f"The cost to print the object is: ${cost:.2f}")