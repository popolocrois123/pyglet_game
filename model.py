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
        # self.stop_images = {
        #     "down": self.hero_grid[10],
        #     "up": self.hero_grid[1],
        #     "right": self.hero_grid[4],
        #     "left": self.hero_grid[7]
        # }
        
        # # ヒーローの縦の長さ
        # self.hero_height = self.hero.height / 4

        # # ヒーローの画像をリストにする
        # self.hero_frames = list()
        # self.hero_grids()

        # # ベクトルのリスト
        # self.vector_x = 0
        # self.vector_y = 0

        # # # 現在のフレームインデックス
        # # self.current_frame = 0

        # アニメーションのリストを作成
        self.animations = {
                            "left": pyglet.image.Animation.from_image_sequence(self.hero_grid[6:9], duration=0.1, loop=True),
                            "right": pyglet.image.Animation.from_image_sequence(self.hero_grid[3:6], duration=0.1, loop=True),
                            "up": pyglet.image.Animation.from_image_sequence(self.hero_grid[0:3], duration=0.1, loop=True),
                            "down": pyglet.image.Animation.from_image_sequence(self.hero_grid[9:12], duration=0.1, loop=True)
                        }
        
        # # 今の方向
        # self.past_direction = "down"
        # self.new_direction = "down"
        # # 0.5秒ごとに update を呼ぶ（アニメの心臓部分）
        pyglet.clock.schedule_interval(self.update, 0.01)
        # pyglet.clock.schedule_interval(self.update, 1/60.0)

    
    
 
    

    # キーの状況を確認してdx, dyを設定し、移動中ならmove()を呼び出す
    def update(self, dt):
        # 方角と移動の値（dx, dy）の初期化
        dx = dy = 0
        # dx, dyが初期値以外の場合（キャラクターが動いている）move()関数の呼び出し
        # キャラクターがmap_dataのグリッドごとに１マスずつ動くという設定
        # dx, dy の条件によってキャラクターのアニメーションを変更する
        if self.keys[key.LEFT]:
            dx = -1
            self.hero_sprite.image = self.animations["left"]
            self.moving = True
        elif self.keys[key.RIGHT]:
            dx = 1
            self.hero_sprite.image = self.animations["right"]
            self.moving = True
        elif self.keys[key.UP]:
            dy = -1
            self.hero_sprite.image = self.animations["up"]
            self.moving = True
        elif self.keys[key.DOWN]:
            dy = 1
            self.hero_sprite.image = self.animations["down"]
            self.moving = True

        if dx != 0 or dy != 0:
            self.move(dx, dy, self.map, dt)
        # self.new_direction = None
        # # if self.keys[key.LEFT]:
        # #     self.x -= self.speed * dt
        # #     self.new_direction = "left"
        # #     # self.hero_sprite.image = self.animations["left"]
        # # if self.keys[key.RIGHT]:
        # #     self.x += self.speed * dt
        # #     self.new_direction = "right"
        # # if self.keys[key.UP]:
        # #     self.y += self.speed * dt
        # #     self.new_direction = "up"
        # # if self.keys[key.DOWN]:
        # #     self.y -= self.speed * dt
        # #     self.new_direction = "down"
        # # self.x = self.x -1
        # # self.hero_sprite.x = self.x
        # # self.hero_sprite.y = self.y
        
        # self.move(10, 5)
        # self.check_wall()
        # # print(f"{self.x}, {self.y}")
 
        # # if self.past_direction == "down" and self.new_direction == None:
        # #     self.hero_sprite.image = self.stop_images["down"]
        # # elif self.past_direction == "down" and self.new_direction == None:
        # #      self.hero_sprite.image = self.animations["down"]
        # # elif self.new_direction != None:
        # #     if self.new_direction != self.past_direction:
        # #         self.hero_sprite.image = self.animations[self.new_direction]
        # #         self.past_direction = self.new_direction
        # # elif self.new_direction == None:
        # #     self.hero_sprite.image = self.stop_images[self.past_direction]

        # # # 移動中方角が変わった時だけアニメーション、キーを押してない時は静止
        # # if self.new_direction != None:
        # #     if self.past_direction != self.new_direction:
        # #         self.hero_sprite.image = self.animations[self.new_direction]
        # #         self.past_direction = self.new_direction
        # # else:
        # #      # キーを押していないときは静止画像
        # #     if self.past_direction:
        # #         self.hero_sprite.image = self.stop_images[self.past_direction]
    
    # キャラクターの現在地を移動させる
    def move(self, dx, dy, map, dt):
        # 新しい現在位置（new_x, new_y）を作成し、現在位置のグリッド（grid_x, grid_y)とupdateで移動した（dx,dy)を追加
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        # キャラクターが歩ける場所であるならば
        # 現在位置のグリッド（grid_x, grid_y）を新しい現在位置に変更する。
        if self.moving:
            if map.is_walkable(new_x, new_y):
            # キャラクターのスプライトをピクセル単位で移動する
                self.grid_x = new_x
                self.grid_y = new_y
                self.hero_sprite.x = self.grid_x * self.cell_size + dt
                # self.hero_sprite.x = self.grid_x * self.cell_size + dt
                self.hero_sprite.y = self.window_height - (self.grid_y + 1) * self.cell_size + dt
        
            # for i in range(x + 1):
        #     self.x = self.x - 1
        #     self.hero_sprite.x = self.x
        #     pyglet.clock.Clock.sleep(2000)
        # for t in range(y + 1):
        #     self.y = self.y - 1
        #     self.hero_sprite.y = self.y
        #     pyglet.clock.Clock.sleep(2000)


    # def check_wall(self):
    #     # 左の壁に当たった時
    #     if self.hero_sprite.x <= 0:
    #             self.hero_sprite.x = 0
    #     # 右の壁に当たった時
    #     if self.hero_sprite.x + self.hero_height >= self.width:
    #             self.hero_sprite.x = self.width - self.hero_height
    #     # 上の壁に当たった時
    #     if self.hero_sprite.y + self.hero_height >= self.height:
    #             self.hero_sprite.y = self.height - self.hero_height
    #     # 下の壁に当たった時
    #     if self.hero_sprite.y  <= 0:
    #             self.hero_sprite.y = 0


    # ヒーローの画像をリストに入れる関数
    def hero_grids(self):
        for num in range(12):
            self.hero_frames.append(self.hero_grid[num])

    # keyによって画像を入れ替える関数
    def change_pic(self, key_num):
        # 現在のフレームインデックス
        self.current_frame = (self.current_frame + 1) % 3 + key_num
        self.hero_sprite.image = self.hero_frames[self.current_frame]

    
        
        
