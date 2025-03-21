import pygame
import os
import tkinter as tk
from tkinter import messagebox
from grid import Grid

os.environ['SDK_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 100)

pygame.init()

surface = pygame.display.set_mode((900, 625))
pygame.display.set_caption('Sudoku')

pygame.font.init()
title_font = pygame.font.SysFont('comic sans MS', 60)
button_font = pygame.font.SysFont('comic sans MS', 40)
game_font = pygame.font.SysFont('comic sans MS', 40)

grid = None
running = True
in_menu = True
difficulty = None
display_win = False
error_count = 0  

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.default_color = (200, 200, 200)
        self.hover_color = (255, 255, 255)
        self.text_color = (0, 0, 0)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.default_color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surface = button_font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

difficulty_buttons = [
    Button(350, 225, 200, 60, "Easy", 1),
    Button(350, 325, 200, 60, "Medium", 2),
    Button(350, 425, 200, 60, "Hard", 3)
]

new_game_button = Button(350, 500, 200, 60, "New Game")

def show_alert():
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning("Game Over", "You've made 3 errors! Try again.")
    root.destroy()

def draw_errors():
    for i in range(min(error_count, 3)):
        x_pos = 805 - (i * 50)
        y_pos = 400
        cross_size = 30
        thickness = 8
        
        pygame.draw.line(surface, (255, 0, 0), (x_pos, y_pos), (x_pos + cross_size, y_pos + cross_size), thickness)
        pygame.draw.line(surface, (255, 0, 0), (x_pos + cross_size, y_pos), (x_pos, y_pos + cross_size), thickness)

    if error_count == 3:
        pygame.time.delay(500)
        show_alert()
        reset_game()

def reset_game():
    global in_menu, error_count
    error_count = 0
    in_menu = True

def show_menu():
    surface.fill((0, 0, 0))
    title_text = title_font.render("Sudoku Game", True, (255, 255, 255))
    surface.blit(title_text, (260, 100))
    for button in difficulty_buttons:
        button.draw(surface)
    pygame.display.flip()

def show_win_screen():
    surface.fill((0, 0, 0))
    win_text = title_font.render("YOU WIN!", True, (255, 255, 255))
    win_text_rect = win_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 50))
    surface.blit(win_text, win_text_rect)
    new_game_button.rect = pygame.Rect(300, 380, 300, 80)
    new_game_button.draw(surface)
    pygame.display.flip()

while running:
    if in_menu:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in difficulty_buttons:
                    if button.is_clicked(event.pos):
                        difficulty = button.action
                        in_menu = False
                        display_win = False
                        error_count = 0
                        grid = Grid(pygame, game_font, difficulty)
    elif display_win:
        show_win_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if new_game_button.is_clicked(event.pos):
                    in_menu = True
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                move_result = grid.get_mouse_click(pos[0], pos[1])

                if move_result == "incorrect":
                    error_count += 1
                elif move_result == "reset":
                    error_count = 0  

                if error_count >= 3:
                    draw_errors()

        surface.fill((0, 0, 0))
        grid.draw_all(pygame, surface)
        draw_errors()

        if grid.win:
            display_win = True

        pygame.display.flip()

pygame.quit()
