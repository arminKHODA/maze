import random

def create_maze(width, height):
    maze = [['+'] * (2 * width + 1) for _ in range(2 * height + 1)]
    
    def carve_passages(cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and maze[2 * ny + 1][2 * nx + 1] == '+':
                maze[2 * cy + 1 + dy][2 * cx + 1 + dx] = ' '
                maze[2 * ny + 1][2 * nx + 1] = ' '
                carve_passages(nx, ny)
    
    carve_passages(random.randrange(width), random.randrange(height))
    
    for y in range(2 * height + 1):
        for x in range(2 * width + 1):
            if maze[y][x] == '+':
                if x % 2 == 1 and y % 2 == 1:
                    maze[y][x] = ' '
                elif x % 2 == 1 or y % 2 == 1:
                    maze[y][x] = '+'
    
    return maze

def print_maze(maze):
    for row in maze:
        print(''.join(row))

def maze_to_01(maze):
    return [[1 if cell == '+' else 0 for cell in row] for row in maze]

def format_maze_for_cpp(maze_01, width, height):
    print("const int maze[MAP_HEIGHT][MAP_WIDTH] = {")
    for row in maze_01[:height]:
        print(f"    {{{', '.join(map(str, row[:width]))}}},")
    print("};")

if __name__ == "__main__":
    MAP_WIDTH, MAP_HEIGHT = 40, 30  # Dimensions for the maze
    maze = create_maze(MAP_WIDTH // 2, MAP_HEIGHT // 2)  # Adjusted for the maze creation
    
    print("Maze:")
    print_maze(maze)
    
    maze_01 = maze_to_01(maze)
    
    # Manually set the corners to 1
    maze_01[0][0] = 1
    maze_01[0][MAP_WIDTH-1] = 1
    maze_01[MAP_HEIGHT-1][0] = 1
    maze_01[MAP_HEIGHT-1][MAP_WIDTH-1] = 1
    
    # Ensure the maze has the correct dimensions
    for row in maze_01:
        if len(row) < MAP_WIDTH:
            row.extend([0] * (MAP_WIDTH - len(row)))
        elif len(row) > MAP_WIDTH:
            del row[MAP_WIDTH:]
    
    if len(maze_01) < MAP_HEIGHT:
        maze_01.extend([[0] * MAP_WIDTH for _ in range(MAP_HEIGHT - len(maze_01))])
    elif len(maze_01) > MAP_HEIGHT:
        del maze_01[MAP_HEIGHT:]
    
    print("\nFormatted maze for C++:")
    format_maze_for_cpp(maze_01, MAP_WIDTH, MAP_HEIGHT)
