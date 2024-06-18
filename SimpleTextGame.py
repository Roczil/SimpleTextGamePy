class GameObject:

    # Sets up an instance of GameObject with name, appearance, feel, and smell
    def __init__(self, name, appearance, feel, smell):
        self.name = name
        self.appearance = appearance
        self.feel = feel
        self.smell = smell

    # Returns string describing object appearance
    def look(self):
        return f"You look at the {self.name}. {self.appearance}\n"

    # Returns string describing object feel
    def touch(self):
        return f"You touch the {self.name}. {self.feel}\n"

    # Returns string describing object smell
    def sniff(self):
        return f"You sniff the {self.name}. {self.smell}\n"


class Room:
    # Our Room class has an escape code and a list of game objects as attributes/fields
    escape_code = 0
    game_objects = []

    # Initializer
    def __init__(self, escape_code, game_objects):
        self.escape_code = escape_code
        self.game_objects = game_objects

    # Returns whether the escape code of the room matches the code entered by the player
    def check_code(self, code):
        return self.escape_code == code

    # Returns a list with all the names of the objects we have in our room
    def get_game_object_names(self):
        names = []
        for object in self.game_objects:
            names.append(object.name)
        return names


class Game:

    def __init__(self):
        # Number of attempts the player has made on the escape code of the room
        self.attempts = 0
        objects = self.create_objects()
        # Instantiating our room object
        self.room = Room(731, objects)

    # Returns a list with all the objects we're going to have in our escape room
    def create_objects(self):
        return [
          GameObject(
            "Sweater",
            "It's a blue sweater that had the number 12 switched on it.",
            "Someone has unstitched the second number, leaving only the 1.",
            "The sweater smells of laundry detergent."),
          GameObject(
            "Chair", 
            "It's a wooden chair with only 3 legs.",
            "Someone had deliberately snapped off one of the legs.",
            "It smells like old wood."),
          GameObject(
            "Journal",
            "The final entry states that time should be hours then minutes then seconds (H-M-S).",
            "The cover is worn and several pages are missing.",
            "It smells like musty leather."),
          GameObject(
            "Bowl of soup", 
            "It appears to be tomato soup.",
            "It has cooled down to room temperature.",
            "You detect 7 different herbs and spices."),
          GameObject(
            "Clock", 
            "The hour hand is pointing towards the soup, the minute hand towards the chair, and the second hand towards the sweater.",
            "The battery compartment is open and empty.",
            "It smells of plastic."),
        ]

    # For each turn, we want to present the prompt to the player
    def take_turn(self):
        prompt = self.get_room_prompt()
        selection = input(prompt)
        if selection.isdigit():
            selection = int(selection)
       
            # Only takes the selection prompted if it's a valid input (intiger between 1 and 5)
            if selection >= 1 and selection <= 5:
                self.select_object(selection - 1)
                self.take_turn()
            
            elif len(str(selection)) != 3:
                # If the selection is not exactly 3 characters, it means the player is trying to enter a bad input
                print("Please enter a 3-digit code.")
                self.take_turn()
                
            else:
                # If we're in the else branch it means that the player is guessing a code
                is_code_correct = self.guess_code(selection)
                if is_code_correct:
                    # If the entered code is correct, the player wins
                    print("Congratulations, you win!")
                else:
                    # If they have already guessed the code incorrectly 3 times, they lose the game
                    if self.attempts == 3:
                        print("Game over, you ran out of guesses. Better luck next time!")
                    else:
                        # If the player still has attempts left, they'll take another turn
                        print(f"Incorrect, you have used {self.attempts}/3 attempts.\n")
                        self.take_turn()
        else:
         print("Please enter a valid number.")
         self.take_turn()
                    

    # Shows the option to enter the code or interact further with the objects in the room
    def get_room_prompt(self):
        prompt = "Enter the 3-digit lock code or choose an item to interact with:\n"
        names = self.room.get_game_object_names()
        index = 1
        for name in names:
            prompt += f"{index}. {name}\n"
            index += 1
        return prompt

    # Selects the object chosen by the player and prompts them for further interaction
    def select_object(self, index):
        selected_object = self.room.game_objects[index]
        prompt = self.get_object_interaction_string(selected_object.name)
        interaction = input(prompt)
        if interaction.isdigit() and 1 <= int(interaction) <= 3:
           clue = self.interact_with_object(selected_object, interaction)
           print(clue)
        else:
            print("Invalid interaction. Please enter 1, 2, or 3.")
            self.select_object(index)

    # Displays message to get type of interaction with object
    def get_object_interaction_string(self, name):
        return f"How do you want to interact with the {name}?\n1. Look\n2. Touch\n3. Smell\n"

    # Shows the interaction message to the player
    def interact_with_object(self, object, interaction):
        if interaction == "1":
            return object.look()
        elif interaction == "2":
            return object.touch()
        else:
            return object.sniff()

    # Compares the code entered to the code of the room
    def guess_code(self, code):
        if self.room.check_code(code):
            return True
        else:
            # If the codes don't match, increases attempts variable by 1
            self.attempts += 1
            return False


# Here we're creating an object of our Game class 
# and calling on its take_turn() method
game = Game()
game.take_turn()