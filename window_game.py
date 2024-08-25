import subprocess
import time
import pygetwindow as gw
from pywinauto import Application
import pyautogui
import win32gui
import win32con
import tkinter as tk
from tkinter import messagebox
from const import *


class WindowGame:
    count_index = 0 
    def __init__(self, config, username="", password=""):
        self.config = config
        self.window = None
        self.rect = None
        self.index = WindowGame.count_index
        self.username = username
        self.password = password
        self.is_logged = False
        self.is_zoom_out = False

        WindowGame.count_index += 1
    
    @staticmethod
    def set_count_index(value):
        WindowGame.count_index = value

    def set_index(self, index):
        self.index = index

    def change_config(self, config):
        self.config = config
        
    def open_window(self, x, y):
        if not self.config['game_path']:
            print("Không tìm thấy đường dẫn tới file.")
            return None

        try:
            subprocess.Popen(self.config['game_path'])
            delay = self.config['time_delay_1_4']
            if (self.index == 4 or self.index == 5):
                delay = self.config['time_delay_5_6']
            elif (self.index == 6 or self.index == 7):
                delay = self.config['time_delay_7_8']
            elif self.index > 7:
                delay = self.config['time_delay_9_10']

            time.sleep(delay)

            windows = gw.getWindowsWithTitle(self.config['game_title'])
            if not windows:
                print("Không tìm thấy cửa sổ.")
                return None

            window = windows[0]
            app = Application().connect(handle=window._hWnd)
            app_window = app.window(handle=window._hWnd)

            try:
                app_window.wait('ready', timeout=30)
                rect = app_window.rectangle()
                # print(f"Window handle {window._hWnd} - Position: {rect.left}, {rect.top}, {rect.right}, {rect.bottom}")
                app_window.move_window(x=x, y=y)
                self.window = window
                self.is_logged = True
            except timings.TimeoutError:
                print("Cửa sổ không sẵn sàng trong thời gian cho phép.")
                return None

        except FileNotFoundError:
            messagebox.showwarning('File error', 'Không tìm thấy file NgocRongNguyenThuy.exe')
        return None

    def get_screen_width(self):
        root = tk.Tk()
        width = root.winfo_screenwidth()
        root.destroy()  # Đóng cửa sổ khi không cần nữa
        return width
    def calc_position(self):
        x, y = 0, 0
        if not self.is_zoom_out:
            if (self.config["tab_align"] == 'left'):
                if self.index >= self.config['num_tab_per_col']:
                    x += self.config['col_spacing']
                    y = 0
                x += self.index * self.config['horizontal_spacing']
                y += (self.index % self.config['num_tab_per_col']) * self.config['vertical_spacing']
            else:
                x,y = self.get_screen_width() - ORIGINAL_WIDTH, 0
                if self.index >= self.config['num_tab_per_col']:
                    x -= self.config['col_spacing']
                    y = 0
                x -= ((self.config['indentation']) + self.index * self.config['horizontal_spacing'])
                y += (self.index % self.config['num_tab_per_col']) * self.config['vertical_spacing']

        else:
            if self.index >= self.config['num_mini_tab_per_row']:
                y = self.config['minimal_height'] * int(self.index / self.config['num_mini_tab_per_row'])

            if self.config['mini_tab_align'] == 'left':
                x = self.config['indentation_mini_tab'] + (self.index % self.config['num_mini_tab_per_row']) * self.config['minimal_width']
            else:
                screen_width = self.get_screen_width()
                x = screen_width - self.config['indentation_mini_tab'] - ((self.index % self.config['num_mini_tab_per_row'])+1) * self.config['minimal_width']
            y += self.config['mini_tab_margin_top']
        return x, y 

    def login(self):
        x, y = self.calc_position()
        self.open_window(x, y)
        if self.window:
            pyautogui.click(x + 662, y + 425)
            pyautogui.click(x + 654, y + 344)
            pyautogui.write(self.username, interval=0.05)
            pyautogui.click(x + 657, y + 409)
            pyautogui.write(self.password, interval=0.05)
            pyautogui.click(x + 433, y + 524)
            pyautogui.click(x + 535, y + 303)

            return self.window._hWnd
        return None

    def close(self):
        if self.window:
            try:
                self.window.close()
                return True
            except:
                return False

    def focus(self):
        if self.window:
            self.window.activate()

    def toggle_zoom_out(self):
        if self.is_zoom_out:
            self.restore_origin_size()
        else:
            self.minimize()

    def minimize(self):
        if self.window:
            self.is_zoom_out = True
            x, y = self.calc_position()
            win32gui.MoveWindow(self.window._hWnd, x, y, self.config['minimal_width'], self.config['minimal_height'], True)
            print(x,y)

    def restore_origin_size(self):
        if self.window:
            self.is_zoom_out = False
            x, y = self.calc_position()
            win32gui.MoveWindow(self.window._hWnd, x, y, ORIGINAL_WIDTH, ORIGINAL_HEIGHT, True)

    def restore_init_position(self):
        if self.window:
            x, y = self.calc_position()
            rect = win32gui.GetWindowRect(self.window._hWnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            # Di chuyển cửa sổ đến (x, y) với kích thước hiện tại
            win32gui.MoveWindow(self.window._hWnd, x, y, width, height, True)

    def swap(self, other_window):
        if self.window and other_window:
            temp = self.index
            self.index = other_window.index
            other_window.set_index(temp)

            self.restore_init_position()
            other_window.restore_init_position()
    
    def nhap_code(self, code):
        x,y = 0, 0
        if self.window:
         # Click vào vị trí
            pyautogui.click(x + 527, y + 590)
            
            self.focus()
            # Nhấn phím Enter
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.press('right')
            time.sleep(0.5)
            pyautogui.press('enter') 
            time.sleep(0.5)
            
            # Click vào vị trí khác
            pyautogui.click(x + 523, y + 501)
            time.sleep(0.5)
            # Gõ mã
            pyautogui.write(code, interval=0.2)
            time.sleep(0.5)
            
            # Click vào vị trí khác
            pyautogui.click(x + 649, y + 595)

