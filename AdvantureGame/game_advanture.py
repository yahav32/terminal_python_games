import random
from abc import ABC

# ABC - Abstract Base Class
class Entity(ABC):
    def __init__(self, name: str, health: int, power: int):
        self.name = name
        self.max_health = health
        self.health = health
        self.power = power

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        return damage

    def attack(self):
        return random.randint(self.power // 2, self.power)

class Player(Entity):
    def __init__(self, name: str, max_health: int = 100, power: int = 10, inventory: list = []):
        super().__init__(name, max_health, power)
        self.inventory = inventory

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def show_stats(self):
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Power: {self.power}")
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}")
        print("---------------------------\n")

class Monster(Entity):
    def __init__(self, name: str, health: int, power: int):
        super().__init__(name, health, power)

class Game:
    def __init__(self):
        self.player = None
        self.game_over = False

    def start(self):
        print("Welcome to the Great Adventure!")
        name = input("What is your hero's name? ")
        self.player = Player(name)
        print(f"Hello {name}, your journey begins now...")
        self.play()

    def combat(self, monster):
        print(f"\nA {monster.name} has appeared!")
        while monster.is_alive() and self.player.is_alive():
            print(f"\n{monster.name}: {monster.health} HP | {self.player.name}: {self.player.health} HP")
            action = input("What do you want to do? (attack/run): ").strip().lower()
            
            if action == "attack":
                damage = self.player.attack()
                monster.take_damage(damage)
                print(f"You hit the {monster.name} and dealt {damage} damage!")
                
                if monster.is_alive():
                    m_damage = monster.attack()
                    self.player.take_damage(m_damage)
                    print(f"The {monster.name} attacked back and dealt {m_damage} damage!")
            elif action == "run":
                if random.random() < 0.5:
                    print("You managed to escape!")
                    return False
                else:
                    print("You failed to escape!")
                    m_damage = monster.attack()
                    self.player.take_damage(m_damage)
                    print(f"The {monster.name} hit you while you tried to run and dealt {m_damage} damage!")
            else:
                print("Invalid action!")

        if not self.player.is_alive():
            print(f"\n{self.player.name} was defeated in battle... Game Over.")
            self.game_over = True
            return False
        else:
            print(f"You defeated the {monster.name}!")
            return True

    def play(self):
        print("\nYou are in a dark room. There is a door in front of you and a chest on the side.")
        choice = input("What do you want to do? (open door/check chest): ").strip().lower()
        
        if "chest" in choice:
            print("You found a health potion and a rusty sword!")
            self.player.inventory.append("Health Potion")
            self.player.inventory.append("Rusty Sword")
            self.player.power += 5
            print("Your power increased by 5!")
        
        print("\nYou open the door and move into the hallway...")
        
        goblin = Monster("Goblin", 30, 8)
        if self.combat(goblin):
            if self.game_over: return
            
            self.player.show_stats()
            print("\nYou continued down the hallway and found a large golden door.")
            choice = input("Do you want to open it? (yes/no): ").strip().lower()
            
            if choice == "yes":
                dragon = Monster("Small Dragon", 60, 15)
                if self.combat(dragon):
                    print("\nCongratulations! You found the treasure and won the game!")
            else:
                print("\nYou were too afraid and decided to go home. Game Over.")
        
        print("\nThanks for playing!")

if __name__ == "__main__":
    game = Game()
    game.start()