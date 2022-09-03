import pyxel
import math
import Player as player

player_img_x = 0
player_img_y = 4
player_w = 14
player_h = 10
player_hit_img_x = 3
player_hit_img_y = 2
player_hit_w = 9
player_hit_h = 9

monsterball_x = 180
monsterball_img_x = 0
monsterball_img_y = 16
monsterball_w = 16
monsterball_h = 16
monsterball_hit_img_x = 3
monsterball_hit_img_y = 3
monsterball_hit_w = 9
monsterball_hit_h = 9

monsterball_y_min = 0
monsterball_y_max = 108
monsterball_speed_min = 1
monsterball_speed_max =3
monsterball_intensity_min = 0
monsterball_intensity_max = 3.5

catch_time = 30

motion1_x = 40
motion1_y = 10
motion1_img_x = 0
motion1_img_y = 0
motion1_w = 87
motion1_h = 90

motion2_x = 42
motion2_y = 10
motion2_img_x = 88
motion2_img_y = 0
motion2_w = 110
motion2_h = 90

motion3_x = 28
motion3_y = 10
motion3_img_x = 0
motion3_img_y = 88
motion3_w = 110
motion3_h = 90

motion4_x = 0
motion4_y = 0
motion4_img_x = 100
motion4_img_y = 114
motion4_w = 160
motion4_h = 140

escape_x = 55
escape_y = 24
escape_img_x = 12
escape_img_y = 116
escape_w = 40
escape_h = 32

Mainmenu_Message = """        
Yukihami Escaping
Start Push "R"Key 
"""
Gameover_Message = """        
Game Over
Restart Push "R"Key
Main Menu Push "S"key
"""

revive_Message = """
ball kara tobidasitazo!
Push "0"key Continue"""



#Enemies class
class MonsterBall: 
    def __init__(self):
        #imgファイルの用意
        pyxel.load("assets/img.pyxres")
        #初期位置
        self.w = monsterball_w
        self.h = monsterball_h
        self.is_alive = True
        self.timer = 0

    def update(self,x,y,speed,intensity):
        self.speed = speed
        self.x = x
        self.x -= self.speed
        self.timer += 0.1
        self.intensity = intensity
        self.y = y + self.intensity*math.sin(self.timer)

