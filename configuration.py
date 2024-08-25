import os
import pickle
from const import *
class Configuration:
    config_file_path = "config.pkl"
    accounts_file_path = "accounts.txt"
    key_of_number_values = ['num_tab_per_col', 'vertical_spacing', 'horizontal_spacing', 
                    'minimal_width', 'minimal_height', 'col_spacing', 'time_delay_1_4', 
                    'time_delay_5_6', 'time_delay_7_8', 'time_delay_9_10', 'num_mini_tab_per_row',
                    'indentation', 'indentation_mini_tab', 'mini_tab_margin_top'
                    ]
    
    @staticmethod
    def create_files_if_not_exists():
        # Tạo tệp accounts.txt nếu không tồn tại
        if not os.path.isfile(Configuration.accounts_file_path):
            with open(Configuration.accounts_file_path, 'w') as f:
                f.write('')  # Tạo tệp rỗng

        # Tạo tệp settings.pkl nếu không tồn tại
        if not os.path.isfile(Configuration.config_file_path):
            default_settings = {
                'game_path': DEFAULT_GAME_PATH,
                'game_title': DEFAULT_GAME_TITLE,
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
                'num_mini_tab_per_row': DEFAULT_NUM_MINI_TAB_PER_ROW,
                'tab_align': DEFAULT_TAB_ALGIN,
                'mini_tab_align': DEFAULT_MINI_TAB_ALGIN,
                'indentation': DEFAULT_INDENTATION_TAB,
                'indentation_mini_tab': DEFAULT_INDENTATION_TAB,
                'mini_tab_margin_top': DEFAULT_MINI_TAB_MARGIN_TOP,
                'first_time':True
            }
            with open(Configuration.config_file_path, 'wb') as f:
                pickle.dump(default_settings, f)
    
    @staticmethod
    def load_config():
        Configuration.create_files_if_not_exists()
        with open(Configuration.config_file_path, 'rb') as config_file:
            config = pickle.load(config_file)
        
        # Chuyển đổi các giá trị cấu hình
        for key in Configuration.key_of_number_values:
            if key in config and config[key] != None:
                config[key] = int(config[key])
        
        config['first_time'] = bool(config['first_time'])
        print("Application config:", config)
        return config
    
    @staticmethod
    def save_config(config):
        with open(Configuration.config_file_path, 'wb') as config_file:
            pickle.dump(config, config_file)
