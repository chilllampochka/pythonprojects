import socket
import time
import pygame
import math
import tkinter

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
sock.connect(("localhost",10000))

radius = 50
pygame.init()
width=800
height=600
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Agario")
run=True

CC=(width//2,height//2)           
radius=50
old=(0,0)

while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    if pygame.mouse.get_focused():
        pos=pygame.mouse.get_pos()
        vektor=pos[0]-CC[0],pos[1]-CC[1]
        lenv=math.sqrt(vektor[0]**2+vektor[1]**2)
        vektor=vektor[0]/lenv,vektor[1]/lenv 
        if lenv<=radius:
            vektor=0,0
        if vektor!=old:
            old=vektor
            sock.send(f"{vektor[0]},{vektor[1]}".encode()) 
    data=sock.recv(1024).decode()
    print(f"Получил {data}")
    screen.fill('gray')
    pygame.draw.circle(screen, (255, 0, 0), CC, radius)
    pygame.display.update()

pygame.quit()    
    