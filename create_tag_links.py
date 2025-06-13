import os
import yaml
from pathlib import Path

def get_tags_from_index_md(index_md_path):
    """Извлекает теги из YAML-секции index.md файла."""
    try:
        with open(index_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Разделяем YAML и остальной контент
            yaml_content = content.split('---')[1]
            # Парсим YAML
            yaml_data = yaml.safe_load(yaml_content)
            return yaml_data.get('tags', [])
    except Exception as e:
        print(f"Ошибка при чтении {index_md_path}: {e}")
        return []

def create_tag_links(projects_dir, bytags_dir):
    """Создает символические ссылки в директории bytags на основе тегов."""
    # Создаем словарь для хранения связей тег -> директории
    tag_to_dirs = {}
    
    # Обходим все поддиректории в projects
    for root, dirs, files in os.walk(projects_dir):
        if 'index.md' in files:
            index_md_path = os.path.join(root, 'index.md')
            tags = get_tags_from_index_md(index_md_path)
            
            # Добавляем директорию в список для каждого тега
            for tag in tags:
                if tag not in tag_to_dirs:
                    tag_to_dirs[tag] = []
                tag_to_dirs[tag].append(root)
    
    # Создаем директорию bytags, если её нет
    os.makedirs(bytags_dir, exist_ok=True)
    
    # Создаем поддиректории для тегов и символические ссылки
    for tag, dirs in tag_to_dirs.items():
        # Создаем поддиректорию для тега
        tag_dir = os.path.join(bytags_dir, tag)
        os.makedirs(tag_dir, exist_ok=True)
        
        # Создаем символические ссылки
        for dir_path in dirs:
            # Получаем имя директории для символической ссылки
            dir_name = os.path.basename(dir_path)
            link_path = os.path.join(tag_dir, dir_name)
            
            # Создаем относительный путь для символической ссылки
            rel_path = os.path.relpath(dir_path, tag_dir)
            
            # Если символическая ссылка уже существует, удаляем её
            if os.path.exists(link_path):
                os.remove(link_path)
            
            try:
                # Создаем символическую ссылку
                os.symlink(rel_path, link_path, target_is_directory=True)
                print(f"Создана ссылка: {link_path} -> {rel_path}")
            except Exception as e:
                print(f"Ошибка при создании ссылки {link_path}: {e}")

if __name__ == "__main__":
    projects_directory = "./projects"
    bytags_directory = "./bytags"
    
    if not os.path.exists(projects_directory):
        print(f"Директория {projects_directory} не существует!")
    else:
        print(f"Начинаем создание символических ссылок в {bytags_directory}...")
        create_tag_links(projects_directory, bytags_directory)
        print("Готово!") 