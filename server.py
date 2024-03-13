import socket
import time
import pygame
from data.players import Players
from data import db_sesion
db_sesion.global_init("db.sqlite")
session=db_sesion.create_session()

main_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
main_socket.bind(("localhost",10000))
main_socket.setblocking(False)
main_socket.listen(5)

pygame.init()
WIDTH_ROOM,HEIGHT_ROOM=4000,4000
WIDTH_SERVER,HEIGHT_SERVER=300,300
FPS=100

screen=pygame.display.set_mode((WIDTH_SERVER,HEIGHT_SERVER))
pygame.display.set_caption("Agario")
clock=pygame.time.Clock()

class Local_Player:
    def __init__(self,id,name,sock,addr):
        self.id=id
        self.db:Players=session.get(Players,self.id)
        self.sock=sock
        self.addres=addr
        self.name=name
        self.x=500
        self.y=500
        self.size=50
        self.errors=0
        self.abs_speed=1
        self.x_speed=0
        self.y_speed=0
        self.color='red'
        self.w_vision=800
        self.h_vision=600
        
    def update(self):
        if self.x-self.size<=0:
            if self.speed_x>=0:
                self.x+=self.x_speed
        elif self.x+self.size>=WIDTH_ROOM:
            if self.speed_x<=0:
                self.x+=self.x_speed
        else:
            self.x+=self.x_speed
            
        if self.y-self.size<=0:
            if self.speed_y>=0:
                self.y+=self.y_speed
        elif self.y+self.size>=HEIGHT_ROOM:
            if self.speed_y<=0:
                self.y+=self.y_speed
        else:
            self.y+=self.y_speed
        
     
    def change_speed(self,vektor):
        vektor=list(map(float,vektor.split(",")))
        if vektor[0]==0 and vektor[1]==0:
            self.x_speed=self.y_speed=0
        else:
            vektor=vektor[0]*self.abs_speed,vektor[1]*self.abs_speed
            self.x_speed=vektor[0]
            self.y_speed=vektor[1]
            
    def load(self):
        self.size = self.db.size
        self.abs_speed = self.db.abs_speed
        self.speed_x = self.db.speed_x
        self.speed_y = self.db.speed_y
        self.errors = self.db.errors
        self.x = self.db.x
        self.y = self.db.y
        self.color = self.db.color
        self.w_vision = self.db.w_vision
        self.h_vision = self.db.h_vision
        return self
    
    def sync(self):
        self.db.size = self.size
        self.db.abs_speed = self.abs_speed
        self.db.speed_x = self.speed_x
        self.db.speed_y = self.speed_y
        self.db.errors = self.errors
        self.db.x = self.x
        self.db.y = self.y
        self.db.color = self.color
        self.db.w_vision = self.w_vision
        self.db.h_vision = self.h_vision
        session.merge(self.db)
        session.commit()

         
        
players={}

run=True
while run:
    clock.tick(FPS) 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    try:
        new_socket,addr=main_socket.accept()
        print(f"Подключился {addr}")
        new_socket.setblocking(False)
        login=new_socket.recv(1024).decode()
        login=login.split(',')
        addr=f"({addr[0]},{addr[1]})"
        player=Players("abc",addr)
        player.name, player.color=login
        session.merge(player)
        session.commit()
        data=session.query(Players).filter(Players.addres==addr).first()
        player=Local_Player(data.id,data.name,new_socket,addr).load()
        players[data.id]=player
    except BlockingIOError:
        pass 
        
    for id in list(players):
        try:
            data=players[id].sock.recv(1024).decode()
            players[id].change_speed(data)
        except:
            pass  
    
    #видимость игроков
    visible_bacteries={}
    for id in list(players):
        visible_bacteries[id]=[]
        pairs=list(players.items())
        for i in range(len(pairs)):
            for j in range(i+1, len(pairs)):
                p_1=pairs[i][1]
                p_2=pairs[j][1]
                dist_x=p_1.x-p_2.x
                dist_y=p_1.y-p_2.y
                
                if abs(dist_x) <= p_1.w_vision // 2 + p_2.size and abs(dist_y) <= p_1.h_vision // 2 + p_2.size:
                    distance=math.sqrt(dist_x**2+dist_y**2)
                    if distance<=p_1.size and p_1.size>p_2.size*1.1:
                        p_1.size=math.sqrt(p_1.size**2+p_2.size**2)
                        p_2.size,p_2.speed_x,p_2.speed_y=0,0,0    
                    if p_1.addres is not None:
                        data=f"{round(dist_x)} {round(dist_y)} {round(p_2.size)} {p_2.color}"
                        visibale_bacteries[p_1.id].append(data)
                if abs(dist_x) <= p_2.w_vision // 2 + p_1.size and abs(dist_y) <= p_2.h_vision // 2 + p_1.size:
                    distance=math.sqrt(dist_x**2+dist_y**2)
                    if distance<=p_2.size and p_2.size>p_1.size*1.1:
                        p_2.size=math.sqrt(p_2.size**2+p_1.size**2)
                        p_1.size,p_1.speed_x,p_1.speed_y=0,0,0 
                    if p_2.addres is not None:
                        data=f"{round(-dist_x)} {round(-dist_y)} {round(p_1.size)} {p_1.color}"
                        visibale_bacteries[p_2.id].append(data)

    #создаем ответ
    for id in list(players):
        visible_bacteries[id]=','.join(visible_bacteries[id])+'$'
                    
    for id in list(players):
        try:
            players[id].sock.send(visible_bacteries[id].encode())
        except:
            players[id].sock.close()
            del players[id]
            session.query(Players).filter(Players.id==id).delete()
            session.commit()
            print("Пользователь отключен")
            
    screen.fill('black') 
    for id in players:
        player = players[id]
        x = player.x * WIDTH_SERVER // WIDTH_ROOM
        y = player.y * HEIGHT_SERVER // HEIGHT_ROOM
        size = player.size * WIDTH_SERVER // WIDTH_ROOM
        pygame.draw.circle(screen, player.color, (x, y), size)
        
    for id in players:
        player = players[id]
        players[id].update()
    
    pygame.display.update()           
            
pygame.quit()           
main_socket.close()
session.query(Players).delete()
session.commit()                             
        