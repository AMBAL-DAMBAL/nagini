import pygame as pg
from pygame.math import Vector2
 

class Player(pg.sprite.Sprite):

    def __init__(self, pos, color, left, right, up, down, fire,
                 all_sprites, bullets, enemy_bullets):
        super().__init__()
        self.image = pg.Surface((30, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = Vector2(0, 0)
        self.pos = Vector2(self.rect.topleft)
        self.dt = 0.03
        self.key_left = left
        self.key_right = right
        self.key_up = up
        self.key_down = down
        self.key_fire = fire
        self.all_sprites = all_sprites
        self.bullets = bullets
        self.enemy_bullets = enemy_bullets
        self.fire_direction = Vector2(350, 0)
        self.health = 3

    def update(self, dt):
        self.dt = dt
        self.pos += self.vel
        self.rect.center = self.pos

        collided_bullets = pg.sprite.spritecollide(self, self.enemy_bullets, True)
        for bullet in collided_bullets:
            self.health -= 1
            if self.health <= 0:
                self.kill()

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.key_left:
                self.vel.x = -90 * self.dt
                self.fire_direction = Vector2(-350, 0)
            elif event.key == self.key_right:
                self.vel.x = 90 * self.dt
                self.fire_direction = Vector2(350, 0)
            elif event.key == self.key_up:
                self.vel.y = -90 * self.dt
                self.fire_direction = Vector2(0, -350)
            elif event.key == self.key_down:
                self.vel.y = 90 * self.dt
                self.fire_direction = Vector2(0, 350)
            elif event.key == self.key_fire:   
                bullet = Bullet(self.rect.center, self.fire_direction)
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
        elif event.type == pg.KEYUP:
            if event.key == self.key_left and self.vel.x < 0:
                self.vel.x = 0
            elif event.key == self.key_right and self.vel.x > 0:
                self.vel.x = 0
            elif event.key == self.key_up and self.vel.y < 0:
                self.vel.y = 0
            elif event.key == self.key_down and self.vel.y > 0:
                self.vel.y = 0


class Bullet(pg.sprite.Sprite):

    def __init__(self, pos, velocity):
        super().__init__()
        self.image = pg.Surface((5, 5))
        self.image.fill(pg.Color('aquamarine1'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.vel = velocity

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos


class Game:

    def __init__(self):
        self.fps = 30
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((800, 600))
        self.bg_color = pg.Color('gray30')

         
        self.all_sprites = pg.sprite.Group()
        self.bullets1 = pg.sprite.Group()    
        self.bullets2 = pg.sprite.Group()   
        player1 = Player(
            (100, 300), pg.Color('dodgerblue2'),
            pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_f,
            self.all_sprites, self.bullets1, self.bullets2)   
        player2 = Player(
            (300, 400),  pg.Color('sienna2'),
            pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_SPACE,
            self.all_sprites, self.bullets2, self.bullets1)   
        self.all_sprites.add(player1, player2)
        self.players = pg.sprite.Group(player1, player2)

    def run(self):
        while not self.done:
            self.dt = self.clock.tick(self.fps) / 1000
            self.handle_events()
            self.run_logic()
            self.draw()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            for player in self.players:
                player.handle_event(event)

    def run_logic(self):
        self.all_sprites.update(self.dt)

    def draw(self):
        self.screen.fill(self.bg_color)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    Game().run()
    pg.quit()
