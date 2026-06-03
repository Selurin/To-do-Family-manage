import os
import sys
import uvicorn

if __name__ == "__main__":
    # Учитываем двойную вложенность: backend/app
    target_dir = os.path.abspath(os.path.join("backend", "app"))
    
    # Добавляем именно эту целевую папку в пути поиска модулей
    sys.path.insert(0, target_dir)
    os.chdir(target_dir)
    
    # Теперь Python гарантированно увидит main.py и все соседние файлы
    from main import app
    
    uvicorn.run(app, host="0.0.0.0", port=80)
