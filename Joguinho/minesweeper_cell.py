from tkinter import Button, Label
import utils
import settings
import random


class Cell:
    all_cells = []
    mines_list = []
    remaining_mines = settings.NUMBER_OF_MINES
    cell_mines_count = None
    reset_button = None
    happy_img = None
    sad_img = None
    flag_img = None
    empty_img = None
    mine_img = None
    heart_img = None

    def __init__(self,location , x, y, is_mine):
        self.x = x
        self.y = y
        self.location = location
        self.create_button(self.location, settings.BUTTON_SIDE, settings.BUTTON_SIDE)
        self.is_mine = is_mine
        self.is_revealed = False
        self.is_flagged = False

        Cell.all_cells.append(self)
    
    def create_button(self, location, width, height):
        btn = Button(
            location,
            image=Cell.empty_img,
            bg=utils._from_rgb(169,169,169),
            width=width,
            height=height,
            compound="c",
            text="",
            font = ('Sans','12','bold'),
            padx=0,
            pady=0
        )
        btn.grid(row=self.y, column=self.x)
        btn.bind('<Button-1>', self.reveal)
        btn.bind('<Button-3>', self.flag)

        self.cell_btn_obj = btn

    def reveal(self, event):
        if self.is_revealed or self.is_flagged:
            return
        self.is_revealed = True
        if self.is_mine:
            self.show_mine()
        else:
            self.show_cell()

    def show_cell(self):
        count = 0
        self.cell_btn_obj.config(bg=utils._from_rgb(211,211,211))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x = self.x + i
                y = self.y + j
                if x < 0 or x >= settings.GRID_SIZE_W or y < 0 or y >= settings.GRID_SIZE_H:
                    continue
                cell = Cell.get_cell_by_axis(x, y)
                if cell and cell.is_mine:
                    count += 1
        if count == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    x = self.x + i
                    y = self.y + j
                    if x < 0 or x >= settings.GRID_SIZE_W or y < 0 or y >= settings.GRID_SIZE_H:
                        continue
                    cell = Cell.get_cell_by_axis(x, y)
                    if cell and not cell.is_revealed:
                        cell.reveal(None)
            return
        self.cell_btn_obj.config(text=f"{count}")
        match count:
            case 1:
                self.cell_btn_obj.config(fg=utils._from_rgb(0,0,255))
            case 2:
                self.cell_btn_obj.config(fg=utils._from_rgb(0,128,0))
            case 3:
                self.cell_btn_obj.config(fg=utils._from_rgb(255,0,0))
            case 4:
                self.cell_btn_obj.config(fg=utils._from_rgb(0,0,128))
            case 5:
                self.cell_btn_obj.config(fg=utils._from_rgb(128,0,0))
            case 6:
                self.cell_btn_obj.config(fg=utils._from_rgb(0,128,128))
            case 7:
                self.cell_btn_obj.config(fg=utils._from_rgb(0,0,0))
            case 8:
                self.cell_btn_obj.config(fg=utils._from_rgb(128,128,128))
            case _:
                self.cell_btn_obj.config(fg=utils._from_rgb(0,0,0))


    def show_mine(self):
        self.cell_btn_obj.config(bg=utils._from_rgb(210,43,43))
        self.cell_btn_obj.config(image=Cell.mine_img)
        for cell in Cell.mines_list:
            cell.cell_btn_obj.config(image=Cell.mine_img)

        for cell in Cell.all_cells:
            cell.cell_btn_obj.unbind('<Button-1>')
            cell.cell_btn_obj.unbind('<Button-3>')
        
        utils.change_face(Cell.reset_button, Cell.sad_img)
        

    def flag(self, event):
        if self.is_revealed:
            return
        if not self.is_flagged and Cell.remaining_mines >0:
            self.cell_btn_obj.config(image=Cell.flag_img)
            self.is_flagged = True
            Cell.remaining_mines -= 1
        elif self.is_flagged:
            self.cell_btn_obj.config(image=Cell.empty_img)
            self.is_flagged = False
            Cell.remaining_mines += 1
        Cell.cell_mines_count.config(text=f"{Cell.remaining_mines}")
        if Cell.remaining_mines == 0:
            Cell.check_win()

    @staticmethod
    def check_win():
        for cell in Cell.mines_list:
            if not cell.is_flagged:
                return
        for cell in Cell.all_cells:
            cell.cell_btn_obj.unbind('<Button-1>')
            cell.cell_btn_obj.unbind('<Button-3>')
        utils.change_face(Cell.reset_button, Cell.heart_img)

    @staticmethod
    def create_mine_count_label(location):
        label = Label(
            location,
            text=f"{Cell.remaining_mines}",
            font = ('ds-digital','30','bold'),
            bg=utils._from_rgb(0,0,0),
            fg=utils._from_rgb(210,43,43)
        )
        Cell.cell_mines_count = label

    @staticmethod
    def get_cell_by_axis(x, y):
        for cell in Cell.all_cells:
            if cell.x == x and cell.y == y:
                return cell
        return None

    @staticmethod
    def randomize_mines():
        Cell.mines_list = random.sample(Cell.all_cells, settings.NUMBER_OF_MINES)
        for cell in Cell.mines_list:
            cell.is_mine = True
    
    @staticmethod
    def reset(event):
        for cell in Cell.all_cells:
            cell.cell_btn_obj.config(image=Cell.empty_img)
            cell.cell_btn_obj.config(bg=utils._from_rgb(169,169,169))
            cell.cell_btn_obj.config(text="")
            cell.cell_btn_obj.bind('<Button-1>', cell.reveal)
            cell.cell_btn_obj.bind('<Button-3>', cell.flag)
            cell.is_mine = False
            cell.is_revealed = False
            cell.is_flagged = False
            Cell.remaining_mines = settings.NUMBER_OF_MINES
            Cell.cell_mines_count.config(text=f"{Cell.remaining_mines}")
        Cell.randomize_mines()
        utils.change_face(Cell.reset_button, Cell.happy_img)

    def __repr__(self):
        return f"Cell at ({self.x}, {self.y})"
    
    