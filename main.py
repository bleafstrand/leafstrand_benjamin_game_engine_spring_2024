#this file was created by: Benjamin Leafstrand
#my first source control edit
#importing modules
import pygame as pg
import sys
from setting import *
from random import randint
from sprites import *
from os import path
# I want to add another maze level to make the game even more hard :)
# data types: in, string, float, bool
#Tino helped with specail ability
#Used the help of ChatGPT for text once completed level
#Used ccozort for mob and help
# Character ability, spawned enemies, start screen, music

#creating the game class
class Game:
    #inializes function
    def __init__(self):
        pg.init()
        #self.img_folder = path.join(self.game_folder, 'images')
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        #inializes music
        pg.mixer.init()
    #we have defined the run method in our function
    
    #load game data
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'tr') as f:
            for line in f:
                self.map_data.append(line)


    def new(self):
        #loads music and plays
        pg.mixer.music.load('music.mp3')
        pg.mixer.music.play(loops=-1)
        
        # init all variables, setup groups, instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        # self.player = Player(self, 10, 10)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            #print(row)
            #print(tiles)
            for col, tile in enumerate(tiles):
                #print(col)
                #print(tile)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == '6':
                    Secret(self, col, row)

            
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
#ai assisted: Defines draw_text function
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
         self.all_sprites.update()
#grid is created
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw(self):
        #BGCOLOR in setting.py
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
           
    #input method
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            #if event.type == pg.KEYDOWN:
                #if event.key == pg.K_LEFT:
                    #self.player.move(dx=-1)
                #if event.key == pg.K_RIGHT:
                    #self.player.move(dx=1)
                #if event.key == pg.K_UP:
                    #self.player.move(dy=-1)d
                #if event.key == pg.K_DOWN:
                    #self.player.move(dy=1)
    #start screen
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "Welcome to the hardest game on the history of the planet. Your goal is to reach the center of the maze. Good Luck" , 20, GREEN, WIDTH/2 - 32, 2)
        pg.display.flip()
        #waits for any key to get pressedr
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    
           
#i have instantiated the game
g = Game()
g.show_start_screen()  # Display the start screen first
while True:
    g.new()
    g.run()
     #g.show_go_screen()
#imports pygames, creates library,
g.run()
