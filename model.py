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
    def __init__(self, window, batch, keys, cell_size, height, map):
        super().__init__(window, batch, keys)

        # ボタンの押しっぱなしの監視
        self.keys = keys
        # self.directions = {"left": False, "right": False, "up": False, "down": False}
        self.x = self.width / 2
        self.y = self.height / 2 
        self.cell_size = cell_size
        self.speed = 30
        self.hero = pyglet.image.load('Hero.png')
        self.hero_grid = pyglet.image.ImageGrid(self.hero, 4, 3)
        self.map = map
        
        self.hero_sprite = pyglet.sprite.Sprite(self.hero_grid[10], x = self.x, y = self.y , batch=self.batch)
        self.hero_sprite.z = 2
        self.stop_images = {
            "down": self.hero_grid[10],
            "up": self.hero_grid[1],
            "right": self.hero_grid[4],
            "left": self.hero_grid[7]
        }
        
        # ヒーローの縦の長さ
        self.hero_height = self.hero.height / 4

        # ヒーローの画像をリストにする
        self.hero_frames = list()
        self.hero_grids()

        # ベクトルのリスト
        self.vector_x = 0
        self.vector_y = 0

        # # 現在のフレームインデックス
        # self.current_frame = 0

        # アニメーションのリストを作成
        self.animations = {
                            "left": pyglet.image.Animation.from_image_sequence(self.hero_grid[6:9], duration=0.1, loop=True),
                            "right": pyglet.image.Animation.from_image_sequence(self.hero_grid[3:6], duration=0.1, loop=True),
                            "up": pyglet.image.Animation.from_image_sequence(self.hero_grid[0:3], duration=0.1, loop=True),
                            "down": pyglet.image.Animation.from_image_sequence(self.hero_grid[9:12], duration=0.1, loop=True)
                        }
        
        # 今の方向
        self.past_direction = "down"
        self.new_direction = "down"
        # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
        # pyglet.clock.schedule_interval(self.update, 0.1)
        pyglet.clock.schedule_interval(self.update, 1/60.0)


    def update(self, dt: float):
        self.new_direction = None
        if self.keys[key.LEFT]:
            self.x -= self.speed * dt
            self.new_direction = "left"
            # self.hero_sprite.image = self.animations["left"]
        if self.keys[key.RIGHT]:
            self.x += self.speed * dt
            self.new_direction = "right"
        if self.keys[key.UP]:
            self.y += self.speed * dt
            self.new_direction = "up"
        if self.keys[key.DOWN]:
            self.y -= self.speed * dt
            self.new_direction = "down"
        self.hero_sprite.x = self.x
        self.hero_sprite.y = self.y
 
        self.check_wall()

 
        if self.past_direction == "down" and self.new_direction == None:
            self.hero_sprite.image = self.stop_images["down"]
        elif self.past_direction == "down" and self.new_direction == None:
             self.hero_sprite.image = self.animations["down"]
        elif self.new_direction != None:
            if self.new_direction != self.past_direction:
                self.hero_sprite.image = self.animations[self.new_direction]
                self.past_direction = self.new_direction
        elif self.new_direction == None:
            self.hero_sprite.image = self.stop_images[self.past_direction]

        # 移動中方角が変わった時だけアニメーション、キーを押してない時は静止
        if self.new_direction != None:
            if self.past_direction != self.new_direction:
                self.hero_sprite.image = self.animations[self.new_direction]
                self.past_direction = self.new_direction
        else:
             # キーを押していないときは静止画像
            if self.past_direction:
                self.hero_sprite.image = self.stop_images[self.past_direction]
             


    def check_wall(self):
        # 左の壁に当たった時
        if self.hero_sprite.x <= 0:
                self.hero_sprite.x = 0
        # 右の壁に当たった時
        if self.hero_sprite.x + self.hero_height >= self.width:
                self.hero_sprite.x = self.width - self.hero_height
        # 上の壁に当たった時
        if self.hero_sprite.y + self.hero_height >= self.height:
                self.hero_sprite.y = self.height - self.hero_height
        # 下の壁に当たった時
        if self.hero_sprite.y  <= 0:
                self.hero_sprite.y = 0


    # ヒーローの画像をリストに入れる関数
    def hero_grids(self):
        for num in range(12):
            self.hero_frames.append(self.hero_grid[num])

    # keyによって画像を入れ替える関数
    def change_pic(self, key_num):
        # 現在のフレームインデックス
        self.current_frame = (self.current_frame + 1) % 3 + key_num
        self.hero_sprite.image = self.hero_frames[self.current_frame]

        
        
        