class App:
    def __init__(self):
        #Windowの作成
        pyxel.init(160,120,title="Yukihami Escaping")
        #imgファイルの用意
        pyxel.load("assets/img.pyxres")
        self.score = 0
        self.chance1 = 0
        self.chance2 = 0
        self.chance3 = 0
        self.motion1 = False
        self.motion2 = False
        self.motion3 = False
        self.motion4 = False
        self.start()
        pyxel.playm(1, loop = True)
        #書き出し
        pyxel.run(self.update,self.draw)

    def reset(self):
        #初期値の設定--
        self.menu = False
        self.score = 0
        self.motion_time = 0
        #player classの呼び出し
        self.player = player.Player()
        self.Monsterballs = []
        pyxel.playm(1, loop = True)

    def start(self):
        self.menu = True
        self.player = player.Player()
        self.Monsterballs = []

    def revive(self):
        #初期値の設定--
        self.motion_time = 0
        self.menu = False
        #player classの呼び出し
        self.player = player.Player()
        monsterball_count = len(self.Monsterballs)
        for i in range(monsterball_count):
            self.Monsterballs[i].is_alive = True
            self.Monsterballs[i].x = 180
        pyxel.playm(1, loop = True)

    def chance(self):
        self.chance1 = pyxel.rndi(0,round(self.score/15))
        self.chance2 = pyxel.rndi(0,round(self.score/30))
        self.chance3 = pyxel.rndi(0,round(self.score/45))
    
    def motion(self):
        if self.chance1 <= 3:
            self.motion1 = True
            self.motion2 = False
            self.motion3 = False
            self.motion4 = False

        elif self.chance2 <= 3:
            self.motion1 = False
            self.motion2 = True
            self.motion3 = False
            self.motion4 = False

        elif self.chance3 <= 3:
            self.motion1 = False
            self.motion2 = False
            self.motion3 = True
            self.motion4 = False
        else:
            self.motion1 = False
            self.motion2 = False
            self.motion3 = False
            self.motion4 = True

    def update(self):
        #score
        time_score = pyxel.frame_count % 10
        if ((time_score == 9) and 
            (self.player.is_alive == True)):
            self.score += 10
        
        monsterball_count = len(self.Monsterballs)
        #モンスターボール------------------------------------------------
        if self.score >= monsterball_count*50 and self.score <= 600:
            self.new_monsterball = MonsterBall()
            self.new_monsterball.update(monsterball_x,
                                    pyxel.rndi(monsterball_y_min,monsterball_y_max),
                                    pyxel.rndi(monsterball_speed_min,monsterball_speed_max),
                                    pyxel.rndf(monsterball_intensity_min,monsterball_intensity_max))
            self.Monsterballs.append(self.new_monsterball)
        monsterball_count = len(self.Monsterballs)

        for i in range(monsterball_count):
            self.Monsterballs[i].update(self.Monsterballs[i].x,
                                        self.Monsterballs[i].y,
                                        self.Monsterballs[i].speed,
                                        self.Monsterballs[i].intensity)
            if self.Monsterballs[i].x <= -10:
                self.Monsterballs[i].x = monsterball_x
                self.Monsterballs[i].y = pyxel.rndi(monsterball_y_min,monsterball_y_max)
                self.Monsterballs[i].speed = pyxel.rndf(monsterball_speed_min,monsterball_speed_max)
                self.Monsterballs[i].intensity = pyxel.rndf(monsterball_intensity_min,monsterball_intensity_max)
        #当たり判定
            e_x_min = self.Monsterballs[i].x +monsterball_hit_img_x
            e_x_max = self.Monsterballs[i].x +monsterball_hit_img_x + monsterball_hit_w
            e_y_min = self.Monsterballs[i].y +monsterball_hit_img_y
            e_y_max = self.Monsterballs[i].y +monsterball_hit_img_y + monsterball_hit_h
            p_x_min = self.player.x + player_hit_img_x
            p_x_max = self.player.x + player_hit_img_x + player_hit_w
            p_y_min = self.player.y + player_hit_img_y 
            p_y_max = self.player.y + player_hit_img_y + player_hit_h 

            if ((e_x_min< p_x_min)
                and (p_x_min < e_x_max)
                and (e_y_min < p_y_min)
                and (p_y_min < e_y_max)
                or(e_x_min< p_x_max)
                and (p_x_max < e_x_max)
                and (e_y_min < p_y_min)
                and (p_y_min < e_y_max)
                or(e_x_min< p_x_min)
                and (p_x_min < e_x_max)
                and (e_y_min < p_y_max)
                and (p_y_max < e_y_max)
                or(e_x_min< p_x_max)
                and (p_x_max < e_x_max)
                and (e_y_min < p_y_max)
                and (p_y_max < e_y_max)):
                self.player.is_alive = False
                
                for j in range(monsterball_count):
                    if ((self.player.is_alive == False) 
                        and (self.Monsterballs[j].is_alive==True)):
                        pyxel.play(0,4)
                        self.chance()
                    self.Monsterballs[j].is_alive = False
                    
        self.motion()            

        if ((self.menu == False)
            and (self.player.is_alive == False)):

            self.plus = pyxel.frame_count %2
            self.motion_time += self.plus
            if  self.motion1 == True:
                if pyxel.btn(pyxel.KEY_0):
                    self.revive()
                if self.motion_time == catch_time:
                    pyxel.play(0,5)
            elif self.motion2 == True:
                if pyxel.btn(pyxel.KEY_0):
                    self.revive()
                if self.motion_time == catch_time:
                    pyxel.play(0,4)
                elif self.motion_time == 2*catch_time:
                    pyxel.play(0,5)
            elif self.motion3 == True:
                if pyxel.btn(pyxel.KEY_0):
                    self.revive()
                if self.motion_time == catch_time:
                    pyxel.play(0,4)
                elif self.motion_time == 2*catch_time:
                    pyxel.play(0,4)
                elif self.motion_time == 3*catch_time:
                    pyxel.play(0,5)
            elif self.motion4 == True:
                if self.motion_time == catch_time:
                    pyxel.play(0,4)
                elif self.motion_time == 2*catch_time:
                    pyxel.play(0,4)
                elif self.motion_time == 3*catch_time:
                    pyxel.play(0,6)


        if pyxel.btn(pyxel.KEY_R):
            self.reset()
        
        if pyxel.btn(pyxel.KEY_S):
            self.start()
        self.player.update()
  
  #表示画面ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    def draw(self):
        #背景色
        pyxel.cls(0)
        # プレイ画面
        if self.player.is_alive == True and self.menu == False:
            s = f"SCORE {self.score}"
            pyxel.text(5, 4, s, 1)
            pyxel.text(4, 4, s, 7)

        #player
        if pyxel.btn(pyxel.KEY_LEFT) :
                self.player.w = -player_w
        elif pyxel.btn(pyxel.KEY_RIGHT) :
            self.player.w = player_w
        if self.player.is_alive == True:
            pyxel.blt(self.player.x,self.player.y,0,player_img_x,player_img_y,self.player.w,self.player.h,14)
        #モンスターボール
        for self.monsterball in self.Monsterballs:
            if self.monsterball.is_alive == True:
                pyxel.blt(self.monsterball.x,self.monsterball.y,0,monsterball_img_x,monsterball_img_y,self.monsterball.w,self.monsterball.h,14)
    
        #初期画面
        if self.menu == True :
            pyxel.blt(0,0,1,40,40,256,256)
            x = round(pyxel.frame_count /3)
            pyxel.text(40,5 ,Mainmenu_Message,  x % 6)
        
        #捕獲画面
        elif ((self.menu == False) and
            (self.player.is_alive == False)):
        #ボール揺れなし
            if self.motion1 == True:
                if self.motion_time <catch_time:
                    pyxel.blt(motion1_x,motion1_y,2,motion1_img_x,motion1_img_y,motion1_w,motion1_h,14)
                else:
                    pyxel.blt(escape_x,escape_y,0,escape_img_x,escape_img_y,escape_w,escape_h,14)
                    pyxel.text(40,60 ,revive_Message, 7)
        # ボール揺れ１回   
            elif self.motion2 == True:
                if self.motion_time <catch_time:
                    pyxel.blt(motion1_x,motion1_y,2,motion1_img_x,motion1_img_y,motion1_w,motion1_h,14)
                elif self.motion_time >= catch_time and self.motion_time <catch_time*2:
                    pyxel.blt(motion2_x,motion2_y,2,motion2_img_x,motion2_img_y,motion2_w,motion2_h,14)
                else:
                    pyxel.blt(escape_x,escape_y,0,escape_img_x,escape_img_y,escape_w,escape_h,14)
                    pyxel.text(40,60 ,revive_Message, 7)

        # ボール揺れ2回   
            elif self.motion3 == True:
                if self.motion_time <catch_time:
                    pyxel.blt(motion1_x,motion1_y,2,motion1_img_x,motion1_img_y,motion1_w,motion1_h,14)
                elif self.motion_time >= catch_time and self.motion_time <catch_time*2:
                    pyxel.blt(motion2_x,motion2_y,2,motion2_img_x,motion2_img_y,motion2_w,motion2_h,14)
                elif self.motion_time >= catch_time*2 and self.motion_time <catch_time*3:
                    pyxel.blt(motion3_x,motion3_y,2,motion3_img_x,motion3_img_y,motion3_w,motion3_h,14)
                else:
                    pyxel.blt(escape_x,escape_y,0,escape_img_x,escape_img_y,escape_w,escape_h,14)
                    pyxel.text(40,60 ,revive_Message, 7)
        # 捕獲
            elif self.motion4 == True:
                if self.motion_time <catch_time:
                    pyxel.blt(motion1_x,motion1_y,2,motion1_img_x,motion1_img_y,motion1_w,motion1_h,14)
                elif self.motion_time >= catch_time and self.motion_time <catch_time*2:
                    pyxel.blt(motion2_x,motion2_y,2,motion2_img_x,motion2_img_y,motion2_w,motion2_h,14)
                elif self.motion_time >= catch_time*2 and self.motion_time <catch_time*3:
                    pyxel.blt(motion3_x,motion3_y,2,motion3_img_x,motion3_img_y,motion3_w,motion3_h,14)
                else:
                    pyxel.blt(motion4_x,motion4_y,2,motion4_img_x,motion4_img_y,motion4_w,motion4_h,14)
                    t = f"""
SCORE {self.score} {Gameover_Message}"""
                    pyxel.text(45,78 ,t, 1)    
             
App()