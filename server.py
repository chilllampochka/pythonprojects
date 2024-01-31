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
        self.x+=self.x_speed
        self.y+=self.y_speed 
     
    def change_speed(self,vektor):
        vektor=list(map(float,vektor.split(",")))
        if vektor[0]==0 and vektor[1]==0:
            self.x_speed=self.y_speed=0
        else:
            vektor=vektor[0]*self.abs_speed,vektor[1]*self.abs_speed
            self.x_speed=vektor[0]
            self.y_speed=vektor[1]         
        
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
        player=Local_Player(data.id,data.name,new_socket,addr)
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
                p1=pairs[i][1]
                p2=pairs[j][1]
                dist_x=p1.x-p2.x
                dist_y=p1.y-p2.y
                
                if
                
    
    for id in list(players):
        try:
            players[id].sock.send("Cъел".encode())
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
        pygame.draw.circle(screen, "yellow", (x, y), size)
        
    for id in players:
        player = players[id]
        players[id].update()
    
    pygame.display.update()           
            
pygame.quit()           
main_socket.close()
session.query(Players).delete()
session.commit()                             
        