"""
Abstract Factory pattern serves to provide an interface for creating
related / dependent objects without need to specify their actual class.


Idea: Abstract the creation of objects depending on the business logic, platform choice etc.
Classes are first class objects in python
TLDR - Provide a way to encapsulate a group of individual factories

"""

import random
from typing import Type

class Pet:
    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> None:
        """ This is the equivalent of virtual function"""
        raise NotImplementedError

    def __str__(self) -> str:
        """ This is the equivalent of virtual function - Magic Method"""
        raise NotImplementedError

class Dog(Pet):
    """ Dog publicly inherits Pet"""
    def speak(self) -> None:
        print("Wooof")

    def __str__(self) -> str:
        return f"Dog<{self.name}>"

class Cat(Pet):
    def speak(self) -> None:
        print("Meow")

    def __str__(self) -> None:
        return f"Cat<{self.name}>"

""" So above we have 2 abstractions """

# Factory #1
class PetShop:
    def __init__(self, animal_factory: Type[Pet]) -> None:
        self.pet_factory = animal_factory

    def buy_pet(self, name:str) -> Pet:
        pet = self.pet_factory(name)
        print(f"Here us your lovely {pet}")
        return pet


# Factory #2
def random_animal(name: str):
    return random.choice([Dog, Cat])(name)

def main():
    cat_shop = PetShop(Cat)
    pet = cat_shop.buy_pet("Hulk")
    pet.speak()

    # Generating random animals
    shop = PetShop(random_animal)
    for name in ["Max", "Jack", "Buddy"]:
        pet = shop.buy_pet(name)
        pet.speak()
        print("="*20)

if __name__ == '__main__':
    random.seed(1234567)
    main()