from src.service.animal_service import AnimalService
from src.model.animal import Animal

def test_get_animal_by_id():
    service = AnimalService()
    animal1 = Animal("Mimi", "Cat", 101)
    service.add_animal(animal1)
    res = service.get_animal_by_id(animal1.id)
    assert res is not None
    assert res.name == "Mimi"