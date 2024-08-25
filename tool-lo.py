import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk, messagebox, filedialog
import pickle
from window_game import *
import os
import threading
import keyboard

class Application(ThemedTk):
    def __init__(self,theme="arc"):
        ThemedTk.__init__(self, fonts=True, themebg=True)
        self.set_theme(theme)
        self.style = ttk.Style()
        self.style.configure('lefttab.TNotebook', tabposition='wn')
        current_theme =self.style.theme_use()
        self.style.theme_settings(current_theme, {"TNotebook.Tab": {"configure": {'background':'white', "padding": [10, 8]}}}) 
        self.config_file_path = "config.pkl"
        self.accounts_file_path = "accounts.txt"
        self.logged_in_windows = {}  # Dictionary to store logged-in windows

        self.stop_login_flag = False  # Cờ để kiểm tra có dừng đăng nhập hay không
        # Thiết lập phím F3 để dừng đăng 

        self.create_files_if_not_exists()
        self.config = self.load_config()
        # threading.Thread(target=self.listen_for_stop, daemon=True).start()

    def listen_for_stop(self):
        while True:
            if keyboard.is_pressed('F3'):
                print("F3 được nhấn!")
                self.stop_login_flag = True
                time.sleep(1)
    def create_files_if_not_exists(self):
        # Tạo tệp accounts.txtpicolo01 nếu không tồn tại
        if not os.path.isfile(self.accounts_file_path):
            with open(self.accounts_file_path, 'w') as f:
                f.write('')  # Tạo tệp rỗng

        # Tạo tệp settings.pkl nếu không tồn tại
        if not os.path.isfile(self.config_file_path):
            default_settings = {
                'game_path': DEFAULT_GAME_PATH,
                'num_tab_per_col': DEFAULT_NUM_TAB_PER_COL,
                'vertical_spacing': DEFAULT_VERTICAL_SPACING,
                'horizontal_spacing': DEFAULT_HORIZONTAL_SPACING,
                'minimal_width': DEFAULT_MINIMAL_WIDTH,
                'minimal_height': DEFAULT_MINIMAL_HEIGHT,
                'col_spacing': DEFAULT_COL_SPACING,
                'time_delay_1_4': DEFAULT_DELAY_TIME_1_TO_4,
                'time_delay_5_6': DEFAULT_DELAY_TIME_5_TO_6,
                'time_delay_7_8': DEFAULT_DELAY_TIME_7_TO_8,
                'time_delay_9_10': DEFAULT_DELAY_TIME_9_TO_10,
                'num_mini_tab_per_row': DEFAULT_NUM_MINI_TAB_PER_ROW
            }
            with open(self.config_file_path, 'wb') as f:
                pickle.dump(default_settings, f)
    
    def save_timing_config(self):
        self.config['time_delay_1_4'] = int(self.entry_time_deplay_1.get())
        self.config['time_delay_5_6'] = int(self.entry_time_deplay_2.get())
        self.config['time_delay_7_8'] = int(self.entry_time_deplay_3.get())
        self.config['time_delay_9_10'] = int(self.entry_time_deplay_4.get())
        with open(self.config_file_path, 'wb') as config_file:
            pickle.dump(self.config, config_file)

    def save_spacing_config(self):
        self.config['num_tab_per_col'] = int(self.entry_num_tab_per_col.get())
        self.config['vertical_spacing'] = int(self.entry_vertical_spacing.get())
        self.config['horizontal_spacing'] = int(self.entry_horizontal_spacing.get())
        self.config['minimal_width'] = int(self.entry_minimal_width.get())
        self.config['minimal_height'] = int(self.entry_minimal_height.get())
        self.config['col_spacing'] = int(self.entry_col_spacing.get())
        self.config['num_mini_tab_per_row'] = int(self.entry_num_mini_tab_per_row.get())
        with open(self.config_file_path, 'wb') as config_file:
            pickle.dump(self.config, config_file)
        
        self.update_current_window()
        print(self.config)
    def save_shortcut_config(self):
        pass
    def update_current_window(self):
        for hWnd, windowGame in self.logged_in_windows.items():
            windowGame.change_config(self.config)
            windowGame.restore_init_position()
    
    def load_config(self):
        try:
            with open(self.config_file_path, 'rb') as config_file:
                config = pickle.load(config_file)
        except (FileNotFoundError, EOFError):
            config = {}
        
        # Chuyển đổi các giá trị cấu hình
        for key in ['num_tab_per_col', 'vertical_spacing', 'horizontal_spacing', 
                    'minimal_width', 'minimal_height', 'col_spacing', 'time_delay_1_4', 
                    'time_delay_5_6', 'time_delay_7_8', 'time_delay_9_10', 'entry_num_mini_tab_per_row']:
            if key in config:
                config[key] = int(config[key])
        
        print("Application config:", config)
        return config
    
    def save_account(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username and password:
            with open(self.accounts_file_path, 'a') as file:
                file.write(f'{username} {password}\n')
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self.update_account_list()
        else:
            messagebox.showwarning('Input error', 'Please enter both username and password')

    def update_account_list(self):
        self.listbox_accounts.delete(0, tk.END)
        try:
            with open(self.accounts_file_path, 'r') as file:
                accounts = file.readlines()
                for account in accounts:
                    self.listbox_accounts.insert(tk.END, account.strip())
        except FileNotFoundError:
            messagebox.showwarning('File not found', 'Account file not found. Please select a valid file.')

    def delete_account(self):
        selected_account = self.listbox_accounts.curselection()
        if selected_account:
            account = self.listbox_accounts.get(selected_account)
            with open(self.accounts_file_path, 'r') as file:
                accounts = file.readlines()
            with open(self.accounts_file_path, 'w') as file:
                for acc in accounts:
                    if acc.strip() != account:
                        file.write(acc)
            self.update_account_list()
            messagebox.showinfo('Success', 'Account deleted successfully')

    def select_game_path(self):
        game_path = filedialog.askopenfilename(title='Select Game Executable', filetypes=[('Executable files', '*.exe')])
        if game_path:
            self.config['game_path'] = game_path
            with open(self.config_file_path, 'wb') as config_file:
                pickle.dump(self.config, config_file)
            self.game_path = game_path
            self.entry_game_path.delete(0, tk.END)
            self.entry_game_path.insert(0, game_path)
            messagebox.showinfo('Game Path Selected', f'Game Path: {game_path}')
    
    def reset_tab_positions(self):
        self.notebook.select(0)
        messagebox.showinfo('Reset Tabs', 'Tabs have been reset to their original positions.')

    def minimize_tabs(self):
        self.root.state('iconic')

    def enable_editing(self):
        self.text_accounts.config(state=tk.NORMAL)
        self.text_accounts.delete(1.0, tk.END)
        with open(self.accounts_file_path, 'r') as file:
            accounts = file.readlines()
            for account in accounts:
                self.text_accounts.insert(tk.END, account)
        self.text_accounts.pack(side=tk.LEFT, padx=10, pady=10, fill='both', expand=True)
        self.listbox_accounts.pack_forget()
        self.btn_edit.config(state=tk.DISABLED)
        self.btn_save_edit.config(state=tk.NORMAL)

    def save_editing(self):
        with open(self.accounts_file_path, 'w') as file:
            file.write(self.text_accounts.get(1.0, tk.END))
        self.text_accounts.pack_forget()
        self.listbox_accounts.pack(side=tk.LEFT, padx=10, pady=10, fill='both', expand=True)
        self.text_accounts.config(state=tk.DISABLED)
        self.btn_edit.config(state=tk.NORMAL)
        self.btn_save_edit.config(state=tk.DISABLED)
        self.update_account_list()
        messagebox.showinfo('Success', 'Accounts updated successfully')
    
    def find_window_by_index(self, index):
        for hWnd, windowGame in self.logged_in_windows.items():
            if windowGame.index == index:
                return windowGame 
        return None

    # def stop_login(self):
    #     print("Dừng đăng nhập!")
    #     self.stop_login_flag = True

    def login(self):
        self.stop_login_flag = False  # Đặt lại cờ trước khi bắt đầu đăng nhập

        with open(self.accounts_file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if self.stop_login_flag:
                break

            line = line.strip()
            if line:
                username, password = line.split(' ', 1)
                window = WindowGame(i, self.config, username, password)
                hWnd = window.login()
                window.minimize()
                self.logged_in_windows[str(hWnd)] = window

        self.update_logged_in_accounts_list()
        self.expand_all_tabs()
    
    def close_window(self, hWnd):
        window = self.logged_in_windows.get(hWnd)
        if window:
            window.close()
            self.update_logged_in_accounts_list()
            del self.logged_in_windows[hWnd]
        else:
            del self.logged_in_windows[hWnd]

    def focus_window(self, event): 
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            value = event.widget.get(index)
            hWnd = value.split(':')[0]
            windowGame = self.logged_in_windows.get(hWnd)
            text = "Phóng to" if windowGame.is_zoom_out else "Thu nhỏ"
            self.btn_minimize.config(text=text)
            windowGame.focus()

    def toggle_zoom_out(self, hWnd):
        windowGame = self.logged_in_windows.get(hWnd)
        if windowGame:
            windowGame.toggle_zoom_out()
        
        text = "Phóng to" if windowGame.is_zoom_out else "Thu nhỏ"
        self.btn_minimize.config(text=text)

    def restore_position(self, hWnd):
        windowGame = self.logged_in_windows.get(hWnd)
        if windowGame:
            windowGame.restore_init_postion()

    def set_active_item(self, index):
        self.listbox_logged_in_accounts.selection_clear(0, tk.END)  # Xóa tất cả các lựa chọn hiện tại
        self.listbox_logged_in_accounts.selection_set(index)  # Đặt mục tại index làm mục đang hoạt động
        self.listbox_logged_in_accounts.activate(index)  # Đặt mục tại index làm mục đang hoạt động

    def move_down(self, hWnd):
        window = self.logged_in_windows.get(hWnd)
        if window:
            index = window.index 
            next_windows = self.find_window_by_index(index + 1)
            if next_windows: 
                window.swap(next_windows)
                self.update_logged_in_accounts_list()
                self.set_active_item(index + 1)

    def move_up(self, hWnd):
        window = self.logged_in_windows.get(hWnd)
        if window:
            index = window.index 
            next_windows = self.find_window_by_index(index - 1)
            if next_windows: 
                window.swap(next_windows)
                self.update_logged_in_accounts_list()
                self.set_active_item(index - 1)

    def update_logged_in_accounts_list(self):
        sorted_accounts_by_indx = dict(sorted(self.logged_in_windows.items(), key=lambda item: item[1].index))
        self.listbox_logged_in_accounts.delete(0, tk.END)
        for handle, windowGame in sorted_accounts_by_indx.items():
            self.listbox_logged_in_accounts.insert(tk.END, f"{handle}:tk={windowGame.username},idx={windowGame.index}")

    def on_account_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            value = event.widget.get(index)
            messagebox.showinfo("Account Selected", f"Bạn đã chọn: {value}")

    def minimize_all_tabs(self):
        items = self.logged_in_windows.items()
        for handle, windowGame in items:
            windowGame.minimize()
    
    def expand_all_tabs(self):
        items = self.logged_in_windows.items()
        for handle, windowGame in items:
            windowGame.restore_origin_size()
    
    def close_all(self):
        for hWnd, windowGame in self.logged_in_windows.items():
            windowGame.close()
        self.logged_in_windows.clear()
        self.update_logged_in_accounts_list()

    def nhap_code(self):
        code = self.entry_code.get()
        self.stop_login_flag = False  # Đặt lại cờ trước khi bắt đầu đăng nhập
        # threading.Thread(target=self.listen_for_stop, daemon=True).start()
        with open(self.accounts_file_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if self.stop_login_flag:
                break

            line = line.strip()
            if line:
                username, password = line.split(' ', 1)
                window = WindowGame(0, self.config, username, password)
                window.login()
                time.sleep(5)
                window.nhap_code(code)
                time.sleep(5)
                window.close()
                time.sleep(5)


    def show_account_tab_ui(self, frame_manage):
        username = tk.StringVar()
        password = tk.StringVar()

        frame_inputs = tk.Frame(frame_manage)
        frame_inputs.pack(pady=10)

        label_username = tk.Label(frame_inputs, text='Tài khoản:')
        label_username.grid(row=0, column=0, padx=5)
        self.entry_username = tk.Entry(frame_inputs, textvariable=username)
        self.entry_username.grid(row=0, column=1, padx=5)

        label_password = tk.Label(frame_inputs, text='Mật khẩu:')
        label_password.grid(row=0, column=2, padx=5)
        self.entry_password = tk.Entry(frame_inputs, textvariable=password)
        self.entry_password.grid(row=0, column=3, padx=5)

        btn_save = tk.Button(frame_inputs, text='Lưu', command=self.save_account)
        btn_save.grid(row=0, column=4, padx=5)

        frame_content = tk.Frame(frame_manage)
        frame_content.pack(fill='both', expand=True)

        self.listbox_accounts = tk.Listbox(frame_content)
        self.listbox_accounts.pack(side=tk.LEFT, padx=10, pady=10, fill='both', expand=True)

        self.text_accounts = tk.Text(frame_content, state=tk.DISABLED)

        frame_buttons = tk.Frame(frame_content)
        frame_buttons.pack(side=tk.RIGHT, padx=10, pady=10, fill='y')

        btn_delete = tk.Button(frame_buttons, text='Xóa tài khoản', command=self.delete_account)
        btn_delete.pack(pady=5)

        self.btn_edit = tk.Button(frame_buttons, text='Chỉnh sửa', command=self.enable_editing)
        self.btn_edit.pack(pady=5)

        self.btn_save_edit = tk.Button(frame_buttons, text='Lưu thay đổi', command=self.save_editing, state=tk.DISABLED)
        self.btn_save_edit.pack(pady=5) 

        frame_action_btns = tk.Frame(frame_manage)
        frame_action_btns.pack(padx=10, pady=10, fill='x')

        btn_login = tk.Button(frame_action_btns, text='Đăng nhập', command=self.login)
        btn_login.grid(row=0, column=0, padx=5, pady=5)

    def show_config_tab_ui(self, frame_config):
    # Xóa các widget hiện có
        for widget in frame_config.winfo_children():
            widget.pack_forget()

        # Tạo một Notebook mới
        self.nb = ttk.Notebook(frame_config, style='lefttab.TNotebook')
        self.nb.pack(fill='both', expand=True)

        # Tạo các trang mới
        self.page_path = ttk.Frame(self.nb, width=500, height=300)
        self.page_spacing = ttk.Frame(self.nb, width=500, height=300)
        self.page_timing = ttk.Frame(self.nb, width=500, height=300)
        self.page_shortcut = ttk.Frame(self.nb, width=500, height=300)

        # Thay đổi màu nền của các trang
        self.style = ttk.Style()
        self.style.configure("TFrame", background='white')

        # Thêm các trang vào Notebook
        self.nb.add(self.page_path, text='Đường dẫn', sticky="nsew")
        self.nb.add(self.page_spacing, text='Khoảng cách', sticky="nsew")
        self.nb.add(self.page_timing, text='Thời gian', sticky="nsew")
        self.nb.add(self.page_shortcut, text='Phím tắt', sticky="nsew")

        # Trang Đường dẫn
        tk.Label(self.page_path, text="Đường dẫn game:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_game_path = tk.Entry(self.page_path, width=50)
        self.entry_game_path.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.entry_game_path.insert(0, self.config.get('game_path', DEFAULT_GAME_PATH))

        tk.Button(self.page_path, text='Chọn đường dẫn', command=self.select_game_path).grid(row=1, column=0, columnspan=2, pady=10)

        # Trang Khoảng cách
        tk.Label(self.page_spacing, text="Số tab mỗi cột:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_num_tab_per_col = tk.Entry(self.page_spacing, width=10)
        self.entry_num_tab_per_col.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.entry_num_tab_per_col.insert(0, self.config.get('num_tab_per_col', DEFAULT_NUM_TAB_PER_COL))

        tk.Label(self.page_spacing, text="Khoảng cách dọc:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_vertical_spacing = tk.Entry(self.page_spacing, width=10)
        self.entry_vertical_spacing.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.entry_vertical_spacing.insert(0, self.config.get('vertical_spacing', DEFAULT_VERTICAL_SPACING))

        tk.Label(self.page_spacing, text="Khoảng cách ngang:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_horizontal_spacing = tk.Entry(self.page_spacing, width=10)
        self.entry_horizontal_spacing.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.entry_horizontal_spacing.insert(0, self.config.get('horizontal_spacing', DEFAULT_HORIZONTAL_SPACING))

        tk.Label(self.page_spacing, text="Khoảng cách cột:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_col_spacing = tk.Entry(self.page_spacing, width=10)
        self.entry_col_spacing.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.entry_col_spacing.insert(0, self.config.get('col_spacing', DEFAULT_COL_SPACING))

        tk.Label(self.page_spacing, text="Chiều rộng thu nhỏ:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.entry_minimal_width = tk.Entry(self.page_spacing, width=10)
        self.entry_minimal_width.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.entry_minimal_width.insert(0, self.config.get('minimal_width', DEFAULT_MINIMAL_WIDTH))

        tk.Label(self.page_spacing, text="Chiều cao thu nhỏ:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.entry_minimal_height = tk.Entry(self.page_spacing, width=10)
        self.entry_minimal_height.grid(row=5, column=1, padx=5, pady=5, sticky='w')
        self.entry_minimal_height.insert(0, self.config.get('minimal_height', DEFAULT_MINIMAL_HEIGHT))

        tk.Label(self.page_spacing, text="Số tab thu nhỏ trên 1 dòng:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.entry_num_mini_tab_per_row = tk.Entry(self.page_spacing, width=10)
        self.entry_num_mini_tab_per_row.grid(row=6, column=1, padx=5, pady=5, sticky='w')
        self.entry_num_mini_tab_per_row.insert(0, self.config.get('num_mini_tab_per_row', DEFAULT_NUM_MINI_TAB_PER_ROW))

        # Thêm nút lưu cấu hình vào trang khoảng cách
        tk.Button(self.page_spacing, text="Lưu", command=self.save_spacing_config).grid(row=7, column=0, columnspan=2, pady=10)

        # Trang Phím tắt (Empty example, add your configuration here)
        tk.Label(self.page_shortcut, text="Phím tắt - Chưa cấu hình").pack(pady=10)

        # Trang timing
        tk.Label(self.page_timing, text="Thời gian deplay (1-4 tabs):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_time_deplay_1 = tk.Entry(self.page_timing, width=10)
        self.entry_time_deplay_1.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.entry_time_deplay_1.insert(0, self.config.get('time_delay_1_4', 900))

        tk.Label(self.page_timing, text="Thời gian deplay (5-6 tabs):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_time_deplay_2 = tk.Entry(self.page_timing, width=10)
        self.entry_time_deplay_2.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.entry_time_deplay_2.insert(0, self.config.get('time_delay_5_6', DEFAULT_DELAY_TIME_5_TO_6))

        tk.Label(self.page_timing, text="Thời gian deplay (7-8 tabs):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_time_deplay_3 = tk.Entry(self.page_timing, width=10)
        self.entry_time_deplay_3.grid(row=3, column=1, padx=5, pady=5, sticky='w')
        self.entry_time_deplay_3.insert(0, self.config.get('time_delay_7_8', DEFAULT_DELAY_TIME_7_TO_8))

        tk.Label(self.page_timing, text="Thời gian deplay (9-10 tabs):").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.entry_time_deplay_4 = tk.Entry(self.page_timing, width=10)
        self.entry_time_deplay_4.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.entry_time_deplay_4.insert(0, self.config.get('time_delay_9_10', DEFAULT_DELAY_TIME_9_TO_10))

        tk.Button(self.page_timing, text="Lưu", command=self.save_timing_config).grid(row=5, column=0, columnspan=2, pady=10)
        
        # Đảm bảo các cột có kích thước đồng đều
        self.page_spacing.grid_columnconfigure(1, weight=1)
        self.page_path.grid_columnconfigure(1, weight=1)
        self.page_shortcut.grid_columnconfigure(1, weight=1)

    def show_extra_tab_ui(self, frame_extra):        
        self.label_code = tk.Label(frame_extra, text='Nhập code:')
        self.label_code.pack(pady=5)

        # Tạo widget để nhập code
        self.entry_code = tk.Entry(frame_extra)
        self.entry_code.pack(pady=5)

        # Tạo nút Bắt đầu
        self.btn_bat_dau = tk.Button(frame_extra, text='Bắt đầu', command=self.nhap_code)
        self.btn_bat_dau.pack(pady=5)
    def show_logged_in_accounts_tab_ui(self, frame_logged_in):
        frame_logged_in_content = tk.Frame(frame_logged_in)
        frame_logged_in_content.pack(fill='both', expand=True)

        self.listbox_logged_in_accounts = tk.Listbox(frame_logged_in_content)
        self.listbox_logged_in_accounts.pack(side=tk.LEFT, padx=10, pady=10, fill='both', expand=True)

        self.listbox_logged_in_accounts.bind('<<ListboxSelect>>', self.focus_window)

        frame_buttons = tk.Frame(frame_logged_in_content)
        frame_buttons.pack(side=tk.RIGHT, padx=10, pady=10, fill='y')

        btn_close = tk.Button(frame_buttons, text='Đóng cửa sổ', command=lambda: self.close_window(self.listbox_logged_in_accounts.get(tk.ACTIVE).split(':')[0]))
        btn_close.pack(pady=5)

        self.btn_minimize = tk.Button(frame_buttons, text='Thu nhỏ', command=lambda: self.toggle_zoom_out(self.listbox_logged_in_accounts.get(tk.ACTIVE).split(':')[0]))
        self.btn_minimize.pack(pady=5)

        btn_move_up = tk.Button(frame_buttons, text='Di chuyển lên', command=lambda: self.move_up(self.listbox_logged_in_accounts.get(tk.ACTIVE).split(':')[0]))
        btn_move_up.pack(pady=5)

        btn_move_down = tk.Button(frame_buttons, text='Di chuyển xuống', command=lambda: self.move_down(self.listbox_logged_in_accounts.get(tk.ACTIVE).split(':')[0]))
        btn_move_down.pack(pady=5)

        frame_action_btns = tk.Frame(frame_logged_in)
        frame_action_btns.pack(padx=10, pady=10, fill='x')

        btn_minimal_all_tabs = tk.Button(frame_action_btns, text='Thu nhỏ tất cả', command=self.minimize_all_tabs)
        btn_minimal_all_tabs.grid(row=0, column=0, padx=5, pady=5)
        
        btn_expand_all_tabs = tk.Button(frame_action_btns, text='Phóng to tất cả', command=self.expand_all_tabs)
        btn_expand_all_tabs.grid(row=0, column=1, padx=5, pady=5)

        btn_close_all = tk.Button(frame_action_btns, text='Đóng tất cả', command=self.close_all)
        btn_close_all.grid(row=0, column=2, padx=5, pady=5)

    def create_frame(self, notebook):
        frame = tk.Frame(notebook, width=680, height=360)
        frame.pack(fill='both', expand=True)
        return frame

    def create_ui(self):
        self.title("Tool lỏ")
        self.geometry("480x480")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        frame_manage = self.create_frame(self.notebook)
        frame_config = self.create_frame(self.notebook)
        # frame_extra = self.create_frame(self.notebook)
        frame_logged_in = self.create_frame(self.notebook)

        self.notebook.add(frame_manage, text='Quản lý tài khoản')
        self.notebook.add(frame_config, text='Cấu hình')
        self.notebook.add(frame_logged_in, text='Tài khoản đã đăng nhập')
        # self.notebook.add(frame_extra, text='Nâng cao')

        self.show_account_tab_ui(frame_manage)
        self.show_config_tab_ui(frame_config)
        # self.show_extra_tab_ui(frame_extra)
        self.show_logged_in_accounts_tab_ui(frame_logged_in)
        
    def run(self):
        self.accounts_file_path = self.config.get('file_path', self.accounts_file_path)
        self.game_path = self.config.get('game_path', "")
        self.create_ui()
        self.update_account_list()
        self.mainloop()

app = Application()
app.run()
