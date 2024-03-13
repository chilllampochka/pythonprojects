import socket
import time
import pygame
import math
import tkinter
from tkinter import ttk
import tkinter.messagebox

def scroll(e):
    global color
    color=combo.get()
    style.configure('TCombobox', fieldbackground=color, background="white")
    
def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tkinter.messagebox.showerror("Ошибка", "Ты не выбрал цвет или не ввёл имя!")

def draw_bacteries(data: list[str]):
    for num, bact in enumerate(data):
        data = bact.split(" ")  # Разбиваем по пробелам подстроку одной бактерии
        x = CC[0] + int(data[0])
        y = CC[1] + int(data[1])
        size = int(data[2])
        color = data[3]
        pygame.draw.circle(screen, color, (x, y), size)

    
name=''
color=''
root=tkinter.Tk()
root.title('Вход')
root.geometry('200x200')
style=ttk.Style()
style.theme_use('classic')
name_label=tkinter.Label(root, text='Введите имя')
name_label.pack()
row=tkinter.Entry(root, width=40)
row.pack()
color_label=tkinter.Label(root, text='Выберите цвет')
color_label.pack()

colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown', 'DarkOrange',
 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow', 'Chartreuse', 'LawnGreen', 'Green', 
 'Lime', 'Lime Green', 'SpringGreen', 'MediumSpringGreen', 'Turquoise', 'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 
 'Cyan', 'Dark Turquoise', 'DeepSkyBlue', 'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

combo=ttk.Combobox(root, values=colors, textvariable=color)
combo.bind('<<ComboboxSelected>>', scroll)
combo.pack()
btn=tkinter.Button(root, text='Зайти в игру', command=login)
btn.pack()

root.mainloop()

radius = 50
pygame.init()
width=800
height=600
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Agario")
run=True

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
sock.connect(("localhost",10000))

sock.send(f'{name},{color}'.encode())

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
    data=sock.recv(1024).decode().replace('$', '')
    data=data.split(',')
    screen.fill('gray')
    pygame.draw.circle(screen, color, CC, radius)
    if data!=['']:
        draw_bacteries(data)
    pygame.display.update()

pygame.quit()    
    