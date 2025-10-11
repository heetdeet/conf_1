import argparse
import tomli
import os
import sys

class Config:
    def __init__(self):
        self.vfs_path = None
        self.script_path = None
        self.config_path = None
        
    def load_from_file(self, filepath):
        #загружаем конфигурацию из TOML файла
        try:
            with open(filepath, 'rb') as f:
                config_data = tomli.load(f)
                
            if 'vfs_path' in config_data:
                self.vfs_path = config_data['vfs_path']
            if 'script_path' in config_data:
                self.script_path = config_data['script_path']
                
        except FileNotFoundError:
            print(f"Ошибка: конфигурационный файл не найден: {filepath}")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка чтения конфигурационного файла: {e}")
            sys.exit(1)
    
    def load_from_args(self):
        #загружаем конфигурацию из аргументов командной строки
        parser = argparse.ArgumentParser(description='Эмулятор командной оболочки ОС')
        parser.add_argument('--vfs-path', help='Путь к физическому расположению VFS')
        parser.add_argument('--script-path', help='Путь к стартовому скрипту')
        parser.add_argument('--config-path', help='Путь к конфигурационному файлу')
        
        args = parser.parse_args()
        
        self.config_path = args.config_path
        
        # изначально загружаем из файла, если указан
        if self.config_path:
            self.load_from_file(self.config_path)
        
        # после перезаписываем значениями из командной строки (приоритет)
        if args.vfs_path:
            self.vfs_path = args.vfs_path
        if args.script_path:
            self.script_path = args.script_path
    
    def dump(self):
        #выводим текущую конфигурацию в формате ключ-значение
        print("Текущая конфигурация:")
        print(f"  VFS путь: {self.vfs_path or 'Не указан'}")
        print(f"  Скрипт путь: {self.script_path or 'Не указан'}")
        print(f"  Конфиг путь: {self.config_path or 'Не указан'}")