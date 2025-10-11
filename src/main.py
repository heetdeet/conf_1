import os
import getpass
import socket

def main():
    username = getpass.getuser()
    hostname = socket.gethostname()
    prompt = f"{username}@{hostname}:~$ "

    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]
            args_str = "".join(args)

            if command == "exit":
                print("До свидания!")
                break
            elif command == "ls":
                print(f"ls: {args_str}")
            elif command == "cd":
                print(f"cd: {args_str}")
            else:
                print(f"Ошибка: неизвестная команда '{command}'")

        except EOFError:
            print("\nДо свидания!")
            break
        except KeyboardInterrupt:
            print("\nПрервано пользователем.")
            break

if __name__ == "__main__":
    main()