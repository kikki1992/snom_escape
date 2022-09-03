import pyxel
player_w = 14
player_h = 10
class Player:
    def __init__(self,x=0,y=0):
        #imgファイルの用意
        pyxel.load("assets/img.pyxres")
        #初期位置
        self.w = player_w
        self.h = player_h
        self.x = pyxel.width/2 - self.w/2
        self.y = pyxel.height/2 - self.h/2
        self.is_alive = True

    def update(self):
        #プレイヤーの移動
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < pyxel.width - self.w: 
            self.x += 2
        if pyxel.btn(pyxel.KEY_UP) and self.y > 0: 
            self.y -= 2
        if pyxel.btn(pyxel.KEY_DOWN) and self.y < pyxel.height - self.h: 
            self.y += 2        
