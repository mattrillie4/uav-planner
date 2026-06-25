import pygame

# Window settings
ROWS = 30
COLS = 40
CELL_SIZE = 20

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# initialise pygame and screen
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UAV Path Planner")

# helper function that converts pixels into indices 
def get_cell(pos):
    row = int(pos[1] / CELL_SIZE)
    col = int(pos[0] / CELL_SIZE)
    return (row, col)

# helper function updates grid sqaures
def set_cell(row, col, value):
    if 0 <= row < ROWS and 0 <= col < COLS:
        grid[row][col] = value
# create the grid to track the squares
grid = [[0] * COLS for _ in range(ROWS)]


## Tracking variables
dragging = False # tracks wether mouse is moving
start = None # keeps only one start square
end = None # keeps only one end square

# Main loop
running = True
while running:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            running = False
       
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1: # left click
                row, col = get_cell(event.pos)
                if (row, col) != start and (row, col) != end:
                    dragging = True
                    set_cell(row, col, 1) # place obstacle
            elif event.button == 2: # middle click
                row, col = get_cell(event.pos)
                if end != None:
                    set_cell(end[0], end[1], 0)
                end = (row, col)
                set_cell(row, col, 3)
            elif event.button == 3: # right click
                row, col = get_cell(event.pos)
                if start != None:
                    set_cell(start[0], start[1], 0) 
                start = (row, col)
                set_cell(row, col, 2)

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False # disable flag

        if event.type == pygame.MOUSEMOTION:
            row, col = get_cell(event.pos)
            if dragging:
                if (row, col) != start and (row, col) != end:
                    set_cell(row, col, 1) # place obstacle
    screen.fill("white")
    for col in range(0, COLS):
        for row in range(0, ROWS):
            x_pixel = col * CELL_SIZE
            y_pixel = row * CELL_SIZE
            rect = pygame.Rect(x_pixel, y_pixel, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 0:
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            elif grid[row][col] == 1:
                pygame.draw.rect(screen, (255, 0, 0), rect)
            elif grid[row][col] == 2:
                pygame.draw.rect(screen, (0, 255, 0), rect)
            elif grid[row][col] == 3:
                pygame.draw.rect(screen, (255, 255, 0), rect)



    pygame.display.flip()

pygame.quit()