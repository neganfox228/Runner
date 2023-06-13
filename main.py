import tkinter as tk
import random
import time

# Создаем окно и задаем его параметры
window = tk.Tk()
window.title("Раннер")
window.geometry("500x500")
window.resizable(0,0)
x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2.8
y = (window.winfo_screenheight() - window.winfo_reqheight()) / 5
window.wm_geometry("+%d+%d" % (x, y))

# Создаем холст для рисования
canvas = tk.Canvas(window, width=500, height=500)
#canvas.config(bg="grey")
canvas.pack()

# Создаем класс для игрока
class Player:
    def __init__(self):
        self.x = 230
        self.y = 250
        self.width = 40
        self.height = 60
        self.rect = canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="blue")

        # Состояние движения
        self.dx, self.dy = 0, 0

    # Обновление положения игрока
    def update(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0:
            self.x = 0
        elif self.x > 460:
            self.x = 460
        if self.y < 0:
            self.y = 0
        elif self.y > 440:
            self.y = 440
        canvas.coords(self.rect, self.x, self.y, self.x + self.width, self.y + self.height)

    # Проверка столкновения игрока с другим объектом
    def collide(self, other):
        x1, y1, x2, y2 = canvas.coords(self.rect)
        ox1, oy1, ox2, oy2 = other.get_coords()
        return (x1 < ox2 and x2 > ox1) and (y1 < oy2 and y2 > oy1)

# Создаем класс для препятствий
class Obstacle:
    def __init__(self):
        global y
        self.x = random.randint(0, 460)
        self.y = random.randint(-200, 0) # Изменяем начальную позицию по оси y
        self.width = 40
        self.height = 20
        self.rect = canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="red")

    # Обновление положения препятствия
    def update(self):
        self.y += 5 #Скорочть обновления препядствий
        canvas.coords(self.rect, self.x, self.y, self.x + self.width, self.y + self.height)

    # Получение координат объекта
    def get_coords(self):
        return canvas.coords(self.rect)

# Создаем игрока и список препятствий
player = Player()
obstacles = []

# Функция для обновления игры
def update_game():
    global player, obstacles, update_id, start_time,obstacle,last_time

    # Добавляем бинд на клавишу "R"
    window.bind("<Key>", restart_game)

    # Обновляем игрока
    player.update()

    # Проверяем столкновение игрока с препятствием
    for obstacle in obstacles:
        if player.collide(obstacle):
            last_time = time.time() - start_time
            bg_rect = canvas.create_rectangle(130, 210, 405, 290, fill="gray")
            gameover_text = canvas.create_text(250, 250, text='''               Вы проиграли! 
            Время: {:.2f} секунд. 
    Нажмите R для новой игры'''.format(last_time), font=("Arial", 15,), tag="game_over")
            canvas.itemconfig(gameover_text, fill="Red")
            window.unbind_all("<Key>") # Отменяем бинды на клавиши
            back_button.config(state='normal')
            return

    # Обновляем каждое препятствие
    for obstacle in obstacles:
        obstacle.update()

    # Удаляем препятствия, которые вышли за пределы экрана
    obstacles = [obstacle for obstacle in obstacles if obstacle.y < 500]

    # Добавляем новое препятствие каждые 50 кадров
    if len(obstacles) // 5 == 0:
        for i in range(4):
            obstacles.append(Obstacle())

    # Обновляем время
    canvas.itemconfig(timer_text, text="Время: {:.2f}".format(time.time() - start_time))

    # Запускаем функцию обновления через 10 миллисекунд
    update_id = window. after(10, update_game)

# Функции для управления игроком
def move_up(event):
    player.dy = -5

def stop_move_up(event):
    if player.dy < 0:
        player.last_dy = player.dy
        player.dy = 0

def move_down(event):
    player.dy = 5

def stop_move_down(event):
    if player.dy > 0:
        player.last_dy = player.dy
        player.dy = 0

def move_left(event):
    player.dx = -5

def stop_move_left(event):
    if player.dx < 0:
        player.last_dx = player.dx
        player.dx = 0

def move_right(event):
    player.dx = 5

def stop_move_right(event):
    if player.dx > 0:
        player.last_dx = player.dx
        player.dx = 0

window.bind("<KeyPress-w>", move_up)
window.bind("<KeyRelease-w>", stop_move_up)
window.bind("<KeyPress-s>", move_down)
window.bind("<KeyRelease-s>", stop_move_down)
window.bind("<KeyPress-a>", move_left)
window.bind("<KeyRelease-a>", stop_move_left)
window.bind("<KeyPress-d>", move_right)
window.bind("<KeyRelease-d>", stop_move_right)

