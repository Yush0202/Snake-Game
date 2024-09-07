import tkinter #GUI INTERFACE
import random #FOR PLACING FOOD RANDOMLY
import os

ROWS =25
COLS =25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y): #take in x and y position
        self.x =x
        self.y =y

#game window
window = tkinter.Tk() #open a window
window.title("Snake")
window.resizable(False,False)

canvas = tkinter.Canvas(window, bg ="Black",width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0) #edit widnow canvas
canvas.pack()
window.update() #add the canvas to the window

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width =window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#calculate x and y poitions for window
window_x = int((screen_width/2)-(window_width/2))
window_y = int((screen_height/2)-(window_height/2))                    

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}") #inputs as widthxheight+x+y as string


#initialize game
snake = Tile(5*TILE_SIZE,5*TILE_SIZE) #single tile,initial position
food = Tile(10*TILE_SIZE,10*TILE_SIZE) #initial food position 
snake_body = []  #grow snake body when eats food (multi tile objects)
velocityX = 0
velocityY = 0
game_over = False
score = 0
highscore =0

# Load the high score
with open("high_score.txt", "r") as file:
    try:
        high_score = int(file.read())
    except ValueError:
        high_score = 0

# Load the high score
with open("high_score.txt", "r") as file:
    try:
        high_score = int(file.read())
    except ValueError:
        high_score = 0

#keybind and velocity
def change_direction(e) : #e = event
    #print(e) whole event
    #print(e.keysym) #key symbol
    global velocityX, velocityY, game_over

    if(e.keysym == "space" and game_over):
        reset_game()
        return

    elif (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0
    

# move snake
def move():
    global snake, food, snake_body, game_over, score ,high_score

    #game over
    if(game_over):
        return 
    
    if(snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):  #crossed the boundary
        game_over = True
        update_high_score()
        return
    
    for tile in snake_body:
        if(snake.x == tile.x and snake.y == tile.y):
            game_over = True
            update_high_score()
            return

    #collision
    if (snake.x == food.x and snake.y == food.y): #snake head and food pos same
        snake_body.append(Tile(food.x,food.y))  #grow snake body by 1 tile
        food.x = random.randint(0,COLS-1) * TILE_SIZE
        food.y = random.randint(0,ROWS-1) * TILE_SIZE
        score += 1
    
    #update snake body
    for i in range(len(snake_body)-1,-1,-1):
        tile =snake_body[i]
        if (i == 0): 
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y



    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE




#draw shapes
def draw():
    global snake, food, snake_body, game_over, score ,high_score

    move() # snake moves at a pace of 10fps

    canvas.delete("all") # everytime new frame created old frame deleted
    
    #object drawn first appears first
    #draw food
    canvas.create_rectangle(food.x,food.y,food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "Red")
    
    #draw snake
    canvas.create_rectangle(snake.x,snake.y,snake.x + TILE_SIZE, snake.y + TILE_SIZE ,fill= "Lime")

    #draw snake after food eaten
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill ="Lime")

    if(game_over):
        canvas.create_text(250, 200, font = "Arial 20", text = "Game Over!", fill="Yellow")  
        canvas.create_text(250,300,font="Arial 10", text=f"Score: {score}" , fill = "Lime" )
        canvas.create_text(250,350,font="Arial 10",text="Press Space to Restart",fill="Red")
        canvas.create_text(250, 400, font="Arial 20", text=f"High Score: {high_score}", fill="White")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text = f"Score: {score}", fill = "White")
    
    window.after(100,draw) #calling draw every 100ms, 10fps

#update high score
def update_high_score():
    global score, high_score

    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))

#reset game
def reset_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score

    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0 

draw()

window.bind("<KeyRelease>", change_direction) #key listener to change direction
window.mainloop() #keep window on

