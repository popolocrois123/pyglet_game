import pyglet

class Map():
    def __init__(self, map_data, cell_size, batch, height):
        self.map_data = map_data
        self.cell_size = cell_size
        self.batch = batch
        self.height = height

        self.tiles = []

        # playerのスタート位置
        self.player_start = (0, 0)

        self.load_map()


    # セルの対応文字ごとにいろと役割を設定する（例：Bはグレーなど）
    # マップの文字情報（グリッド）をピクセル座標に変換する
    # キャラクターがマップの各マス（グリッド）に移動できるかどうかを判別する関数（is_walkable)
    def load_map(self):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                pixel_x = x * self.cell_size
                pixel_y = self.height - (y + 1) * self.cell_size
                # ブロックごとの座標
                # print(f"{cell}: {pixel_x}, {pixel_y}")
                # 場合分け
                if cell == "B":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size, 
                                                   color=(255, 255, 255), batch=self.batch)
                    self.tiles.append(rect)
                elif cell == ".":
                    pass
                elif cell == "P":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, self.cell_size, 
                                                   color=(0, 0, 255), batch=self.batch)
                    self.player_start = (x, y)
                    print(f"{cell}: {pixel_x}, {pixel_y}")
                elif cell == "N":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, self.cell_size, 
                                                   color=(255, 255, 0), batch=self.batch)
                    self.tiles.append(rect)
    
    def is_walkable(self, x, y):
        if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
            return self.map_data[y][x] != "B"
        return False
                        
                

class Background():
    def __init__(self, window, batch):
        self.window = window
        self.batch = batch
        # マップのイラストの読み込み
        self.background_pic = pyglet.image.load('map_sample.png')
        # マップのイラストをspriteに設定する
        self.background_sprite = pyglet.sprite.Sprite(self.background_pic, x = 0, y = 0, batch=self.batch)
        self.background_sprite.z = 0
        # 引数として渡されたウィンドウのwidthとheightを取り出す
        self.width = self.window.get_size()[0]
        self.height = self.window.get_size()[1]
        # スケーリング係数を設定
        self.background_sprite.scale_x = window.width / self.background_pic.width
        self.background_sprite.scale_y = window.height / self.background_pic.height
    
        
