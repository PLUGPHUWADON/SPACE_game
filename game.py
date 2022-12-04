import pgzrun
import random

# ทำภาพพื้นหลัง เคลื่อนที่จาก ขวาไปซ้าย
speed = 0
def background():
    global speed
    speed += 2
    screen.blit('space2', (0 - speed, 0))
    screen.blit('space2', (WIDTH - speed, 0))
    if speed > WIDTH:
        speed = 0

# random ก้อนหิน ออกมาจากด้านขวาของจอ
stone = [] 
stone_spawn = 0
def stone_random():
    global stone_spawn
    screen.draw.text("Score: " + str(player.score),(10, 10),color="white",fontsize=30)
    screen.draw.text("Highscore: " + str(player.highscore),(660, 10),color="white",fontsize=30)
    stone_spawn += 3
    if stone_spawn >= 1:
        stone.append(Actor('stone1', (WIDTH + 160, random.randint(0,HEIGHT))))
        stone_spawn -= random.randint(30,50)

    # ทำให้ก้อนหิน เคลื่่อนจากขวาไปซ้าย และ ตรวจสอบการชนของผู้เล่นกับก้อนหิน
    for i in stone:
        i.x -= 8
        i.draw()
        if i.colliderect(player):
            player.dead = True
        if player.dead == True:
            stone.clear()
            bullet.clear()
            
        # ตรวจสอบการชนของลูกกระสุนกับก้อนหิน แล้วทำการลบ
        try:
            for Bullet in bullet:
                if Bullet.colliderect(i):
                    sounds.boom1.play()
                    stone.remove(i)
                    bullet.remove(Bullet)
                    player.score += 1

                    # ตรวจสอบการเพิ่มขึ้นของ score เมือ มากกว่า highscore จะบวกหนึ่งให้ highscore
                    if player.score > player.highscore:
                        player.highscore += 1
        except:
            stone.append(Actor('stone', (WIDTH + 160, random.randint(0,HEIGHT))))

    # ทำให้กระสุน เคลื่อนที่่
    for Bullet in bullet:
        Bullet.x += 10
        Bullet.draw()

# แสดงโลโก้เกมเมื่อรันโปรแกรม
def game_start():
    if player.start == False:
        screen.draw.text("Score: " + str(player.score),(10, 10),color="black",fontsize=30)
        screen.draw.text("Highscore: " + str(player.highscore),(660, 10),color="black",fontsize=30)
        screen.blit("logo1",(180,100))
        screen.draw.text("START",center = (WIDTH/2,350),fontsize = 30)
        player.pos = (WIDTH/2,HEIGHT + 500)
        stone.clear()
                
# แสดงหน้า game over เมื่อผู้เล่นตาย
def game_over():
    if player.dead == True:
      screen.blit("space2",(0,0)) 
      screen.draw.text("Score: " + str(player.score),(10, 10),color="white",fontsize=30)
      screen.draw.text("Highscore: " + str(player.highscore),(660, 10),color="white",fontsize=30)
      screen.draw.text("GAME OVER",center = (WIDTH/2,HEIGHT/2),fontsize = 40) 

# วาดยานอวกาศ
def draw():
    player.draw()
    

# ทุกฟังก์ชันทำงานที่ def update()
def update():
    background()
    stone_random()
    game_start()
    game_over()

def on_mouse_move(pos):
    # ตรวจสอบเมื่อผู้เล่นยังไม่ตาย จะบังคับยานอวกาศได้
    if player.dead == False:
        player.pos = pos
    # ตรวจสอบเมื่อผู้เล่นตาย จะย้ายยานอวกาศของผู้เล่นให้ไปอยู่นอกจอ
    elif player.dead == True:
        player.pos = (WIDTH/2,HEIGHT + 100)

bullet = []
def on_mouse_down(pos,button):
    # ตรวจสอบการคลิกเมื่อคลิกจะเพิ่มกระสุนใน bullet ถ้ารันโปรแกรมคลั้งแรกจะเป็นการคลิกเพื่อเริ่่มเกมด้วย 
    if button == mouse.LEFT:
        player.start = True
        bullet.append(Actor('bullet', (player.x, player.y)))
        last = len(bullet)
        bullet[last - 1].pos = player.pos
        sounds.bullet.play()

    # ตรวจสอบการคลิกเมื่อผู้เล่นอยู่หน้า game over score จะถูกกำหนด = 0 และเกมจะเริ่มอีกครั้ง
    if player.dead == True:
        if button == mouse.LEFT:
            player.dead = False
            player.score = 0

TITLE = "SPACESHIP"
WIDTH = 810
HEIGHT = 450
speed = int(WIDTH/2)
player = Actor("player1")
player.pos = (0,HEIGHT/2)
player.score = 0
player.highscore = 0
player.dead = False
player.start = False
music.play("music")

pgzrun.go()
