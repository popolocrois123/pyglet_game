import pyglet

class Map():
    def __init__(self, map_data, cell_size, batch, height):
        self.map_data = map_data
        self.cell_size = cell_size
        self.batch = batch
        self.height = height

        self.tiles = []

        self.load_map()

    def load_map(self):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                pixel_x = x * self.cell_size
                pixel_y = self.height - (y + 1) * self.cell_size
                # 場合分け
                if cell == "B":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size, 
                                                   color=(255, 255, 255), batch=self.batch)
                elif cell == ".":
                    pass
                elif cell == "P":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, self.cell_size, 
                                                   color=(0, 0, 255), batch=self.batch)
                elif cell == "N":
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y,  self.cell_size, self.cell_size, 
                                                   color=(255, 255, 0), batch=self.batch)
                self.tiles.append(rect)

class Background():
    def __init__(self, window, batch):
        self.window = window
        self.batch = batch
        self.background_pic = pyglet.image.load('map_sample.png')
        self.background_sprite = pyglet.sprite.Sprite(self.background_pic, x = 0, y = 0, batch=self.batch)
        self.background_sprite.z = 0
        # 引数として渡されたウィンドウのwidthとheightを取り出す
        self.width = self.window.get_size()[0]
        self.height = self.window.get_size()[1]
        # スケーリング係数を設定
        self.background_sprite.scale_x = window.width / self.background_pic.width
        self.background_sprite.scale_y = window.height / self.background_pic.height
    
        
