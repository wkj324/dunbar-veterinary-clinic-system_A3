from src.model.animal import Animal
from src.service.animal_service import AnimalService

def test_get_animal_by_id():
    service = AnimalService()
    animal1 = Animal(1, "Mimi", "Cat", 101)
    service.add_animal(animal1)
    
    result = service.get_animal_by_id(1)
    assert result.name == "Mimi"
    assert result.species == "Cat"

def test_get_animal_not_found():
    service = AnimalService()
    result = service.get_animal_by_id(999)
    assert result is None