def restart_game(event):
    global player, obstacles, update_id, start_time, timer_text,last_time,last_time_text,last_time1  # Добавляем timer_text как глобальную переменную
    if canvas.find_withtag("game_over"):
        canvas.delete("game_over")
        canvas.delete("all")
        start_time = time.time()  # обнуляем start_time
        player = Player()
        obstacles = []
        timer_text = canvas.create_text(450, 20, text="Время: 0.00", font=("Arial", 15), anchor=tk.E)
        if last_time1 < last_time:
            last_time1 = last_time

        last_time_text = canvas.create_text(150, 20, text="Лучший результат: {:.2f} ".format(last_time1), font=("Arial", 15,))
        window.unbind_all("<Key>") # Удаляем все бинды
        window.bind("<KeyPress-w>", move_up)
        window.bind("<KeyRelease-w>", stop_move_up)
        window.bind("<KeyPress-s>", move_down)
        window.bind("<KeyRelease-s>", stop_move_down)
        window.bind("<KeyPress-a>", move_left)
        window.bind("<KeyRelease-a>", stop_move_left)
        window.bind("<KeyPress-d>", move_right)
        window.bind("<KeyRelease-d>", stop_move_right)
        window.bind("<KeyPress-r>", restart_game)
        update_game()
        back_button.config(state='disabled')

# Глобальные переменные
start_button = None
quit_button = None
root_button = None
back_button = None

# Функция для открытия главного меню
def open_main_menu():
    global start_button, quit_button,root_button,last_time1,last_time
    canvas.delete("all")
    canvas.create_text(250, 100, text="Добро пожаловать в игру Раннер!", font=("Arial", 20), anchor=tk.CENTER)

    start_button = tk.Button(window, text="Начать игру", font=("Arial Bold", 14), command=start_game)
    start_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    root_button = tk.Button(window, text="Правила игры", font=("Arial Bold", 14), command=root_game)
    root_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    quit_button = tk.Button(window, text="Выйти", font=("Arial Bold", 14), command=window.quit)
    quit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    last_time1 = 0
    last_time = 0

def open_main_menu1():
    global start_button, quit_button,root_button,last_time1
    canvas.delete("all")
    canvas.create_text(250, 100, text="Добро пожаловать в игру Раннер!", font=("Arial", 20), anchor=tk.CENTER)


    if last_time1 < last_time:
        last_time1 = last_time
    last_time_text = canvas.create_text(250, 150, text="Лучший результат: {:.2f} ".format(last_time1), font=("Arial", 15,))

    start_button = tk.Button(window, text="Начать игру", font=("Arial Bold", 14), command=start_game)
    start_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    root_button = tk.Button(window, text="Правила игры", font=("Arial Bold", 14), command=root_game)
    root_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    quit_button = tk.Button(window, text="Выйти", font=("Arial Bold", 14), command=window.quit)
    quit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    back_button.destroy()

# Функция для начала игры
def start_game():
    global player, obstacles, update_id, start_time, timer_text, back_button,last_time1,last_time
    canvas.delete("all")
    player = Player()
    obstacles = []
    #last_time1 = 0
    start_time = time.time()
    timer_text = canvas.create_text(450, 20, text="Время: 0.00", font=("Arial", 15), anchor=tk.E)
    if last_time1 < last_time:
        last_time1 = last_time
    last_time_text = canvas.create_text(150, 20, text="Лучший результат: {:.2f} ".format(last_time1), font=("Arial", 15,))
    window.bind("<KeyPress-w>", move_up)
    window.bind("<KeyRelease-w>", stop_move_up)
    window.bind("<KeyPress-s>", move_down)
    window.bind("<KeyRelease-s>", stop_move_down)
    window.bind("<KeyPress-a>", move_left)
    window.bind("<KeyRelease-a>", stop_move_left)
    window.bind("<KeyPress-d>", move_right)
    window.bind("<KeyRelease-d>", stop_move_right)
    window.bind("<KeyPress-r>", restart_game)
    update_game()

    # Удаляем кнопки "Начать игру" и "Выйти"
    start_button.destroy()
    root_button.destroy()
    quit_button.destroy()

    back_button = tk.Button(window, text="Назад", font=("Arial Bold", 14), command=open_main_menu1)
    back_button.place(relx=0.1, rely=0.9, anchor=tk.CENTER)
    back_button.config(state='disabled')

def root_game():
    global back_button
    canvas.delete("all")
    start_button.destroy()
    quit_button.destroy()
    root_button.destroy()

    canvas.create_text(250, 50, text="Правила игры:", font=("Arial", 25), anchor=tk.CENTER)
    canvas.create_text(150, 210, text='''
                                    Игра с бегущим прямоугольником. Суть игры 
                                    заключается в том, чтобы пробежать как 
                                    можно дольше.  
                                    При этом, игрок не должен столкнуться с 
                                    препятствием. В случае касания игроком
                                    препятствия, игра заканчивается, а
                                    лучший результат сохраняется в правом
                                    верхнем углу экрана.''', font=("Arial", 17), anchor=tk.CENTER)

    back_button = tk.Button(window, text="Назад", font=("Arial Bold", 14), command=open_main_menu1)
    back_button.place(relx=0.1, rely=0.9, anchor=tk.CENTER)


# Запускаем главное меню
open_main_menu()
window.mainloop()