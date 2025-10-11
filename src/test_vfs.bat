@echo off
chcp 65001 > nul

echo Тестирование с простой VFS:
python main.py --vfs-path vfs_simple.json --script-path startup_script_vfs.txt

echo.
echo Тестирование с многоуровневой VFS:
python main.py --vfs-path vfs_multilevel.json --script-path startup_script_vfs.txt

echo.
echo Тестирование с несуществующей VFS:
python main.py --vfs-path not_exists.json

pause