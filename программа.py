import pygame
import os
import random
os.environ['SDL_VIDEO_CENTERED'] = '1'  # Помещаем окно игры в центр экрана
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Boom them all — 2')


def load_image(name, color_key=None):  # Функция для загрузки изображения
    fullname = os.path.join('data', name)  # Путь к файлу изображения
    try:
        image = pygame.image.load(fullname)  # Загружаем изображение
    except pygame.error as message:
        print('Не удаётся загрузить:', name)  # Выводим сообщение об ошибке
        raise SystemExit(message)  # Завершаем работу программы
    image = image.convert_alpha()  # Преобразуем изображение в формат RGBA
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))  # Определяем цвет ключа изображения
        image.set_colorkey(color_key)  # Устанавливаем цвет ключа изображения
    return image


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image = pygame.transform.smoothscale(image, (70, 70))
    image_boom = load_image("boom.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - 70)
        self.rect.y = random.randrange(height - 70)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


all_sprites = pygame.sprite.Group()
group_bomb = pygame.sprite.Group()
clock = pygame.time.Clock()
while len(group_bomb) < 20:
    bomb_x = Bomb(all_sprites)
    if len(pygame.sprite.spritecollide(bomb_x, group_bomb, False)) == 0:
        group_bomb.add(bomb_x)
running = True
while running:
    screen.fill((0, 0, 0))
    group_bomb.draw(screen)
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in all_sprites:
                group_bomb.update(event)
    clock.tick(100)
    pygame.display.flip()
pygame.quit()





