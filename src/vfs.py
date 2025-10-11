import json
import base64
import os
from pathlib import Path

class VFSNode:
    # узел виртуальной файловой системы
    def __init__(self, name, is_file=False, content=None, permissions='644'): 
        self.name = name
        self.is_file = is_file
        self.content = content or ""
        self.permissions = permissions
        self.children = {}  # для директорий
        self.parent = None

    def add_child(self, node):
        #добавляет дочерний узел
        node.parent = self
        self.children[node.name] = node

    def get_path(self):
        #возвращает полный пу ть к узлу
        path_parts = []
        current = self
        while current and current.name:
            path_parts.append(current.name)
            current = current.parent
        return '/' + '/'.join(reversed(path_parts))

class VFS:
    #виртуальная файловая система
    def __init__(self):
        self.root = VFSNode("")
        self.current_dir = self.root

    def load_from_json(self, filepath):
        #загружает VFS из JSON файла
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._build_from_dict(data, self.root)
            print(f"VFS загружена из {filepath}")
            
        except FileNotFoundError:
            raise Exception(f"Файл VFS не найден: {filepath}")
        except json.JSONDecodeError:
            raise Exception(f"Неверный формат JSON в файле: {filepath}")
        except Exception as e:
            raise Exception(f"Ошибка загрузки VFS: {e}")

    def _build_from_dict(self, data, parent_node):
        #рекурсивно строит VFS из словаря
        for name, node_data in data.items():
            if isinstance(node_data, dict) and 'type' in node_data:
                # файл или директория
                if node_data['type'] == 'file':
                    content = node_data.get('content', '')
                    # декодируем base64 если нужно
                    if node_data.get('encoding') == 'base64':
                        content = base64.b64decode(content).decode('utf-8')
                    
                    new_node = VFSNode(
                        name, 
                        is_file=True, 
                        content=content,
                        permissions=node_data.get('permissions', '644') # чтение+запись для владельца, для групп и пользователя только чтение
                    )
                    parent_node.add_child(new_node)
                    
                elif node_data['type'] == 'directory':
                    new_node = VFSNode(name, permissions=node_data.get('permissions', '755')) # чтение+запись+выполнение для владельца, для групп и пользователя только чтение+выполнение
                    parent_node.add_child(new_node)
                    if 'children' in node_data:
                        self._build_from_dict(node_data['children'], new_node)
            else:
                # простой файл (строка как содержимое)
                new_node = VFSNode(name, is_file=True, content=str(node_data))
                parent_node.add_child(new_node)

    def find_node(self, path):
        #находит узел по пути
        if path == '/':
            return self.root
            
        path = path.strip('/')
        parts = path.split('/')
        current = self.current_dir if not path.startswith('/') else self.root
        
        for part in parts:
            if part == '..':
                current = current.parent if current.parent else self.root
            elif part == '.':
                continue
            elif part in current.children:
                current = current.children[part]
            else:
                return None
        return current

    def list_directory(self, path='.'):
        # список содержимого директории
        target = self.find_node(path) if path != '.' else self.current_dir
        if not target or target.is_file:
            return None
        
        return [node.name for node in target.children.values()]

    def change_directory(self, path):
        # изменяет текущую директорию
        target = self.find_node(path)
        if not target:
            return False
        if target.is_file:
            return False
        
        self.current_dir = target
        return True

    def get_current_path(self):
        #возвращает текущий путь
        return self.current_dir.get_path()