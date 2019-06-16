import numpy as np


class Plant:
    def __init__(self, crop_id="None"):
        self.crop_id = crop_id

    def __repr__(self):
        return self.crop_id


class Landscape:
    def __init__(self, location="Los Angeles", size=3):
        self.location = location
        self.size = size
        self.default = [[Plant()] * self.size for _ in range(self.size)]
        self.default_array = np.array(self.default)

    def ask_size(self):
        while True:
            try:
                grid_size = int(input("input grid length and width\n"))
                if grid_size < 2:
                    print ("invalid int")
                else:
                    self.size = grid_size
            except ValueError:
                print ("invalid input")

    def make_landscape(self):
        return [[Plant()] * self.size for _ in range(self.size)]
