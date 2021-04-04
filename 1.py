class SpaceObject:
    def __init__(self, name=None):
        self.name = name or 'X'
    
class Planet(SpaceObject):
    def __init__(self, name=None, population=None):
        super().__init__(name)
        self.population = population or []
        
    def populate(self, animal):
        self.population.append(animal)
        return self.population
    
    def __str__(self):
        total_num = len(self.population)
        result = f"There are {total_num} animals living on planet {self.name}. \n\n"
        
        for i in range(total_num):
            curr_animal = self.population[i]
            name = curr_animal.name
            kind = curr_animal.__class__.__name__.lower()
            colour = curr_animal.colour
            age = curr_animal.age
            height = curr_animal.height
            mood = curr_animal.mood
            shape = curr_animal.shape
            
            line = f"""{name} is a {kind}, he's {colour} and he's {age}. He's rather {height}{mood}{shape}.\n"""
            result = result + line
        return result
        
class Animal:
    def __init__(self, colour, name=None, age=None):
        self.colour = colour
        self.name = name or "Anonymous"
        self.age = age or 'not willing to share his age with us'
        
    def __getattr__(self, item):
        return ""
        
class Chinchilla(Animal):    
    def __init__(self, shape, colour, name=None, age=None):
        super().__init__(colour, name, age)
        self.shape = shape
        
    def eat_a_cake(self):
        return f"{self.name} is very fond of cakes, thank you for bringing one!"
            
class Kangaroo(Animal):    
    def __init__(self, height, colour, name=None, age=None):
        super().__init__(colour, name, age)
        self.height = height
        
    def jump(self, num):
        assert isinstance(num, int)
        return f"{self.name} loves jumping! And now he'll jump {num} times for you!"
        
class Llama(Animal):    
    def __init__(self, mood, colour, name=None, age=None):
        super().__init__(colour, name, age)
        self.mood = mood
        
    def are_you_alright(self):
        return f"Yeah, {self.name} is alright, he's just a bit {self.mood} today."
    
def main():    
    bobby = Chinchilla('fat','grey', 'Bobby', '9')
    larry = Kangaroo('tall','pink', 'Larry')
    perry = Llama('gloomy', 'white', 'Perry', '7')
    earth = Planet('Earth')
    
    earth.populate(bobby)
    earth.populate(larry)
    earth.populate(perry)
    print(earth)
    
if __name__ == "__main__":
    main()
