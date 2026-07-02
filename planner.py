import pygame
import heapq

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

# define heuristic function for algorithm
## estimates distance between start and end points
def heuristic(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


# A* algorithm function
def astar(start, end):
    #initialise everything
    directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    came_from = {} # store previous locations
    g_score = {}
    heap = []
    f = heuristic(start, end) # calculate first f value

    g_score[start] = 0
    heapq.heappush(heap, (f, start))

    while heap:
        current_f, current_cell = heapq.heappop(heap)
        if current_cell == end:
            ## trace back
            current = end
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
                
        else: 
            #calculate neighbour cell
            for dr, dc in directions:
                neighbour = (current_cell[0] + dr, current_cell[1] + dc)
                if 0 <= neighbour[0] < ROWS and 0 <= neighbour[1] < COLS:
                    if grid[neighbour[0]][neighbour[1]] == 1:
                        continue
                    tentative_g = g_score[current_cell] + 1
                    if tentative_g < g_score.get(neighbour, float('inf')):
                        came_from[neighbour] = current_cell
                        g_score[neighbour] = tentative_g
                        new_f = tentative_g + heuristic(neighbour, end)
                        heapq.heappush(heap, (new_f, neighbour))
    
    return None

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
end = None # kee    ps only one end square
mode = "end" # mode for drawing start or end squares
path = [] # holds the path found on grid by astar

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
            elif event.button == 3: # right click
                row, col = get_cell(event.pos)
                if mode == "start":
                    if start != None:
                        set_cell(start[0], start[1], 0) 
                    start = (row, col)
                    set_cell(row, col, 2) # draw start square
                elif mode == "end":
                    if end != None:
                        set_cell(end[0], end[1], 0)
                    end = (row, col)
                    set_cell(row, col, 3) # draw end square

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False # disable flag

        if event.type == pygame.MOUSEMOTION:
            row, col = get_cell(event.pos)
            if dragging:
                if (row, col) != start and (row, col) != end:
                    set_cell(row, col, 1) # place obstacle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start and end:
                    result = astar(start, end)
                    if result:
                        path = result
            if event.key == pygame.K_e:
                mode = "end"
            if event.key == pygame.K_s:
                mode = "start"
    screen.fill("white")
    for col in range(0, COLS):
        for row in range(0, ROWS):
            x_pixel = col * CELL_SIZE
            y_pixel = row * CELL_SIZE
            rect = pygame.Rect(x_pixel, y_pixel, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 0:
                if (row, col) in path:
                    pygame.draw.rect(screen, ("blue"), rect)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
            elif grid[row][col] == 1:
                pygame.draw.rect(screen, (255, 0, 0), rect)
            elif grid[row][col] == 2:
                pygame.draw.rect(screen, (0, 255, 0), rect)
            elif grid[row][col] == 3:
                pygame.draw.rect(screen, (255, 255, 0), rect)



    pygame.display.flip()

pygame.quit()