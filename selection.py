class SelectNumber:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.btn_w = 55  
        self.btn_h = 55  
        self.my_font = pygame.font.Font(None, 40) 
        self.selected_number = 0

        self.color_selected = (0, 255, 0)
        self.color_normal = (200, 200, 200)

        self.btn_pos = [(705, 50), (770, 50),
                        (705, 115), (770, 115),
                        (705, 180), (770, 180),
                        (705, 245), (770, 245),
                        (770, 310)]

    def draw(self, pygame, surface, grid):
        num_count = {i: 0 for i in range(1, 10)}

        for row in grid:
            for num in row:
                if num in num_count:
                    num_count[num] += 1

        for index, pos in enumerate(self.btn_pos):
            button_rect = [pos[0], pos[1], self.btn_w, self.btn_h]

            if num_count.get(index + 1, 0) == 9:
                pygame.draw.rect(surface, (100, 100, 100), button_rect, width=2, border_radius=10)
                text_color = (100, 100, 100)
            else:
                pygame.draw.rect(surface, self.color_normal, button_rect, width=2, border_radius=10)
                if self.button_hover(pos):
                    pygame.draw.rect(surface, self.color_selected, button_rect, width=2, border_radius=10)
                    text_color = (0, 255, 0)
                else:
                    text_color = self.color_normal

                if self.selected_number > 0 and self.selected_number - 1 == index:
                    pygame.draw.rect(surface, self.color_selected, button_rect, width=3, border_radius=10)
                    text_color = self.color_selected

            text_surface = self.my_font.render(str(index + 1), True, text_color)
            text_rect = text_surface.get_rect(center=(pos[0] + self.btn_w // 2, pos[1] + self.btn_h // 2))
            surface.blit(text_surface, text_rect)

    def button_clicked(self, mouse_x: int, mouse_y: int, grid) -> None:
        num_count = {i: 0 for i in range(1, 10)}

        for row in grid:
            for num in row:
                if num in num_count:
                    num_count[num] += 1

        for index, pos in enumerate(self.btn_pos):
            number = index + 1
            if num_count.get(number, 0) < 9:
                if self.on_button(mouse_x, mouse_y, pos):
                    self.selected_number = number

    def button_hover(self, pos: tuple) -> bool:
        mouse_pos = self.pygame.mouse.get_pos()
        return self.on_button(mouse_pos[0], mouse_pos[1], pos)

    def on_button(self, mouse_x: int, mouse_y: int, pos: tuple) -> bool:
        return pos[0] < mouse_x < pos[0] + self.btn_w and pos[1] < mouse_y < pos[1] + self.btn_h
