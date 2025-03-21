import pygame
from random import sample
from selection import SelectNumber
from copy import deepcopy

def create_line_coord(cell_size: int) -> list[list[tuple]]:
    points = []
    for y in range(1, 9):
        temp = [(0, y * cell_size), (630, y * cell_size)]
        points.append(temp)

    for x in range(1, 10):
        temp = [(x * cell_size, 0), (x * cell_size, 630)]
        points.append(temp)

    return points

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

def pattern(row_num: int, col_num: int) -> int:
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE

def shuffle(samp: range) -> list:
    return sample(samp, len(samp))

def create_grid(sub_grid: int) -> list[list[int]]:
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]

def remove_num(grid: list[list[int]], difficulty: int) -> None:
    num_of_cells = GRID_SIZE * GRID_SIZE
    empties = num_of_cells * difficulty // 5  
    for i in sample(range(num_of_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0

class Grid:
    def __init__(self, pygame, font, difficulty):
        self.cell_size = 70
        self.num_x_off = 25
        self.num_y_off = 12
        self.line_coordinates = create_line_coord(self.cell_size)

        self.grid = create_grid(SUB_GRID_SIZE)
        self.__test_grid = deepcopy(self.grid)
        self.win = False

        remove_num(self.grid, difficulty)
        self.occupied_cell_coord = self.pre_occupied()
        
        self.game_font = font
        self.selection = SelectNumber(pygame, self.game_font)

        self.previous_states = []
        self.initial_state = deepcopy(self.grid)

        self.undo_button = pygame.Rect(650, 500, 100, 50)
        self.reset_button = pygame.Rect(650, 570, 100, 50)

    def save_state(self):
        self.previous_states.append(deepcopy(self.grid))

    def undo_move(self):
        if self.previous_states:
            self.grid = self.previous_states.pop()

    def reset_game(self):
        self.grid = deepcopy(self.initial_state)
        self.previous_states.clear()

    def check_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != self.__test_grid[y][x]:
                    return False
        return True

    def is_cell_preocc(self, x: int, y: int) -> bool:
        return (y, x) in self.occupied_cell_coord

    def get_mouse_click(self, x: int, y: int) -> str:
        result = None
        if self.undo_button.collidepoint(x, y):
            self.undo_move()
        elif self.reset_button.collidepoint(x, y):
            self.reset_game()
            result = "reset" 
        elif x <= 630:
            grid_x, grid_y = x // self.cell_size, y // self.cell_size
            if not self.is_cell_preocc(grid_x, grid_y):
                selected_num = self.selection.selected_number
                if selected_num != 0:
                    self.save_state()
                    self.set_cell(grid_x, grid_y, selected_num)
                    if self.__test_grid[grid_y][grid_x] != selected_num:
                        result = "incorrect"
        
        self.selection.button_clicked(x, y, self.grid)
        
        if self.check_grid():
            self.win = True
            
        return result 


    def pre_occupied(self) -> list[tuple]:
        return [(y, x) for y in range(len(self.grid)) for x in range(len(self.grid[y])) if self.get_cell(x, y) != 0]

    def __draw_numbers(self, surface) -> None:
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell(x, y) != 0:
                    color = (0, 200, 255) if (y, x) in self.occupied_cell_coord else (0, 255, 0)
                    if self.get_cell(x, y) != self.__test_grid[y][x]:
                        color = (255, 0, 0)

                    text_surf = self.game_font.render(str(self.get_cell(x, y)), False, color)
                    surface.blit(text_surf, (x * self.cell_size + self.num_x_off, y * self.cell_size + self.num_y_off))

    def get_cell(self, x: int, y: int) -> int:
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> None:
        self.grid[y][x] = value

    def __draw_lines(self, pg, surface) -> None:
        for index, point in enumerate(self.line_coordinates):
            color = (255, 200, 0) if index in {2, 5, 10, 13} else (0, 50, 0)
            pg.draw.line(surface, color, point[0], point[1])

    def draw_buttons(self, surface):
        button_width, button_height = 120, 40  
        button_x = 710 
        undo_y, reset_y = 500, 550

        mouse_x, mouse_y = pygame.mouse.get_pos()

        small_font = pygame.font.Font(None, 30)  

        undo_hovered = self.undo_button.collidepoint(mouse_x, mouse_y)
        undo_color = (255, 255, 255) if undo_hovered else (0, 0, 0)  
        undo_text_color = (0, 0, 0) if undo_hovered else (255, 255, 255) 

        self.undo_button = pygame.Rect(button_x, undo_y, button_width, button_height)
        pygame.draw.rect(surface, (255, 255, 255), self.undo_button, 2, border_radius=15) 
        pygame.draw.rect(surface, undo_color, self.undo_button.inflate(-6, -6), border_radius=15) 
        undo_text = small_font.render("Undo", True, undo_text_color)
        undo_text_rect = undo_text.get_rect(center=self.undo_button.center)
        surface.blit(undo_text, undo_text_rect)

        reset_hovered = self.reset_button.collidepoint(mouse_x, mouse_y)
        reset_color = (255, 255, 255) if reset_hovered else (0, 0, 0) 
        reset_text_color = (0, 0, 0) if reset_hovered else (255, 255, 255)  

        self.reset_button = pygame.Rect(button_x, reset_y, button_width, button_height)
        pygame.draw.rect(surface, (255, 255, 255), self.reset_button, 2, border_radius=15) 
        pygame.draw.rect(surface, reset_color, self.reset_button.inflate(-6, -6), border_radius=15)

        reset_text = small_font.render("Reset", True, reset_text_color)
        reset_text_rect = reset_text.get_rect(center=self.reset_button.center)
        surface.blit(reset_text, reset_text_rect)

    def draw_all(self, pg, surface):
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)
        self.selection.draw(pg, surface, self.grid)
        self.draw_buttons(surface)

    def show(self):
        for cell in self.grid:
            print(cell)

if __name__ == "__main__":
    pygame.init()
    game_font = pygame.font.Font(None, 50)
    difficulty = 3 
    grid = Grid(pygame, game_font, difficulty)
    grid.show()
