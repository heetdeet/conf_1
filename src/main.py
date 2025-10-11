import os
import getpass
import socket
from config import Config

class Emulator:
    def __init__(self, config):
        self.config = config
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.prompt = f"{self.username}@{self.hostname}:~$ "
        self.commands = {
            'exit': self.cmd_exit,
            'ls': self.cmd_ls,
            'cd': self.cmd_cd,
            'conf-dump': self.cmd_conf_dump,
        }

    def run(self):
        #запускает эмулятор
        #отладочный вывод конфигурации при старте
        print("=== Отладочный вывод конфигурации ===")
        self.config.dump()
        print("=====================================")
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
    def cmd_exit(self, args_str):
        print("До свидания!")
        exit(0)
        return True

    def cmd_ls(self, args_str):
        print(f"ls: {args_str}")
        return True

    def cmd_cd(self, args_str):
        print(f"cd: {args_str}")
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