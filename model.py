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
        self.speed = 100
        self.hero = pyglet.image.load('Hero.png')
        self.hero_grid = pyglet.image.ImageGrid(self.hero, 4, 3)
        self.hero_sprite = pyglet.sprite.Sprite(self.hero_grid[10], x = self.width / 2, y= self.height / 2 , batch=self.batch)

        # ヒーローの縦の長さ
        self.hero_height = self.hero.height / 4

        # ヒーローの画像をリストにする
        self.hero_frames = list()
        self.hero_grids()
        print(self.hero_frames)

        # 現在のフレームインデックス
        self.current_frame = 0

        # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
        # pyglet.clock.schedule_interval(self.update, 0.1)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        # 左キーを押した時の処理
        if symbol == key.LEFT:
            self.directions["left"] = True
            # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
            pyglet.clock.schedule_interval(self.update, 0.01)
        # 右キーを押した時の処理
        if symbol == key.RIGHT:
            self.directions["right"] = True
            # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
            pyglet.clock.schedule_interval(self.update, 0.01)
        # 上キー
        if symbol == key.UP:
            self.directions["up"] = True
            # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
            pyglet.clock.schedule_interval(self.update, 0.01)
        # 下キー
        if symbol == key.DOWN:
            self.directions["down"] = True
            # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
            pyglet.clock.schedule_interval(self.update, 0.01)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        # 左キーを離した時の処理
        if symbol == key.LEFT:
            self.directions["left"] = False
            pyglet.clock.unschedule(self.update)
        # 右キーを離した時の処理
        if symbol == key.RIGHT:
            self.directions["right"] = False
            pyglet.clock.unschedule(self.update)
        # 上キー
        if symbol == key.UP:
            self.directions["up"] = False
            pyglet.clock.unschedule(self.update)
        # 下キー
        if symbol == key.DOWN:
            self.directions["down"] = False
            pyglet.clock.unschedule(self.update)

    def update(self, dt: float) -> None:
        if self.directions["left"]:
            self.hero_sprite.x -= self.speed * dt
            key_num = 6
            self.change_pic(key_num)
            self.check_wall()
        if self.directions["right"]:
            self.hero_sprite.x += self.speed * dt
            self.check_wall()
            key_num = 3
            self.change_pic(key_num)
        if self.directions["up"]:
            self.hero_sprite.y += self.speed * dt
            self.check_wall()
            key_num = 0
            self.change_pic(key_num)
        if self.directions["down"]:
            self.hero_sprite.y -= self.speed * dt
            self.check_wall()
            key_num = 9
            self.change_pic(key_num)


    def check_wall(self):
        # 左の壁に当たった時
        if self.hero_sprite.x <= 0:
                self.directions["left"] = False
                self.hero_sprite.x = 0
        # 右の壁に当たった時
        if self.hero_sprite.x + self.hero_height >= self.width:
                self.directions["right"] = False
                self.hero_sprite.x = self.width - self.hero_height
        # 上の壁に当たった時
        if self.hero_sprite.y + self.hero_height >= self.height:
                self.directions["up"] = False
                self.hero_sprite.y = self.height - self.hero_height
        # 下の壁に当たった時
        if self.hero_sprite.y  <= 0:
                self.directions["down"] = False
                self.hero_sprite.y = 0


    # ヒーローの画像をリストに入れる関数
    def hero_grids(self):
        for num in range(12):
            self.hero_frames.append(self.hero_grid[num])

    # keyによって画像を入れ替える関数
    def change_pic(self, key_num):
        # 現在のフレームインデックス
        self.current_frame = (self.current_frame + 1) % 3 + key_num
        print(self.current_frame)
        self.hero_sprite.image = self.hero_frames[self.current_frame]

         

    
        
        
