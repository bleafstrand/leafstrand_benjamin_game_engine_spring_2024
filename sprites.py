# This file was created by: Benjamin Leafstrand

#import modules


#create a player class
import pygame as pg
from pygame.sprite import Sprite
from setting import *
#create a wall class

#make sure Player is capitilized
class Player(Sprite):
    # creat init method/function that allow us to assign properties
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 3000
        self.dash_start_time = 0
        self.dash_duration = 1
    

    #def move(self, dx=0, dy=0):
        #self.x += dx
        #self.y += dy

    def get_keys(self):
        self.vx, self.vy = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            if self.dash_start_time == 0:
                self.dash_start_time = pg.time.get_ticks()
            if pg.time.get_ticks() - self.dash_start_time < self.dash_duration * 100:
                self.vx *= 2
                self.vy *= 2
            else:
                self.dash_start_time = 0
        if self.vx != 0 and self.vy != 0:
            self.vx *=0.7071
            self.vy *=0.7071
        
    def collide_with_obj(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            self.rect.width += 25
            self.rect.height += 25

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits: 
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right 
                self.vx=0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits: 
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom 
                self.vy=0
                self.rect.y = self.y

#woohoo math
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        #add x collision in future
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        #add y collision in future
        self.collide_with_obj(self.game.mobs, False)
        if self.game.map_data[int(self.y // TILESIZE)][int(self.x // TILESIZE)] == 'F':
                self.show_congratulations_popup()
    
    def show_congratulations_popup(self):
        popup_text = "Congratulations! You finished the hardest game in the world."
        popup_font = pg.font.Font(None, 30)
        popup_surface = popup_font.render(popup_text, True, WHITE)
        popup_rect = popup_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.game.screen.blit(popup_surface, popup_rect)
        pg.display.flip()
        pg.time.wait(3000)


class Wall(Sprite):
    # creat init method/function that allow us to assign properties
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

    