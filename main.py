import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Click Game")
icon = pygame.image.load("img/icon.jpg")
pygame.display.set_icon(icon)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Шрифт
font = pygame.font.Font(None, 36)

# Класс для объектов
class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 50
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.clicked = False

    def draw(self):
        if self.clicked:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            pygame.draw.rect(screen, WHITE, self.rect, 2)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.clicked = True
            return self.color
        return None

# Функция для создания случайного объекта
def create_random_object():
    x = random.randint(0, WIDTH - 50)
    y = random.randint(0, HEIGHT - 50)
    color = random.choice([GREEN, RED, BLUE, YELLOW])
    return GameObject(x, y, color)

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    score = 0
    objects = []
    game_over = False

    while not game_over:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for obj in objects:
                    color = obj.check_click(event.pos)
                    if color:
                        if color == GREEN:
                            score += 5
                        elif color == RED:
                            score -= 5
                        elif color == BLUE:
                            score += 3
                        elif color == YELLOW:
                            score += 1

        # Создаем новые объекты
        if len(objects) < 5:
            objects.append(create_random_object())

        # Рисуем объекты
        for obj in objects:
            obj.draw()

        # Отображаем счет
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Проверяем условия победы и проигрыша
        if score >= 20:
            win_text = font.render("You Win!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - 50, HEIGHT // 2))
            game_over = True
        elif score < 0:
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