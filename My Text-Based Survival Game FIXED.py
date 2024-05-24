#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random

class Room:
    def __init__(self, name, description, items=None, enemies=None, connected_rooms=None):
        self.name = name
        self.description = description
        self.items = items if items else []
        self.enemies = enemies if enemies else []
        self.connected_rooms = connected_rooms if connected_rooms else {}

    def connect_room(self, room, direction):
        self.connected_rooms[direction] = room

    def describe(self):
        print(f"\nYou are in the {self.name}.")
        print(self.description)
        if self.items:
            print("You see the following items: " + ", ".join(self.items))
        if self.enemies:
            print("You encounter: " + ", ".join(enemy['name'] for enemy in self.enemies))
        if self.connected_rooms:
            directions = ", ".join(f"{dir} to {room.name}" for dir, room in self.connected_rooms.items())
            print(f"You can move: {directions}")

    def get_connected_rooms(self):
        return self.connected_rooms

    def take_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return item
        return None

    def remove_enemy(self, enemy_name):
        self.enemies = [enemy for enemy in self.enemies if enemy['name'] != enemy_name]


class Game:
    def __init__(self):
        self.rooms = self.create_rooms()
        self.current_room = self.rooms['basement']
        self.inventory = ["knife"]
        self.health = 100
        self.player_name = "LeBron James"
        self.enemies_defeated = 0
        self.total_enemies = sum(len(room.enemies) for room in self.rooms.values())
        self.damage_boost = 1.0

    def create_rooms(self):
        basement = Room("Basement", "A cold, damp basement with flickering lights. You can barely see around you but it smells absolutely terrible. You get the feeling you aren't alone...", [], [{"name": "zombie", "health": 30}])
        kitchen = Room("Kitchen", "A dark, cluttered kitchen with unwashed dishes. The smell of rotting food is overwhelming but upon further inspection, you don't think its food anymore... .", ["can of food"], [{"name": "mutant rat", "health": 20}])
        living_room = Room("Living Room", "A once cozy living room, now covered in nuclear. The windows are shattered and you hear the screams of either an animal or a person outside.", ["flashlight", "mysterious injection"], [])
        bedroom = Room("Bedroom", "An eerie bedroom with a broken bed dark-colored stains and the smell of fish.", ["medkit"], [])
        bathroom = Room("Bathroom", "A small bathroom with a cracked mirror and a damaged sink. It seems as if someone had their head smashed through the remains of the leaking faucet.", ["bandages"], [{"name": "infected", "health": 25}])

        basement.connect_room(kitchen, "forward")
        kitchen.connect_room(basement, "backward")
        kitchen.connect_room(living_room, "forward")
        living_room.connect_room(kitchen, "backward")
        living_room.connect_room(bedroom, "right")
        bedroom.connect_room(living_room, "left")
        bedroom.connect_room(bathroom, "forward")
        bathroom.connect_room(bedroom, "backward")

        return {
            'basement': basement,
            'kitchen': kitchen,
            'living_room': living_room,
            'bedroom': bedroom,
            'bathroom': bathroom
        }

    def play(self):
        print(f"Welcome, {self.player_name}, you have woken up from what feels like a coma. You must find a way out, defeat all the enemies, and ultimately... survive.")
        print("Commands:")
        print("  move [direction] - Move in a direction (forward, left, right, backward)")
        print("  take [item] - Take an item")
        print("  use [item] - Use an item")
        print("  fight [enemy] - Fight an enemy")
        print("  inventory - Check your inventory")
        print("  quit - Quit the game")
        while self.health > 0:
            self.current_room.describe()
            command = input("\nWhat do you want to do? (move [direction] / take [item] / use [item] / fight [enemy] / inventory / quit): ").strip().lower()
            if command.startswith("move"):
                direction = command.split(" ", 1)[1]
                self.move(direction)
            elif command.startswith("take"):
                item = command.split(" ", 1)[1]
                self.take(item)
            elif command.startswith("use"):
                item = command.split(" ", 1)[1]
                self.use(item)
            elif command.startswith("fight"):
                enemy_name = command.split(" ", 1)[1]
                self.fight(enemy_name)
            elif command == "inventory":
                self.show_inventory()
            elif command == "quit":
                print("Thanks for playing!")
                break
            else:
                print("Invalid command. Try again.")

            if self.enemies_defeated == self.total_enemies:
                self.end_game()

        if self.health <= 0:
            print("You have died. Game over.")

    def move(self, direction):
        connected_rooms = self.current_room.get_connected_rooms()
        if direction in connected_rooms:
            self.current_room = connected_rooms[direction]
            print(f"You move to the {self.current_room.name}.")
        else:
            print("You can't move in that direction.")

    def take(self, item):
        taken_item = self.current_room.take_item(item)
        if taken_item:
            self.inventory.append(taken_item)
            print(f"You took the {item}.")
        else:
            print(f"There is no {item} here.")

    def use(self, item):
        if item in self.inventory:
            if item == "mysterious injection":
                self.transform_to_michael_jordan()
            elif item == "medkit":
                self.health += 50
                print(f"You used the medkit. Your health is now {self.health}.")
            elif item == "bandages":
                self.health += 20
                print(f"You used the bandages. Your health is now {self.health}.")
            else:
                print(f"You can't use the {item} right now.")
            self.inventory.remove(item)
        else:
            print(f"You don't have {item} in your inventory.")

    def transform_to_michael_jordan(self):
        self.player_name = "Michael Jordan"
        self.health += 200
        self.damage_boost = 1.5
        print(f"You have taken the mysterious injection and transformed into {self.player_name}!")
        print(f"Your health is now {self.health} and your damage is increased by 50%.")

    def fight(self, enemy_name):
        enemy = next((enemy for enemy in self.current_room.enemies if enemy['name'] == enemy_name), None)
        if not enemy:
            print(f"There is no {enemy_name} here.")
            return

        print(f"You are fighting the {enemy_name}!")
        while enemy['health'] > 0 and self.health > 0:
            action = input("Do you want to (attack / run)? ").strip().lower()
            if action == "attack":
                damage = int(random.randint(20, 40) * self.damage_boost)
                enemy['health'] -= damage
                print(f"You hit the {enemy_name} for {damage} damage with your knife.")
                if enemy['health'] <= 0:
                    print(f"You have defeated the {enemy_name}.")
                    self.current_room.remove_enemy(enemy_name)
                    self.enemies_defeated += 1
                    break

                enemy_damage = random.randint(5, 20)
                self.health -= enemy_damage
                print(f"The {enemy_name} hits you for {enemy_damage} damage. Your health is now {self.health}.")
                if self.health <= 0:
                    print("You have been killed in battle.")
                    break
            elif action == "run":
                print("You run away from the fight.")
                break
            else:
                print("Invalid action. Try again.")

    def show_inventory(self):
        if self.inventory:
            print("You have the following items (use [item] to use them): " + ", ".join(self.inventory))
        else:
            print("Your inventory is empty.")

    def end_game(self):
        print("You have killed all the threats that have plagued your home. You finally feel the sense to leave this shell of a happy home.")
        print("You open the ruined front door of the house, only to be greeted by the barrell of a gun. Suddenly, everything turns to black.")
        print("You have died. Game over.")

if __name__ == "__main__":
    game = Game()
    game.play()


# In[ ]:





# In[ ]:




