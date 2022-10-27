import pygame,os,sys,random


#初始化
pygame.init()
pygame.mixer.init()

pygame.display.set_caption("火鍋下樓梯")
logo = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","Hotpot.png"))
pygame.display.set_icon(logo)

width = 1024
height = 1024
screen = pygame.display.set_mode((width,height))

clock = pygame.time.Clock()

#color
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,153,18)

#載入
face = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","Face.png")).convert_alpha()
face = pygame.transform.scale(face,(120,140))
background_img = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","Background.png")).convert_alpha()
top_ceil_img = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","Ceiling.png")).convert_alpha()
top_ceil_img = pygame.transform.scale(top_ceil_img,(1034,41))

wall = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","wall.png")).convert_alpha()
wall = pygame.transform.scale(wall,(28.8,1024))

life_bar = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","HpBar.png"))
life_bar = pygame.transform.scale(life_bar,(310,70))

start_img = pygame.transform.scale(logo,(250,183))

fonts_name = os.path.join("火鍋下樓梯DATA","火鍋字體","Pixel.ttf")

#sound
hurt_sound = pygame.mixer.Sound(os.path.join("火鍋下樓梯DATA","火鍋音效","hurt.mp3"))
touch_sound = pygame.mixer.Sound(os.path.join("火鍋下樓梯DATA","火鍋音效","touch_normal.mp3"))
die_sound = pygame.mixer.Sound(os.path.join("火鍋下樓梯DATA","火鍋音效","death.mp3"))
score_sound = pygame.mixer.Sound(os.path.join("火鍋下樓梯DATA","火鍋音效","get.mp3"))

##flr
normal_flr = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","floor","Normal.png")).convert_alpha()
fake_flr = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","floor","Fake.png")).convert_alpha()
nails_flr = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","floor","Nails.png")).convert_alpha()
roll_r = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","floor","ConveyorRight.png")).convert_alpha()
roll_l = pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","floor","ConveyorLeft.png")).convert_alpha()
flr_data = [normal_flr,fake_flr,nails_flr,roll_r,roll_l]

#player
player_anim = {}
player_anim["idle"] = []
player_anim["run"] = []
for i in range(4):
    player_anim["idle"].append(pygame.transform.scale(pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","player_idle",f"idle_{i}.png")).convert_alpha(),(169,155)))
    player_anim["run"].append(pygame.transform.scale(pygame.image.load(os.path.join("火鍋下樓梯DATA","火鍋圖片","player_run",f"run_{i}.png")).convert_alpha(),(169,155)))

#遊戲數值
world_speed = 0
score = 0
life = 10

wall_y = 0

gravity = 5

time=0
hurt_time = 0
start_time = 0
touch_time = 0

#funtion
def draw_text(surf,text,size,x,y,color):
    font=pygame.font.Font(fonts_name,size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)
    return text_rect

def Hpbar():
    health = pygame.Rect(10,45,life*31,70)
    pygame.draw.rect(screen,(255,255,0),health)
    screen.blit(life_bar,(10,45))

def choose_floor():
    return random.choice(flr_data)

def random_rect():
    return random.randint(100,925)

def random_time():
    return random.randint(500,1500)

def life_control():
    global life,hurt_time
    life = int(life)
    if life < 0 :
        life = 0
    if life > 10 :
        life = 10
    if life != 10:
        if (time-hurt_time) // 1000 == 2:
            hurt_time = time
            life += 1 
    if life == 0:
        player = players.sprites()
        player[0].rect.top = height+1000

def Chinese_num_trasfrom(num):
    num = str(num)
    num_date = {"0":"零",
                "1":"一",
                "2":"二",  
                "3":"三",
                "4":"四",
                "5":"五",
                "6":"六",
                "7":"七",
                "8":"八",
                "9":"九"}
    carry_date = ["十","百","千","萬"]

    number = []
    for n in num:
        number.append(n)

    for i in number:
        if len(number) == 1 :
            return num_date[i]
        
        if len(number) == 2:
            if number[1] == "0":
                if i == "1":
                    return carry_date[0]
                elif i != "1":
                    return num_date[i]+carry_date[0]
            else:
                if i == "1":
                    return carry_date[0]+num_date[number[1]]
                return num_date[number[0]]+carry_date[0]+num_date[number[1]]
        
        if len(number) == 3:
            if number[1] == "0" and number[2] == "0":
                return num_date[i]+carry_date[1]
            if number[1] == "0":
                return num_date[i]+carry_date[1]+num_date[number[1]]+num_date[number[2]]
            if number[2] == "0":
                return num_date[i]+carry_date[1]+num_date[number[1]]+carry_date[0]
            return num_date[i]+carry_date[1]+num_date[number[1]]+carry_date[0]+num_date[number[2]]

        if len(number) == 4:
            first_3 = number[1] + number[2] + number[0]
            last_3 = number[1] + number[2] + number[3]
            if first_3 == "000":
                return num_date["0"] + Chinese_num_trasfrom(number[-1])

            if last_3 == "000":
                return num_date[i]+carry_date[2]
            if number[1] == "0" and number[2] == "0":
                return num_date[i]+carry_date[2]+num_date["0"]+num_date[number[3]]
            return num_date[i]+carry_date[2]+Chinese_num_trasfrom(last_3)
        
        if len(number) == 5:
            last_4 = number[1] + number[2] + number[3] + number[4]
            if last_4 == "0000":
                return num_date[i] + carry_date[3]
            return  num_date[i]+carry_date[3]+Chinese_num_trasfrom(last_4)
        
        if len(number) == 6:
            first_2 =number[0] + number[1]
            last_4 = number[2] + number[3] + number[4] + number[5]
            return Chinese_num_trasfrom(first_2)+carry_date[-1]+Chinese_num_trasfrom(last_4)
        
        if len(number) == 7:
            first_3 =number[0] + number[1] +number[2]
            last_4 = number[3] + number[4] + number[5] + number[6]
            return Chinese_num_trasfrom(first_3)+carry_date[-1]+Chinese_num_trasfrom(last_4)
        
        if len(number) == 8:
            first_4 =number[0] + number[1] +number[2] + number[3]
            last_4 =  number[4] + number[5] + number[6] + number[7] 
            return Chinese_num_trasfrom(first_4)+carry_date[-1]+Chinese_num_trasfrom(last_4)

def score_control():
    global start_time,score,world_speed
    if (time - start_time)//1000 == 10:
        start_time = time
        score +=1
        score_sound.play()


#背景
class Background:
    def init():
        screen.fill(BLACK)

    def wall_roll():
        global wall_y
        wall_height = 1024

        #left
        screen.blit(wall,(0,wall_y))
        screen.blit(wall,(0,wall_y + wall_height))
        #right
        screen.blit(wall,(height-28,wall_y))
        screen.blit(wall,(height-28,wall_y + wall_height))

        if wall_y <= -1024:
            screen.blit(wall,(0,wall_height))
            wall_y = 0

        wall_y -= world_speed

    def background():
        screen.blit(top_ceil_img,(0,165))
        Background.wall_roll()

        screen.blit(background_img,(0,0))
        screen.blit(face,(width/2-52,20))
        Hpbar()
        draw_text(screen,"第"+Chinese_num_trasfrom(score)+"層",80,width-200,45,ORANGE)

#按鈕
class Button:
    def __init__(self,x,y,img):
        self.image = img
        self.rect = self.image.get_rect(center =(x,y))
        self.clicked = False

    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))

        pos = pygame.mouse.get_pos() 
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed() [0] ==1 and self.clicked != True:
                self.clicked = True
                touch_sound.play()
                return True
start_btn = Button(width/2,height*3/4,start_img)
REstart_btn = Button(width/2,height*3/4,start_img)

#地板
class Floor(pygame.sprite.Sprite):
    def __init__(self,pos,img):
        super().__init__()
        self.id = img
        self.image = pygame.transform.scale(img,(97*1.5,16*1.5))
        self.rect = self.image.get_rect(midtop = pos)
        self.collide = False
    
    def out(self):
        if self.rect.bottom < 0 :
            self.kill()
    
    def coliidison(self):
        global life,hurt_time,touch_time
        player = players.sprites()
        for sprite in floors.sprites():
            if player[0].rect.top >= 165+41:
                if sprite.rect.colliderect(player[0].bar):
                    if player[0].rect.bottom-20 < sprite.rect.top:
                        player[0].rect.bottom = sprite.rect.top+5
                        if sprite.id == normal_flr:
                            if sprite.collide != True:
                                sprite.collide = True
                                touch_sound.play()
                        
                        if sprite.id == nails_flr:
                            if sprite.collide != True:
                                hurt_sound.play()
                                sprite.collide = True
                                hurt_time = pygame.time.get_ticks()
                                life -= 2
                        if sprite.id == roll_l:
                            if sprite.collide != True:
                                sprite.collide = True
                                touch_sound.play()
                            player[0].rect.x-=0.8
                        if sprite.id == roll_r:
                            if sprite.collide != True:
                                sprite.collide = True
                                touch_sound.play()
                            player[0].rect.x+=1
                        if sprite.id == fake_flr:
                            if sprite.collide != True:
                                touch_time = pygame.time.get_ticks()
                                sprite.collide = True
                                touch_sound.play()
                            if (time - touch_time)//1000 == 1:
                                sprite.kill()
            else:
                life -=2
                hurt_sound.play()
                player[0].rect.top = 165+41+15

    def update(self):
        self.coliidison()
        self.rect.y -= world_speed
        self.out()
        
#player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frame = 0
        self.image = player_anim["idle"][self.frame]
        self.rect = self.image.get_rect( center =(width/2,height/3))
        self.speed = 10
        self.mode = "right"
        self.isalive = True
        self.bar = pygame.Rect(self.rect.x-100,self.rect.y,100,self.image.get_height())

    def anim(self):
        self.frame += 0.05
        if self.frame >= len(player_anim["idle"])-1 :
            self.frame = 0
        self.image = player_anim["idle"][int(self.frame)]
        
    
    def anim_run(self):
        self.frame += 0.1
        self.image = player_anim["run"][int(self.frame)]

    def right_or_left(self):
        if self.mode == "right":
            self.image = pygame.transform.flip(self.image,False,False)
        elif self.mode == "left":
            self.image = pygame.transform.flip(self.image,True,False)



    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.mode = "right"
            self.rect.x += self.speed
            self.anim_run()
        if key[pygame.K_LEFT]:
            self.mode = "left"
            self.rect.x -= self.speed
            self.anim_run()
        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top > height:
            if self.isalive != False:
                self.isalive = False
                global game_mode,world_speed
                game_mode = "over"
                world_speed = 0
                die_sound.play()

    def set_gravity(self):
        self.rect.y += gravity 

    def update(self):
        self.anim()
        self.move()
        self.set_gravity()
        self.right_or_left()
        self.bar = pygame.Rect(self.rect.x+50,self.rect.y,100,self.image.get_height())
        
        pass


#into game
def game_init():
    global floors,players
    floors = pygame.sprite.Group()
    f = Floor((width/2,height),normal_flr)
    floors.add(f)

    players = pygame.sprite.Group()
    p = Player()
    players.add(p)
game_init()

#計時器
spawn_time = pygame.USEREVENT
pygame.time.set_timer(spawn_time,(3000))


#遊戲迴圈
game_mode = "ready"
while True:
    time = pygame.time.get_ticks()
    Background.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_mode == "playing":
            if event.type == spawn_time:
                fe = Floor((random_rect(),height),choose_floor())
                floors.add(fe)
                pygame.time.set_timer(spawn_time,random_time())
    
    if game_mode == "ready":
        screen.blit(pygame.transform.scale(face,(240,280)),(width/2-100,height/4-25))
        title_rect =draw_text(screen,"火鍋 DOWN STAIRS!!",80,width/2,height/2,ORANGE)
        draw_text(screen,"製作 BY.雷克斯",36,width/2,title_rect.bottom,WHITE)
        if start_btn.draw():
            start_time = pygame.time.get_ticks()
            game_mode = "playing"
            world_speed = 1.2
            score = 1
        draw_text(start_img,"START",50,140,100,WHITE)
    if game_mode == "playing":
        life_control()
        score_control()
        floors.draw(screen)
        floors.update()
        players.draw(screen)
        players.update()
    if game_mode == "over":
        floors.draw(screen)
        REstart_btn = Button(width/2,height*3/4,start_img)
        if REstart_btn.draw():
            start_time = pygame.time.get_ticks()
            game_mode = "playing"
            world_speed = 1.2
            score = 1
            floors.empty()
            players.empty()
            life = 10
            game_init()
    
        # draw_text(start_img,"restart",50,140,100,WHITE)


    Background.background()

    clock.tick(60)
    pygame.display.update()