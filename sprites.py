# This file was created by: Benjamin Leafstrand

#import modules


#create a player class
from os import path
import pygame as pg
from pygame.sprite import Sprite
from setting import *
#create a wall class
SPRITESHEET = "theBell.png"
# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# needed for animated sprite

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image


#make sure Player is capitilized
class Player(Sprite):
    # creat init method/function that allow us to assign properties
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        # needed for animated sprite
        self.load_images()
        #self.image.fill(YELLOW)
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 3000
        self.dash_start_time = 0
        self.dash_duration = 1
         # needed for animated sprite
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False
        self.can_collide = True

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32)]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            self.image = self.standing_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    

    #def move(self, dx=0, dy=0):
        #self.x += dx
        #self.y += dy
#this is where play movement happens
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
            #special ability
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
#collion detection
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
        if self.game.map_data[int(self.rect.y // TILESIZE)][int(self.rect.x // TILESIZE)] == 'F':
            # Restart the level
            self.game.new()
            #spawn mob at A position on map
            for row, tiles in enumerate(self.game.map_data):
                for col, tile in enumerate(tiles):
                    if tile == 'A':
                        Mob(self.game, col, row)
        self.animate()
        self.get_keys()
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
  #ai assisted code  
    def show_congratulations_popup(self):
        popup_text = "Congratulations! You finished the hardest game in the world.... SIKE your toast on this next one buddy"
        popup_font = pg.font.Font(None, 30)
        popup_surface = popup_font.render(popup_text, True, WHITE, BLACK)
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

#mob class
class Mob(pg.sprite.Sprite):
    #properties of class
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
