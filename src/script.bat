@echo off
chcp 65001 > nul
echo Тестирование с конфигурационным файлом
python main.py --config-path config.toml

echo.
echo Тестирование с параметрами командной строки
python main.py --vfs-path .custom_vfs --script-path ./custom_script.txt

echo.
echo Тестирование с приоритетом командной строки
python main.py --config-path config.toml --vfs-path ./override_vfs

echo.
echo Тестирование без параметров
python main.py

pause