import os
import yaml
import shutil

def update_files_section(yaml_data, dir_path):
    """Обновляет секцию files в YAML данных, сохраняя существующие title для файлов."""
    # Получаем список файлов в директории, исключая index.md
    current_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f != 'index.md']
    
    # Создаем словарь существующих файлов из YAML
    existing_files = {file['file']: file['title'] for file in yaml_data.get('files', [])}
    
    # Обновляем список файлов
    updated_files = []
    for file in current_files:
        # Используем существующий заголовок или создаем новый
        title = existing_files.get(file, 'Файл требует описания')
        file_info = {
            'title': title,
            'file': file
        }
        updated_files.append(file_info)
    
    # Сортируем файлы по имени для стабильного порядка
    updated_files.sort(key=lambda x: x['file'])
    
    yaml_data['files'] = updated_files
    return yaml_data

def should_update_yaml(existing_yaml, example_yaml, dir_path):
    """Проверяет, нужно ли обновлять YAML данные."""
    # Проверяем title только для новых файлов
    if not existing_yaml.get('title'):
        if existing_yaml.get('title') != example_yaml.get('title'):
            print(f"Обновление {dir_path}: отсутствует заголовок")
            return True
    
    # Проверяем tags
    existing_tags = set(existing_yaml.get('tags', []))
    example_tags = set(example_yaml.get('tags', []))
    
    # Если теги были изменены (не содержат стандартные теги), не обновляем
    if not example_tags.issubset(existing_tags):
        return False
    
    # Получаем текущий список файлов
    current_files = set(f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f != 'index.md')
    
    # Получаем список файлов из существующего YAML
    existing_files = set(file['file'] for file in existing_yaml.get('files', []))
    
    # Проверяем, есть ли различия
    if current_files != existing_files:
        print(f"Обновление {dir_path}:")
        if current_files - existing_files:
            print(f"  Добавлены: {', '.join(current_files - existing_files)}")
        if existing_files - current_files:
            print(f"  Удалены: {', '.join(existing_files - current_files)}")
        return True
    
    return False

def create_index_md_in_projects(projects_directory, example_md_path):
    """Рекурсивно обрабатывает папки в projects, создает или обновляет index.md файлы."""
    # Читаем содержимое example.md
    with open(example_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Разделяем YAML и остальной контент
        yaml_content = content.split('---')[1]
        rest_content = content.split('---')[2]
        
        # Парсим YAML
        example_yaml = yaml.safe_load(yaml_content)
    
    # Обходим все поддиректории в projects
    for root, dirs, files in os.walk(projects_directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            index_md_path = os.path.join(dir_path, 'index.md')
            
            if os.path.exists(index_md_path):
                # Если index.md существует, читаем его
                with open(index_md_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
                    existing_yaml_content = existing_content.split('---')[1]
                    existing_yaml = yaml.safe_load(existing_yaml_content)
                
                # Проверяем, нужно ли обновлять YAML
                if should_update_yaml(existing_yaml, example_yaml, dir_path):
                    # Обновляем только секцию files
                    updated_yaml = update_files_section(existing_yaml, dir_path)
                    
                    # Создаем новый контент
                    new_content = '---\n'
                    new_content += yaml.dump(updated_yaml, 
                                          allow_unicode=True, 
                                          sort_keys=False, 
                                          default_flow_style=False)
                    new_content += '---\n'
                    new_content += rest_content
                    
                    # Записываем обновленный файл
                    with open(index_md_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Обновлен файл: {index_md_path} (обновлена секция files)")
            else:
                # Создаем новый index.md
                yaml_data = example_yaml.copy()
                yaml_data = update_files_section(yaml_data, dir_path)
                
                new_content = '---\n'
                new_content += yaml.dump(yaml_data, 
                                      allow_unicode=True, 
                                      sort_keys=False, 
                                      default_flow_style=False)
                new_content += '---\n'
                new_content += rest_content
                
                with open(index_md_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Создан файл: {index_md_path}")

if __name__ == "__main__":
    projects_directory = "./projects"
    example_md_path = "./example.md"
    
    if not os.path.exists(projects_directory):
        print(f"Директория {projects_directory} не существует!")
    elif not os.path.exists(example_md_path):
        print(f"Файл {example_md_path} не существует!")
    else:
        print(f"Начинаем создание/обновление index.md файлов в {projects_directory}...")
        create_index_md_in_projects(projects_directory, example_md_path) 