from src.model.animal import Animal

class AnimalService:
    def __init__(self):
        self.animal_list = []

    def add_animal(self, animal):
        self.animal_list.append(animal)

    def get_animal_by_id(self, animal_id):
        for animal in self.animal_list:
            if animal.animal_id == animal_id:
                return animal
        return None
