import os
import getpass
import socket
from config import Config
from vfs import VFS

class Emulator:
    def __init__(self, config):
        self.config = config
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.vfs = VFS()
        self.update_prompt()
        self.commands = {
            'exit': self.cmd_exit,
            'ls': self.cmd_ls,
            'cd': self.cmd_cd,
            'conf-dump': self.cmd_conf_dump,
            'pwd': self.cmd_pwd,
            'cat': self.cmd_cat,
        }

    def update_prompt(self):
        #обновляет приглашение с текущим путем VFS
        current_path = self.vfs.get_current_path()
        self.prompt = f"{self.username}@{self.hostname}:{current_path}$ "

    def run(self):
        #запускает эмулятор
        #отладочный вывод конфигурации при старте
        print("=== Отладочный вывод конфигурации ===")
        self.config.dump()
        print("=====================================")
        print()
        
        #загрузка VFS если указан путь
        if self.config.vfs_path and os.path.exists(self.config.vfs_path):
            try:
                self.vfs.load_from_json(self.config.vfs_path)
                print(f"VFS успешно загружена из {self.config.vfs_path}")
            except Exception as e:
                print(f"Ошибка загрузки VFS: {e}")
        else:
            print("VFS не загружена (путь не указан или файл не существует)")
        
        print()

        #выполнение стартового скрипта, если указан
        if self.config.script_path:
            self.execute_startup_script()
        
        #основной REPL цикл
        self.repl_loop()

    def execute_startup_script(self):
        #выполняем стартовый скрипт
        print(f"Выполнение стартового скрипта: {self.config.script_path}")
        try:
            with open(self.config.script_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                print(f"{self.prompt}{line}")
                success = self.execute_command(line)
                
                if not success:
                    print(f"Ошибка в строке {line_num}. Прерывание выполнения скрипта.")
                    break
                    
        except FileNotFoundError:
            print(f"Ошибка: стартовый скрипт не найден: {self.config.script_path}")
        except Exception as e:
            print(f"Ошибка выполнения стартового скрипта: {e}")

    def execute_command(self, command_line):
        #выполняет одну команду и возвращает успешность выполнения
        parts = command_line.split()
        if not parts:
            return True
            
        command = parts[0]
        args = parts[1:]
        args_str = "".join(args)
        
        if command in self.commands:
            return self.commands[command](args_str)
        else:
            print(f"Ошибка: неизвестная команда '{command}'")
            return False

    def repl_loop(self):
        #основной цикл REPL
        while True:
            try:
                user_input = input(self.prompt).strip()
                if not user_input:
                    continue
                
                self.execute_command(user_input)

            except EOFError:
                print("\nДо свидания!")
                break
            except KeyboardInterrupt:
                print("\nПрервано пользователем.")
                break

    # команды
    def cmd_exit(self, args):
        print("До свидания!")
        exit(0)
        return True

    def cmd_ls(self, args):
        path = ''.join(args) if args else '.'
        items = self.vfs.list_directory(path)
        if items is None:
            print(f"ls: {path}: Нет такой директории")
            return False
        
        for item in items:
            print(item)
        return True

    def cmd_cd(self, args):
        if not args:
            path = '/'
        else:
            path = ''.join(args)
        
        if self.vfs.change_directory(path):
            self.update_prompt()
            return True
        else:
            print(f"cd: {path}: Нет такой директории")
            return False
        
    def cmd_pwd(self, args):
        print(self.vfs.get_current_path())
        return True

    def cmd_cat(self, args):
        if not args:
            print("cat: требуется аргумент - имя файла")
            return False
        
        #объединяем все аргументы в одно имя файла
        filename = ''.join(args)
        
        #получаем текущую директорию
        current_dir = self.vfs.current_dir
        
        #ищем файл в текущей директории
        if filename in current_dir.children:
            node = current_dir.children[filename]
        else:
            #пробуем найти по абсолютному пути
            node = self.vfs.find_node(filename)
        
        if not node:
            print(f"cat: {filename}: Нет такого файла")
            return False
        if not node.is_file:
            print(f"cat: {filename}: Это директория")
            return False
        
        print(node.content)
        return True

    def cmd_conf_dump(self, args_str):
        self.config.dump()
        return True

def main():
    config = Config()
    config.load_from_args()

    emulator = Emulator(config)
    emulator.run()

if __name__ == "__main__":
    main()