import pygame
import random
import sys
import time
from config import *  # Импортируем настройки из config.py

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(bg_color)
pygame.display.set_caption("Color Click Game")
icon = pygame.image.load("img/icon.jpg")
pygame.display.set_icon(icon)

star = pygame.image.load("img/star.png")
red_star = pygame.image.load("img/red.png")
green_star = pygame.image.load("img/green.png")
blue_star = pygame.image.load("img/blue.png")
yellow_star = pygame.image.load("img/yellow.png")

# Шрифт
font = pygame.font.Font(None, FONT_SIZE)

# Класс для объектов
class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.img_name = f"{color}_star"
        self.size = OBJECT_SIZE
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.clicked = False
        self.spawn_time = time.time()  # Время появления объекта

    def draw(self):
        if self.clicked:
            screen.blit(eval(self.img_name), (self.x, self.y))
        else:
            screen.blit(star, (self.x, self.y))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True
            return self.color
        return None

    def is_expired(self):
        # Проверяем, прошло ли OBJECT_LIFETIME секунд с момента появления
        return time.time() - self.spawn_time > OBJECT_LIFETIME

# Функция для создания случайного объекта
def create_random_object():
    x = random.randint(0, WIDTH - OBJECT_SIZE)
    y = random.randint(0, HEIGHT - OBJECT_SIZE)
    color = random.choice(['green', 'red', 'blue', 'yellow'])
    return GameObject(x, y, color)

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    score = 0
    objects = []
    game_over = False
    last_spawn_time = time.time()  # Время последнего появления объекта

    while not game_over:
        screen.fill(bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in objects:
                    color = obj.check_click(event.pos)
                    print(color)
                    if color:
                        if color == 'green':
                            score += 5
                        elif color == 'red':
                            score -= 5
                        elif color == 'blue':
                            score += 3
                        elif color == 'yellow':
                            score += 1

        # Появление объектов каждую секунду
        current_time = time.time()
        if current_time - last_spawn_time >= SPAWN_INTERVAL:
            objects.append(create_random_object())
            last_spawn_time = current_time

        # Удаляем объекты, которые "просрочены"
        objects = [obj for obj in objects if not obj.is_expired()]

        # Рисуем объекты
        for obj in objects:
            obj.draw()

        # Отображаем счет
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Проверяем условия победы и проигрыша
        if score >= WIN_SCORE:
            win_text = font.render("You Win!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - 50, HEIGHT // 2))
            game_over = True
        elif score <= LOSE_SCORE:
            lose_text = font.render("You Lose!", True, RED)
            screen.blit(lose_text, (WIDTH // 2 - 50, HEIGHT // 2))
            game_over = True

        pygame.display.flip()
        clock.tick(30)

    # Ожидание перед закрытием
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()