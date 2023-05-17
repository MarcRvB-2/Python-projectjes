from tkinter import *
import random

# Vaste variabelen
# TODO: Deze in een optievenster door de gebruiker laten veranderen

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#1d8b37"
FOOD_COLOR = "#982020"
BACKGROUND_COLOR = "#373737"

class Snake:
    """Alle functionaliteiten over het instellen van de speler (de slang)"""

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.sqaures = []

        # Creëer de slang d.m.v. zijn lengte
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.sqaures.append(square)


class Food:
    """Alle functionaliteiten over het instellen van een voedsel object in de game"""

    def __init__(self):
        """Bepaal de willekeurige locatie van het voedsel object"""

        x = random.randint(0, GAME_WIDTH / SPACE_SIZE - 1) * SPACE_SIZE
        y = random.randint(0, GAME_HEIGHT / SPACE_SIZE - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_move(snake, food):
    """Bepaald de richting van de speler (de slang) en detecteerd als de slang het voedselobject aanraakt en 
    deze niet zichzelf of de rand van de canvas raakt"""
    
    x, y = snake.coordinates[0]

    # Controleer de richting en verander daarmee de x en y van de slang
    if direction == "Up":
        y -= SPACE_SIZE

    elif direction == "Right":
        x += SPACE_SIZE

    elif direction == "Down":
        y += SPACE_SIZE

    elif direction == "Left":
        x -= SPACE_SIZE


    # Voeg de nieuwe blok toe d.m.v. de richting en haal het laatste blokje weer weg
    snake.coordinates.insert(0, (x, y))
    sqaure = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.sqaures.insert(0, sqaure)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        # Als de slang het voedselobject aanraakt, voeg 1 scorepunt toe en zet het voedselobject weer op een andere plaats
        global score

        score += 1
        label.config(text = "Score:{}".format(score))

        canvas.delete("food")
        food = Food()

    else:
        # Indien niet, haal de laatste deel van de slang weg
        del snake.coordinates[-1]
        canvas.delete(snake.sqaures[-1])
        del snake.sqaures[-1]


    if check_collition():
        # Als de speler de canvas of zichzelf aanraakt, game over!
        gameover()

    else:
        # Voeg het resultaat toe in de UI
        gameWindow.after(SPEED, next_move, snake, food)

def change_direction(input_direction):
    """Bepaalt de richting van de speler (de slang) a.d.h.v. de gegeven input toets"""

    global direction

    if input_direction == "Left" and direction != "Right":
        direction = input_direction

    elif input_direction == "Right" and direction != "Left":
        direction = input_direction

    elif input_direction == "Up" and direction != "Down":
        direction = input_direction

    elif input_direction == "Down" and direction != "Up":
        direction = input_direction

def check_collition():
    """Controleer een aanbotsing met zichzelf of met de rand van de canvas"""

    x, y = snake.coordinates[0]

    if (x < 0 or x >= GAME_WIDTH) or (y < 0 or y > GAME_HEIGHT):
        print("GAME OVER!")
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER!")
            return True
    
    return False

def gameover():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2, 
        canvas.winfo_height() / 2,
        font = ("helvatica", 70),
        text="GAME OVER!",
        fill=FOOD_COLOR)

# Instellen UI

gameWindow = Tk()
gameWindow.title("Snake game by MarcRvB")
gameWindow.resizable(False, False)

score = 0
direction = "Down" # Standaard richting

label = Label(gameWindow, text="Score:{}".format(score), font=("helvetica", 40))
label.pack()

canvas = Canvas(gameWindow, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

gameWindow.update()

gameWindow_width = gameWindow.winfo_width()
gameWindow_height = gameWindow.winfo_height()
screen_width = gameWindow.winfo_screenmmwidth()
screen_height = gameWindow.winfo_screenheight()

x = int((screen_width / 2) - (gameWindow_width / 2))
y = int((screen_height / 2) - (gameWindow_height / 2))

gameWindow.geometry(f"{gameWindow_width}x{gameWindow_height}+{x}+{y}")

# Gameplay
## Toesten met de acties instellen

gameWindow.bind("<Left>", lambda event: change_direction("Left"))
gameWindow.bind("<Right>", lambda event: change_direction("Right"))
gameWindow.bind("<Up>", lambda event: change_direction("Up"))
gameWindow.bind("<Down>", lambda event: change_direction("Down"))

snake = Snake()
food = Food()

next_move(snake, food)

gameWindow.mainloop()