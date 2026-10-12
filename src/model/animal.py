class Animal:
    _id_counter = 1
    def __init__(self, name, species, owner_id):
        self.id = Animal._id_counter
        Animal._id_counter += 1
        self.name = name
        self.species = species
        self.owner_id = owner_id
        