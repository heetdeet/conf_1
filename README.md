# conf_1
# Эмулятор командной оболочки ОС

## Вариант №16

Эмулятор командной строки UNIX-подобной операционной системы с виртуальной файловой системой.

---

## Этап 1: Базовая оболочка REPL

Реализована базовая интерактивная оболочка (Read-Eval-Print Loop) с поддержкой основных команд.

### Функциональность:
- **Интерактивный режим** с приглашением `username@hostname:~$ `
- **Базовые команды**: `ls`, `cd`, `exit`
- **Обработка ошибок**: неизвестные команды, неверные аргументы
- **Заглушки команд**: вывод имени команды и аргументов

### Использование:
```bash
python main.py
```

### Пример работы:
```
user@host:~$ ls
ls:
user@host:~$ cd /home
cd: /home
user@host:~$ unknown
Ошибка: неизвестная команда 'unknown'
user@host:~$ exit
До свидания!
```

---

## Этап 2: Система конфигурации

Реализована гибкая система конфигурации с поддержкой параметров командной строки и конфигурационных файлов.

### Функциональность:
- **Параметры командной строки**:
  - `--vfs-path` - путь к VFS
  - `--script-path` - путь к стартовому скрипту
  - `--config-path` - путь к конфигурационному файлу
- **Конфигурационные файлы TOML**
- **Приоритет конфигурации**: командная строка > файл конфигурации
- **Стартовые скрипты** с остановкой при первой ошибке
- **Команда `conf-dump`** для отображения текущей конфигурации
- **Тестовые скрипты** для Windows (BAT)

### Использование:
```bash
# С конфигурационным файлом
python main.py --config-path config.toml

# С параметрами командной строки
python main.py --vfs-path .custom_vfs --script-path ./custom_script.txt

# Комбинация (приоритет у командной строки)
python main.py --config-path config.toml --vfs-path ./override_vfs

# Тестирование
script.bat
```

### Структура конфигурационного файла (TOML):
```toml
vfs_path = "./vfs"
script_path = "./script.txt"
```

### Пример стартового скрипта:
```txt
# Стартовый скрипт
ls
cd /home
conf-dump
exit
```

---

## Этап 3: Виртуальная файловая система (VFS)

Реализована виртуальная файловая система, работающая полностью в памяти с загрузкой из JSON-файлов.

### Функциональность:
- **Загрузка из JSON** с поддержкой структур любой сложности
- **Многоуровневая структура** директорий и файлов
- **Base64 кодирование** для бинарных данных
- **Полная навигация**: `ls`, `cd`, `pwd`, `cat`
- **Обработка ошибок**: несуществующие файлы, ошибки загрузки VFS
- **Работа в памяти** без модификации исходных данных

### Использование:
```bash
# С простой VFS
python main.py --vfs-path vfs_simple.json --script-path startup_script_vfs.txt

# С многоуровневой VFS
python main.py --vfs-path vfs_multilevel.json --script-path startup_script_vfs.txt

# С несуществующей VFS
python main.py --vfs-path not_exists.json

# Тестирование
test_vfs.bat
```

### Структура JSON VFS:
```json
{
  "home": {
    "type": "directory",
    "children": {
      "user": {
        "type": "directory",
        "children": {
          "documents": {
            "type": "directory",
            "children": {
              "file.txt": {
                "type": "file",
                "content": "Текст файла",
                "encoding": "base64",
                "content_base64": "0J7RgtC/0YDQsNCy0LvQtdC90LjQtQ=="
              }
            }
          }
        }
      }
    }
  }
}
```

### Пример работы с VFS:
```
user@host:/$ ls /
home 
etc 
README.txt
user@host:/$ cd home/user/documents
user@host:/home/user/documents$ ls
file1.txt 
file2.txt
user@host:/home/user/documents$ cat file1.txt
Содержимое файла
user@host:/home/user/documents$ pwd
/home/user/documents
```

---

## История разработки

- **Этап 1**: Базовая оболочка REPL
- **Этап 2**: Система конфигурации  
- **Этап 3**: Виртуальная файловая система