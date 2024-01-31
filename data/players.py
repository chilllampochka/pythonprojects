import sqlalchemy
from sqlalchemy import orm
from .db_sesion import sqlalchemy_base

class Players(sqlalchemy_base):
    __tablename__="players"
    id=sqlalchemy.Column(sqlalchemy.Integer,primary_key=True,autoincrement=True)
    name=sqlalchemy.Column(sqlalchemy.String(200))
    addres=sqlalchemy.Column(sqlalchemy.String(200))
    x=sqlalchemy.Column(sqlalchemy.Integer,default=500)
    y=sqlalchemy.Column(sqlalchemy.Integer,default=500)
    size=sqlalchemy.Column(sqlalchemy.Integer,default=50)
    errors=sqlalchemy.Column(sqlalchemy.Integer,default=0)
    abs_speed=sqlalchemy.Column(sqlalchemy.Integer,default=1)
    speed_x=sqlalchemy.Column(sqlalchemy.Integer,default=0)
    speed_y=sqlalchemy.Column(sqlalchemy.Integer,default=0)
    color=sqlalchemy.Column(sqlalchemy.String(250),default='red')
    w_vision=sqlalchemy.Column(sqlalchemy.Integer,default=800)
    h_vision=sqlalchemy.Column(sqlalchemy.Integer,default=600)
    def __init__(self,name,addr):
        self.name=name
        self.addres=addr
    
    