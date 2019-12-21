import tkinter as tk
from PIL import Image, ImageTk, ImageOps
from pathlib import Path
import random
from config import *

class App(tk.Tk):
    def __init__(self, screenName=None, baseName=None, className="Tk", useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName,
                         className=className, useTk=useTk, sync=sync, use=use)
        self.geometry("1200x720")
        self.resizable(0, 0)
        self._frame = None
        self.switch(Welcome)

    def switch(self, frame):
        if frame is Welcome:
            new_frame = frame(self,pady = 250)
        else:
            new_frame = frame(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame


class Welcome(tk.Frame):
    def __init__(self, master=None,**kw):
        super().__init__(master=master,**kw)
        tk.Label(self, text="Welcome to 2048!", font=('Arial', 40)).pack()
        tk.Button(self, text="Start!", font=("Arial", 15), justify=tk.CENTER,
                  width=18, height=4, command=lambda: master.switch(Main)).pack()
        self.pack()


class Main(tk.Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        try:
            with open("score.txt") as f:
                self.highscore = int(f.read())
        except FileNotFoundError:
            self.highscore = 0
        self.score = 0
        game_container = tk.Frame(self, height=720, width=720)
        self.all_cells = [[Cell(game_container, row=0, column=0, height=180, width=180), Cell(game_container, row=0, column=1, height=180, width=180), Cell(game_container, row=0, column=2, height=180, width=180), Cell(game_container, row=0, column=3, height=180, width=180)],
                          [Cell(game_container, row=1, column=0, height=180, width=180), Cell(game_container, row=1, column=1, height=180, width=180), Cell(
                              game_container, row=1, column=2, height=180, width=180), Cell(game_container, row=1, column=3, height=180, width=180)],
                          [Cell(game_container, row=2, column=0, height=180, width=180), Cell(game_container, row=2, column=1, height=180, width=180), Cell(
                              game_container, row=2, column=2, height=180, width=180), Cell(game_container, row=2, column=3, height=180, width=180)],
                          [Cell(game_container, row=3, column=0, height=180, width=180), Cell(game_container, row=3, column=1, height=180, width=180), Cell(game_container, row=3, column=2, height=180, width=180), Cell(game_container, row=3, column=3, height=180, width=180)]]
        game_container.grid(row=0, column=0)
        score = tk.Frame(self, height=720, width=720)
        self.points = tk.StringVar()
        self.over = tk.StringVar()
        self.points.set(f"Score: 0\nHighscore:{self.highscore}")
        tk.Label(score, font=("Arial", 20),
                 textvariable=self.points, justify=tk.LEFT).pack()
        tk.Label(score, font=("Arial", 20),
                 textvariable=self.over, justify=tk.LEFT).pack()
        score.grid(row=0, column=1, sticky=tk.N)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<Left>", self.left)
        self.bind("<Right>", self.right)
        self.focus_set()
        self.pack(side=tk.LEFT)
        self.start()

    def start(self):
        used = []
        count = 0
        while True:
            row = random.randint(0, 3)
            column = random.randint(0, 3)
            cell = (row, column)
            if not cell in used:
                used.append(cell)
                self.all_cells[cell[0]][cell[1]].count = 1
                self.all_cells[cell[0]][cell[1]].change_image()
                count += 1
            if count == 2:
                break

    def check(self):
        dead = True
        for y in self.all_cells:
            for x in y:
                if not x.row == 0:
                    if self.all_cells[x.row-1][x.column].count == x.count:
                        dead = False
                if not x.column == 0:
                    if self.all_cells[x.row][x.column-1].count == x.count:
                        dead = False
                if not x.row == 3:
                    if self.all_cells[x.row + 1][x.column].count == x.count:
                        dead = False
                if not x.column == 3:
                    if self.all_cells[x.row][x.column+1].count == x.count:
                        dead = False
                if not dead:
                    break
            if not dead:
                break
        return dead

    def refresh(self):
        for y in self.all_cells:
            for x in y:
                x.merge = False
        while True:
            row = random.randint(0, 3)
            column = random.randint(0, 3)
            cell = (row, column)
            if self.all_cells[cell[0]][cell[1]].count == 0:
                self.all_cells[cell[0]][cell[1]].count = 1
                self.all_cells[cell[0]][cell[1]].change_image()
                break

    def finish(self):
        string = "Game over!\n"
        if self.score == self.highscore:
            string += ("Congratulations you have beaten your high score!")
            with open("score.txt", "w+") as f:
                f.write(str(self.highscore))
        self.over.set(string)

    def add_points(self, count):
        self.score += 2**count
        if self.score > self.highscore:
            self.highscore = self.score
        self.points.set(f"Score:{self.score}\nHighscore:{self.highscore}")

    def go(self, new, old, direction, x, y, z):
        if direction == "+y":
            old.move(old.object, 0, old.y*180)
        elif direction == "-y":
            old.move(old.object, 0, old.y*-180)
        elif direction == "-x":
            old.move(old.object, old.x*-180, 0)
        elif direction == "+x":
            old.move(old.object, old.x*+180, 0)
        new.count = old.count
        new.change_image()
        old.count = 0
        old.change_image()
        old.x = 0
        old.y = 0
        new.x = 0
        new.y = 0

    def up(self, event):
        merge, move = False, False
        for y in range(1, 4):
            for x in range(4):
                merged, moved = False, False
                current = self.all_cells[y][x]
                if current.count == 0:
                    continue
                for z in range(y-1, -1, -1):
                    target = self.all_cells[z][x]
                    if target.count == 0:
                        current.y += 1
                        moved, move = True, True
                    elif target.count == current.count:
                        if target.merge:
                            target = self.all_cells[z+1][x]
                            break
                        current.y += 1
                        current.count += 1
                        self.add_points(current.count)
                        self.go(target, current, "-y", x, y, z)
                        merged, merge,target.merge = True, True, True
                        break
                    else:
                        target = self.all_cells[z+1][x]
                        break
                if not merged and moved:
                    self.go(target, current, "-y", x, y, z)
        if merge or move:
            self.refresh()
        if not merge and not move:
            over, alive = False, False
            for y in self.all_cells:
                for x in y:
                    if x.count == 0:
                        alive = True
                        break
                if alive:
                    break
            if not alive:
                over = True

            if over:
                dead = self.check()
                if dead:
                    self.finish()

    def down(self, event):
        merge, move = False, False
        for y in range(2, -1, -1):
            for x in range(3, -1, -1):
                merged, moved = False, False
                current = self.all_cells[y][x]
                if current.count == 0:
                    continue
                for z in range(y+1, 4):
                    target = self.all_cells[z][x]
                    if target.count == 0:
                        current.y += 1
                        moved, move = True, True
                    elif target.count == current.count:
                        if target.merge:
                            target = self.all_cells[z-1][x]
                            break
                        current.y += 1
                        current.count += 1
                        self.add_points(current.count)
                        self.go(target, current, "+y", x, y, z)
                        merged, merge,target.merge = True, True, True
                        break
                    else:
                        target = self.all_cells[z-1][x]
                        break
                if not merged and moved:
                    self.go(target, current, "+y", x, y, z)
        if merge or move:
            self.refresh()
        if not merge and not move:
            over, alive = False, False
            for y in self.all_cells:
                for x in y:
                    if x.count == 0:
                        alive = True
                        break
                if alive:
                    break
            if not alive:
                over = True

            if over:
                dead = self.check()
                if dead:
                    self.finish()

    def left(self, event):
        merge, move = False, False
        for x in range(1, 4):
            for y in range(4):
                merged, moved = False, False
                current = self.all_cells[y][x]
                if current.count == 0:
                    continue
                for z in range(x-1, -1, -1):
                    target = self.all_cells[y][z]
                    if target.count == 0:
                        current.x += 1
                        moved, move = True, True
                    elif target.count == current.count:
                        if target.merge:
                            target = self.all_cells[y][z+1]
                            break
                        current.x += 1
                        current.count += 1
                        self.add_points(current.count)
                        self.go(target, current, "-x", x, y, z)
                        merged, merge,target.merge = True, True, True
                        break
                    else:
                        target = self.all_cells[y][z+1]
                        break
                if not merged and moved:
                    self.go(target, current, "-x", x, y, z)
        if merge or move:
            self.refresh()
        if not merge and not move:
            over, alive = False, False
            for y in self.all_cells:
                for x in y:
                    if x.count == 0:
                        alive = True
                        break
                if alive:
                    break
            if not alive:
                over = True
            if over:
                dead = self.check()
                if dead:
                    self.finish()

    def right(self, event):
        merge, move = False, False
        for x in range(2, -1, -1):
            for y in range(3, -1, -1):
                merged, moved = False, False
                current = self.all_cells[y][x]
                if current.count == 0:
                    continue
                for z in range(x+1, 4):
                    target = self.all_cells[y][z]
                    if target.count == 0:
                        current.x += 1
                        moved, move = True, True
                    elif target.count == current.count:
                        if target.merge:
                            target = self.all_cells[y][z-1]
                            break
                        current.x += 1
                        current.count += 1
                        self.add_points(current.count)
                        self.go(target, current, "+x", x, y, z)
                        merged, merge = True, True
                        break
                    else:
                        target = self.all_cells[y][z-1]
                        break
                if not merged and moved:
                    self.go(target, current, "+x", x, y, z)
        if merge or move:
            self.refresh()
        if not merge and not move:
            over, alive = False, False
            for y in self.all_cells:
                for x in y:
                    if x.count == 0:
                        alive = True
                        break
                if alive:
                    break
            if not alive:
                over = True
            if over:
                dead = self.check()
                if dead:
                    self.finish()


class Cell(tk.Canvas):
    def __init__(self, master=None, row=0, column=0, count=0, **kw):
        super().__init__(master=master, **kw)
        self.gone = False
        self.merge = False
        self.row = row
        self.column = column
        self.y = 0
        self.x = 0
        self.count = count
        self.image = Image.open(
            f"{str(Path(__file__).absolute()).strip('main.py')}picture/{theme}/{picture[self.count]}")
        resized = self.image.resize((180, 180))
        # self.picture = tk.PhotoImage(self.image,master=self)
        self.picture = ImageTk.PhotoImage(resized)
        self.create_image(0, 0, image=self.picture, anchor=tk.NW, tag="img")
        self.grid(row=self.row, column=self.column)

    def change_image(self):
        self.delete("all")
        self.image = Image.open(
            f"{str(Path(__file__).absolute()).strip('main.py')}picture/{theme}/{picture[self.count]}")
        resized = self.image.resize((180, 180))
        self.picture = ImageTk.PhotoImage(resized)
        self.object = self.create_image(0, 0, image=self.picture, anchor=tk.NW)


if __name__ == "__main__":
    themes = ["Classical","Aqours","Mayday","Pokemon"]
    if not theme in themes:
        print("The chosen theme in config.py is invalid! Please choose from Classical, Aqours, Mayday or Pokemon!")
        SystemExit(0)
    if not Dark == True or not Dark == False:
        Dark = False 
    picture = ["0.png", "2.png", "4.png", "8.png", "16.png", "32.png", "64.png",
               "128.png", "256.png", "512.png", "1024.png", "2048.png", "4096.png", "8192.png"]
    game = App()
    game.mainloop()
