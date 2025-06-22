import pyglet
from pyglet.window import key
from pyglet import shapes



class Character():
    def __init__(self, window, batch, keys):
        self.window = window
        self.batch = batch
        
        # 引数として渡されたウィンドウのwidthとheightを取り出す
        self.width = self.window.get_size()[0]
        self.height = self.window.get_size()[1]


class Hero(Character):
    def __init__(self, px, py, window, batch, cell_size, map, keys):
        super().__init__(window, batch, keys)
        self.grid_x = px
        self.grid_y = py

        # ボタンの押しっぱなしの監視
        self.keys = keys
        # self.directions = {"left": False, "right": False, "up": False, "down": False}
        self.x = 512
        self.y = 192 
        self.cell_size = cell_size
        self.map = map
        self.speed = 30
        self.window_height = window.get_size()[1]
        # heroイメージの読み込み
        self.hero = pyglet.image.load('Hero.png')
        self.hero_grid = pyglet.image.ImageGrid(self.hero, 4, 3)
        self.hero_sprite = pyglet.sprite.Sprite(self.hero_grid[10], x = self.grid_x * cell_size, 
                                                y = self.window_height - (self.grid_y + 1) * cell_size ,
                                                batch=self.batch)
        self.moving = False
        self.hero_sprite.z = 2

        self.map = map
        self.target_x, self.target_y = 6, 6
        self.reached_target = False

        # アニメーションのリストを作成
        self.animations = {
                            "left": pyglet.image.Animation.from_image_sequence(self.hero_grid[6:9], duration=0.1, loop=True),
                            "right": pyglet.image.Animation.from_image_sequence(self.hero_grid[3:6], duration=0.1, loop=True),
                            "up": pyglet.image.Animation.from_image_sequence(self.hero_grid[0:3], duration=0.1, loop=True),
                            "down": pyglet.image.Animation.from_image_sequence(self.hero_grid[9:12], duration=0.1, loop=True)
                        }
    

    def update(self, dt):
        self.move_target()

    def move_target(self):
        if self.grid_x != self.target_x:
            step_x = 1 if self.target_x > self.grid_x else -1
            self.grid_x = self.grid_x + step_x
            self.hero_sprite.x = self.grid_x * self.cell_size

        if self.grid_y != self.target_y:
            step_y = 1 if self.target_y > self.grid_y else -1
            self.grid_y += step_y
            self.hero_sprite.y = self.window_height - (self.grid_y + 1) * self.cell_size

        if self.grid_x == self.target_x and self.grid_y == self.target_y:
                if not self.reached_target:
                    print("着席しました。")
                    self.reached_target = True


        
