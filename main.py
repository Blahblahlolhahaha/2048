import tkinter as tk
from PIL import Image,ImageTk,ImageOps
from pathlib import Path
import random

class App(tk.Tk):
    def __init__(self, screenName=None, baseName=None, className="Tk", useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName, className=className, useTk=useTk, sync=sync, use=use)
        self.geometry("1200x720")
        self._frame = None
        self.switch(Welcome)
    def switch(self,frame):
        new_frame  = frame(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame

class Welcome(tk.Frame):
    def __init__(self,master=None):
        super().__init__()
        self.height = 600
        self.width = 600
        tk.Label(self,text="Welcome to 2048!",font=('Arial',40)).pack()
        tk.Button(self,text="Start!",font=("Arial",15),justify=tk.CENTER,width=18,height=4,command=lambda:master.switch(Main)).pack()
        self.pack()

class Main(tk.Frame):
    def __init__(self, master=None,**kw):
        super().__init__(master=master,**kw)
        game_container = tk.Frame(self,height=720,width=720,bg="#777777")
        self.all_cells = [[Cell(game_container,row=0,column=0,height=180,width=180),Cell(game_container,row=0,column=1,height=180,width=180),Cell(game_container,row=0,column=2,height=180,width=180),Cell(game_container,row=0,column=3,height=180,width=180)],
                          [Cell(game_container,row=1,column=0,height=180,width=180),Cell(game_container,row=1,column=1,height=180,width=180),Cell(game_container,row=1,column=2,height=180,width=180),Cell(game_container,row=1,column=3,height=180,width=180)],
                          [Cell(game_container,row=2,column=0,height=180,width=180),Cell(game_container,row=2,column=1,height=180,width=180),Cell(game_container,row=2,column=2,height=180,width=180),Cell(game_container,row=2,column=3,height=180,width=180)],
                          [Cell(game_container,row=3,column=0,height=180,width=180),Cell(game_container,row=3,column=1,height=180,width=180),Cell(game_container,row=3,column=2,height=180,width=180),Cell(game_container,row=3,column=3,height=180,width=180)]]
        game_container.pack()
        self.bind("<Up>",self.up)
        self.bind("<Down>",self.down)
        self.bind("<Left>",self.left)
        self.bind("<Right>",self.right)
        self.focus_set()
        self.pack(side=tk.LEFT)
        self.start()
        
    def start(self):
        used = []
        count = 0
        while True:
            row = random.randint(0,3)
            column = random.randint(0,3)
            cell = (row,column)
            if not cell in used:
                used.append(cell)
                self.all_cells[cell[0]][cell[1]].count = 1
                self.all_cells[cell[0]][cell[1]].change_image()
                count += 1
            if count == 2:
                break

    def check(self):
        print("gg.com")
    
    def refresh(self):
        while True:
            row = random.randint(0,3)
            column = random.randint(0,3)
            cell = (row,column)
            if self.all_cells[cell[0]][cell[1]].count == 0:
                self.all_cells[cell[0]][cell[1]].count = 1
                self.all_cells[cell[0]][cell[1]].change_image()
                break

    def merge(self,new,old,direction,x,y,z):
        if direction == "+y":
            old.move(old.object,0,old.y*180)
            new.count= new.count + 1
            new.change_image()
            old.count = 0
            old.change_image()
        elif direction == "-y":
            old.move(old.object,0,old.y*-180)
            new.count= new.count + 1
            new.change_image()
            old.count = 0
            old.change_image()    
        elif direction == "-x":
            old.move(old.object,old.x*-180,0)
            new.count= new.count + 1
            new.change_image()
            old.count = 0
            old.change_image() 
        elif direction == "+x":
            old.move(old.object,old.x*+180,0)
            new.count= new.count + 1
            new.change_image()
            old.count = 0
            old.change_image() 
        old.x = 0
        old.y = 0
        new.x = 0
        new.y = 0

    def up(self,event):
        merge,move=False,False
        for y in range(1,4):
            for x in range(4):
                merged,moved = False,False
                current = self.all_cells[y][x]
                if current.count == 0:
                    continue
                for z in range(y-1,-1,-1):
                    target = self.all_cells[z][x]
                    if target.count == 0:
                        current.y += 1
                        moved,move = True,True
                    elif target.count == current.count:
                        current.y += 1
                        self.merge(target,current,"-y",x,y,z)
                        merged,merge = True,True
                        break
                    else:
                        target = self.all_cells[z+1][x]
                        break
                if not merged and moved:
                    current.move(current.object,0,current.y*-180)
                    target.count=current.count
                    target.change_image()
                    current.count = 0
                    current.change_image()
                    current.y = 0
                    target.y = 0
        if merge or move:
            self.refresh()

    def down(self,event):
        merge,move = False,False
        for y in range(2,-1,-1):
            for x in range(3,-1,-1):
                merged,moved = False,False
                current = self.all_cells[y][x]
                if current.count == 0:
                    continue
                for z in range(y+1,4):
                    target = self.all_cells[z][x]
                    if target.count == 0:
                        current.y += 1
                        moved,move = True,True
                    elif target.count == current.count:
                        current.y += 1
                        self.merge(target,current,"+y",x,y,z)
                        merged,merge = True,True
                        break
                    else:
                        target = self.all_cells[z-1][x]
                        break
                if not merged and moved:                       
                    current.move(current.object,0,current.y*180)
                    target.count=current.count
                    target.change_image()
                    current.count = 0
                    current.change_image()
                    current.y = 0
                    target.y = 0
        if merge or move:
            self.refresh()
                    
                    

    def left(self,event):
        merge, move = False,False
        for x in range(1,4):
            for y in range(4):
                merged,moved = False,False
                current = self.all_cells[y][x]
                if current.count == 0:
                    continue
                for z in range(x-1,-1,-1):
                    target = self.all_cells[y][z]
                    if target.count == 0:
                        current.x += 1
                        moved,move = True,True
                    elif target.count == current.count:
                        current.x += 1
                        self.merge(target,current,"-x",x,y,z)
                        merged,merge = True,True
                        break
                    else:
                        target = self.all_cells[y][z+1]
                        break
                if not merged and moved:
                    current.move(current.object,current.x*-180,0)
                    target.count=current.count
                    target.change_image()
                    current.count = 0
                    current.change_image()
                    target.x = 0
                    current.x = 0
        if merge or move:
            self.refresh()

    def right(self,event):
        merge,move=False,False
        for x in range(2,-1,-1):
            for y in range(3,-1,-1):
                merged,moved = False,False
                current = self.all_cells[y][x]
                if current.count == 0:
                    continue
                for z in range(x+1,4):
                    target = self.all_cells[y][z]
                    if target.count == 0:
                        current.x += 1
                        moved,move = True,True
                    elif target.count == current.count:
                        current.x += 1
                        self.merge(target,current,"+x",x,y,z)
                        merged,merge = True,True
                        break
                    else:
                        target = self.all_cells[y][z-1]
                        break
                if not merged and moved:
                    current.move(current.object,current.x*180,0)
                    target.count=current.count
                    target.change_image()
                    current.count = 0
                    current.change_image()
                    current.x = 0
                    target.x = 0
        if merge or move:
            self.refresh()
        
class Cell(tk.Canvas):
    def __init__(self, master=None,row=0,column=0,count=0,**kw):
        super().__init__(master=master,**kw)
        self.gone = False
        self.row = row
        self.column = column
        self.y = 0
        self.x = 0
        self.count = count
        self.image = Image.open(f"{str(Path(__file__).absolute()).strip('main.py')}picture/{picture[self.count]}")
        resized = self.image.resize((180,180))
        # self.picture = tk.PhotoImage(self.image,master=self)
        self.picture = ImageTk.PhotoImage(resized)
        self.create_image(0,0,image=self.picture,anchor=tk.NW,tag="img")
        self.grid(row = self.row,column=self.column)
    
    def change_image(self):
        self.delete("all")
        self.image = Image.open(f"{str(Path(__file__).absolute()).strip('main.py')}picture/{picture[self.count]}")
        resized = self.image.resize((180,180))
        self.picture = ImageTk.PhotoImage(resized)
        self.object = self.create_image(0,0,image=self.picture,anchor=tk.NW)       

if __name__ == "__main__":
    picture = ["0.png","2.png","4.png","8.png","16.png","32.png","64.png","128.png","256.png","512.png","1024.png","2048.png","4096.png","8192.png"]
    game = App()
    game.mainloop()