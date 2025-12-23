import pyglet

window = pyglet.window.Window()

# GIFアニメーションを読み込む
animation = pyglet.image.load_animation('Hero_down.gif')

# フレームごとの画像とdurationを取得し、新しいdurationで再構成
new_duration = 0.2  # 1フレームあたりの秒数（例：0.2秒 = 5fps）

frames = []
for frame in animation.frames:
    new_frame = pyglet.image.AnimationFrame(image=frame.image, duration=new_duration)
    frames.append(new_frame)

# 新しいアニメーションを作成
new_animation = pyglet.image.Animation(frames)

# スプライトに設定
sprite = pyglet.sprite.Sprite(img=new_animation)

@window.event
def on_draw():
    window.clear()
    sprite.draw()

pyglet.app.run()
