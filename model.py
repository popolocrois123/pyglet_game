import pyglet
from pyglet.window import key
from pyglet import shapes


class Character():
    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()
        
        # 引数として渡されたウィンドウのwidthとheightを取り出す
        self.width = self.window.get_size()[0]
        self.height = self.window.get_size()[1]


class Hero(Character):
    def __init__(self, window):
        super().__init__(window)
        self.directions = {"left": False, "right": False, "up": False, "down": False}
        self.speed = 120
        self.hero = pyglet.image.load('Hero.png')
        self.hero_grid = pyglet.image.ImageGrid(self.hero, 4, 3)
        self.hero_sprite = pyglet.sprite.Sprite(self.hero_grid[10], x = self.width / 2, y= self.height / 2 , batch=self.batch)

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
        # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
        # pyglet.clock.schedule_interval(self.update, 0.1)
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # 左キーを押した時の処理
        if symbol == key.LEFT:
            self.directions["left"] = True
            # self.hero_sprite.image = self.animations["left"]
            # pyglet.clock.schedule_interval(self.update, 0.01)
        # 右キーを押した時の処理
        if symbol == key.RIGHT:
            self.directions["right"] = True
            # self.hero_sprite.image = self.animations["right"]
            # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
            # pyglet.clock.schedule_interval(self.update, 0.5)
        # 上キー
        if symbol == key.UP:
            self.directions["up"] = True
            # self.hero_sprite.image = self.animations["up"]
            # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
            # pyglet.clock.schedule_interval(self.update, 0.5)
        # 下キー
        if symbol == key.DOWN:
            self.directions["down"] = True
            # self.hero_sprite.image = self.animations["down"]
            # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
            # pyglet.clock.schedule_interval(self.update, 0.5)


    def on_key_release(self, symbol: int, modifiers: int) -> None:
        # 左キーを離した時の処理
        if symbol == key.LEFT:
            self.directions["left"] = False
            self.hero_sprite.image = self.hero_grid[7]
            
            
        # 右キーを離した時の処理
        elif symbol == key.RIGHT:
            self.directions["right"] = False
            self.hero_sprite.image = self.hero_grid[4]
            # pyglet.clock.unschedule(self.update)
        # 上キー
        elif symbol == key.UP:
            self.directions["up"] = False
            self.hero_sprite.image = self.hero_grid[1]
            # pyglet.clock.unschedule(self.update)
        # 下キー
        elif symbol == key.DOWN:
            self.directions["down"] = False
            self.hero_sprite.image = self.hero_grid[10]
            # pyglet.clock.unschedule(self.update)

        self.vector_x = 0
        self.vector_y = 0

    def update(self, dt: float) -> None:
        new_direction = None
        if self.directions["left"]:
            self.vector_x = -1
            new_direction = "left"
            
        if self.directions["right"]:
            self.vector_x = 1
            new_direction = "right"

        if self.directions["up"]:
            self.vector_y = 1
            new_direction = "up"

        if self.directions["down"]:
            self.vector_y = -1
            new_direction = "down"

        self.hero_sprite.x += self.vector_x * self.speed * dt
        self.hero_sprite.y += self.vector_y * self.speed * dt
        self.check_wall()

        # アニメーションの変更

        if new_direction is not None and new_direction != self.past_direction:
            self.hero_sprite.image = self.animations[new_direction]
            self.past_direction = new_direction
        elif new_direction is None and self.past_direction == "down":
            self.hero_sprite.image = self.animations["down"]
        

        # if self.vector_x < 0 and self.past_direction != new_direction:
        #     self.hero_sprite.image = self.animations["left"]
        # if self.vector_x > 0 and self.past_direction != new_direction:
        #     self.hero_sprite.image = self.animations["right"]
        # if self.vector_y > 0 and self.past_direction != new_direction:
        #     self.hero_sprite.image = self.animations["up"]
        # if self.vector_y < 0 and self.past_direction != new_direction:
        #     self.hero_sprite.image = self.animations["down"] 

    def check_wall(self):
        # 左の壁に当たった時
        if self.hero_sprite.x <= 0:
                # self.directions["left"] = False
                self.hero_sprite.x = 0
                # self.vector_x = 0
        # 右の壁に当たった時
        if self.hero_sprite.x + self.hero_height >= self.width:
                # self.directions["right"] = False
                self.hero_sprite.x = self.width - self.hero_height
                # self.vector_x = 0
        # 上の壁に当たった時
        if self.hero_sprite.y + self.hero_height >= self.height:
                # self.directions["up"] = False
                self.hero_sprite.y = self.height - self.hero_height
                # self.vector_y = 0
        # 下の壁に当たった時
        if self.hero_sprite.y  <= 0:
                # self.directions["down"] = False
                self.hero_sprite.y = 0
                # self.vector_y = 0


    # ヒーローの画像をリストに入れる関数
    def hero_grids(self):
        for num in range(12):
            self.hero_frames.append(self.hero_grid[num])

    # keyによって画像を入れ替える関数
    def change_pic(self, key_num):
        # 現在のフレームインデックス
        self.current_frame = (self.current_frame + 1) % 3 + key_num
        self.hero_sprite.image = self.hero_frames[self.current_frame]


         

    
        
        
