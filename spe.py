import tkinter as tk
import os
import importlib.util
from datetime import datetime
import calendar

class SonicOS:
    def __init__(self, root):
        self.root = root
        self.root.title("SonicOS 2.7")
        self.root.geometry("360x720")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(False, False)

        # Слушаем клавиатуру ПК
        self.root.bind("<Key>", self.handle_keyboard)

        self.screen_state = "HOME"
        self.menu_items = ["Phone", "Apps", "Files", "Clock", "Calendar", "Settings"]
        self.menu_index = 0
        self.active_app = None
        self.dial_buffer = ""

        for folder in ["apps", "FS"]:
            if not os.path.exists(folder): os.makedirs(folder)

        # --- КОРПУС ---
        self.outer_frame = tk.Frame(root, bg="#1a1a1a", bd=5, relief="raised")
        self.outer_frame.place(x=20, y=10, width=320, height=700)

        # --- ЭКРАН ---
        self.screen_bg = "#8ba37d"
        self.pixel_color = "#7a8f6d"
        self.display_border = tk.Frame(self.outer_frame, bg="#050505", bd=2)
        self.display_border.place(x=25, y=40, width=270, height=250)
        self.display_frame = tk.Frame(self.display_border, bg="#111", bd=10, relief="sunken")
        self.display_frame.place(x=5, y=5, width=260, height=240)
        self.canvas = tk.Canvas(self.display_frame, bg=self.screen_bg, highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")

        self.create_controls()
        self.update_loop()

    def handle_keyboard(self, event):
        key = event.keysym.lower()
        # Маппинг клавиш
        if key == 'w': self.input_event("HOME_KEY")
        elif key == 'q': self.input_event("OK")
        elif key == 'e': self.input_event("BACK")
        elif key in ['s', 'return']: self.input_event("OK")
        elif key == 'up': self.input_event("UP")
        elif key == 'down': self.input_event("DOWN")
        elif key == 'left': self.input_event("LEFT")
        elif key == 'right': self.input_event("RIGHT")
        elif key.isdigit(): self.input_event(key)

   def create_controls(self):
        # Панель управления (Джойстик и софт-клавиши)
        ctrl = tk.Frame(self.outer_frame, bg="#1a1a1a")
        ctrl.place(x=30, y=310, width=260, height=130)

        # Софт-клавиши
        tk.Button(ctrl, text="SELECT", bg="#444", fg="#0f0", font=("Arial", 8, "bold"), width=8, 
                  command=lambda: self.input_event("OK")).place(x=0, y=15)
        tk.Button(ctrl, text="BACK", bg="#444", fg="#f44", font=("Arial", 8, "bold"), width=8, 
                  command=lambda: self.input_event("BACK")).place(x=195, y=15)
        
        # Джойстик
        tk.Button(ctrl, text="^", width=4, font=("Arial", 10, "bold"), command=lambda: self.input_event("UP")).place(x=110, y=0)
        tk.Button(ctrl, text="v", width=4, font=("Arial", 10, "bold"), command=lambda: self.input_event("DOWN")).place(x=110, y=60)
        tk.Button(ctrl, text="<", width=4, font=("Arial", 10, "bold"), command=lambda: self.input_event("LEFT")).place(x=70, y=30)
        tk.Button(ctrl, text=">", width=4, font=("Arial", 10, "bold"), command=lambda: self.input_event("RIGHT")).place(x=150, y=30)
        tk.Button(ctrl, text="OK", bg="#333", fg="white", font=("Arial", 8, "bold"), width=4,
                  command=lambda: self.input_event("OK")).place(x=110, y=31)

        # Кнопка HOME
        tk.Button(ctrl, text="HOME", bg="#a00", fg="white", font=("Arial", 8, "bold"), 
                  command=lambda: self.input_event("HOME_KEY")).place(x=100, y=100, width=60)

        # --- ИСПРАВЛЕННАЯ ЦИФРОВАЯ СЕТКА ---
        num_fm = tk.Frame(self.outer_frame, bg="#1a1a1a")
        num_fm.place(x=30, y=450, width=260, height=220)
        
        # Настройка равномерных колонок
        num_fm.columnconfigure(0, weight=1)
        num_fm.columnconfigure(1, weight=1)
        num_fm.columnconfigure(2, weight=1)

        keys = ['1','2','3','4','5','6','7','8','9','*','0','#']
        for i, k in enumerate(keys):
            row = i // 3
            col = i % 3
            btn = tk.Button(num_fm, text=k, width=5, height=2, bg="#333", fg="white", 
                           font=("Arial", 14, "bold"), relief="raised", 
                           command=lambda x=k: self.input_event(x))
            # sticky="nsew" заставляет кнопку растягиваться и стоять ровно
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Джойстик с кнопками Лево и Право
        tk.Button(ctrl, text="▲", width=4, command=lambda: self.input_event("UP")).place(x=110, y=0)
        tk.Button(ctrl, text="▼", width=4, command=lambda: self.input_event("DOWN")).place(x=110, y=60)
        tk.Button(ctrl, text="◄", width=4, command=lambda: self.input_event("LEFT")).place(x=70, y=30)
        tk.Button(ctrl, text="►", width=4, command=lambda: self.input_event("RIGHT")).place(x=150, y=30)
        
        # Центральная кнопка OK
        tk.Button(ctrl, text="OK", bg="#333", fg="white", font=("Arial", 8, "bold"), width=4,
                  command=lambda: self.input_event("OK")).place(x=110, y=32)

        # Кнопка HOME ниже джойстика
        tk.Button(ctrl, text="HOME", bg="#a00", fg="white", font=("Arial", 8, "bold"), 
                  command=lambda: self.input_event("HOME_KEY")).place(x=100, y=100, width=60)

        # Цифровая панель
        num_fm = tk.Frame(self.outer_frame, bg="#1a1a1a")
        num_fm.place(x=55, y=450, width=210, height=220)
        keys = ['1','2','3','4','5','6','7','8','9','*','0','#']
        for i, k in enumerate(keys):
            tk.Button(num_fm, text=k, width=6, height=2, bg="#333", fg="white", font=("Arial", 12, "bold"),
                      command=lambda x=k: self.input_event(x)).grid(row=i//3, column=i%3, padx=5, pady=5)

    def draw_grid(self):
        # Рамка ЖК
        self.canvas.create_rectangle(2, 2, 238, 218, outline="#5a6f4d", width=2)
        # Сетка
        for i in range(0, 240, 3): 
            self.canvas.create_line(i, 0, i, 220, fill=self.pixel_color)
            self.canvas.create_line(0, i, 240, i, fill=self.pixel_color)

    def render(self):
        if self.screen_state == "RUNNING": return 
        self.canvas.delete("all")
        now = datetime.now().strftime("%H:%M")
        self.canvas.create_text(10, 10, text="SonicOS", font=("Courier", 10), anchor="nw")
        self.canvas.create_text(230, 10, text=now, font=("Courier", 10, "bold"), anchor="ne")
        self.canvas.create_line(0, 22, 240, 22)

        if self.screen_state == "HOME":
            self.canvas.create_text(120, 100, text="READY", font=("Courier", 35, "bold"))
        elif self.screen_state == "MENU":
            for i, item in enumerate(self.menu_items):
                pref = "> " if i == self.menu_index else "  "
                self.canvas.create_text(20, 45+(i*25), text=f"{pref}{item.upper()}", font=("Courier", 14), anchor="nw")
        elif self.screen_state == "APPS":
            apps = [f for f in os.listdir("apps") if f.endswith(".py")]
            self.canvas.create_text(120, 35, text="- APPS -", font=("Courier", 10, "bold"))
            for i, a in enumerate(apps[:7]):
                pref = "> " if i == self.menu_index else "  "
                self.canvas.create_text(20, 60+(i*22), text=f"{pref}{a[:-3].upper()}", font=("Courier", 12), anchor="nw")
        elif self.screen_state == "CALENDAR":
            now = datetime.now()
            self.canvas.create_text(120, 110, text=calendar.month(now.year, now.month), font=("Courier", 9), justify="center")
        elif self.screen_state == "PHONE":
            self.canvas.create_text(120, 60, text="DIAL:", font=("Courier", 12))
            self.canvas.create_text(120, 110, text=self.dial_buffer, font=("Courier", 18, "bold"))

        self.draw_grid()

    def input_event(self, key):
        if key == "HOME_KEY":
            self.screen_state = "HOME"; self.active_app = None; self.dial_buffer = ""; self.render(); return

        if self.screen_state == "RUNNING" and self.active_app:
            self.active_app.on_input(key)
            return

        if key == "BACK":
            self.screen_state = "MENU" if self.screen_state != "HOME" else "HOME"
        elif key == "OK":
            if self.screen_state == "HOME": self.screen_state = "MENU"
            elif self.screen_state == "MENU":
                choice = self.menu_items[self.menu_index]
                self.screen_state = choice.upper(); self.menu_index = 0
            elif self.screen_state == "APPS":
                apps = [f for f in os.listdir("apps") if f.endswith(".py")]
                if apps: self.launch_app(apps[self.menu_index])
        elif key in ["UP", "DOWN", "LEFT", "RIGHT"]:
            limit = len(self.menu_items) if self.screen_state == "MENU" else 7
            move = -1 if key == "UP" else 1 if key == "DOWN" else 0
            self.menu_index = (self.menu_index + move) % limit
        elif self.screen_state == "PHONE" and (key.isdigit() or key in ["*", "#"]):
            self.dial_buffer += key

        self.render()

    def launch_app(self, filename):
        path = os.path.join("apps", filename)
        spec = importlib.util.spec_from_file_location("module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.canvas.delete("all")
        self.screen_state = "RUNNING"
        self.active_app = module.App(self)
        self.active_app.render()

    def update_loop(self):
        if self.screen_state != "RUNNING": self.render()
        self.root.after(1000, self.update_loop)

if __name__ == "__main__":
    root = tk.Tk()
    os_app = SonicOS(root)
    root.mainloop()
