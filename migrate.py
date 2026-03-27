import os
import shutil

# Move src/app to app
if os.path.exists("src/app"):
    if os.path.exists("app"):
        shutil.rmtree("app")
    shutil.move("src/app", "app")

if os.path.exists("src"):
    shutil.rmtree("src")

# Find and replace in text files
def replace_in_file(path):
    if not os.path.exists(path): return
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    changed = False
    
    if "src.app" in data:
        data = data.replace("src.app", "app")
        changed = True

    # Strip DB fallback in utils/database.py
    if path.endswith("database.py") and "postgresql+asyncpg://" in data:
        # replace the fallback block
        import re
        data = re.sub(r'DATABASE_URL\s*=\s*os\.getenv\("DATABASE_URL".*\)', 
                      'DATABASE_URL = os.environ["DATABASE_URL"]', data)
        changed = True

    # Strip Redis fallback in routers/wallet.py and middleware.py
    if (path.endswith("wallet.py") or path.endswith("middleware.py") or path.endswith("scheduler.py")) and "redis://" in data:
        import re
        data = re.sub(r'REDIS_URL\s*=\s*os\.getenv\("REDIS_URL".*\)', 
                      'REDIS_URL = os.environ["REDIS_URL"]', data)
        changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

for root, _, files in os.walk("app"):
    for file in files:
        if file.endswith(".py"):
            replace_in_file(os.path.join(root, file))

for root, _, files in os.walk("tests"):
    for file in files:
        if file.endswith(".py"):
            replace_in_file(os.path.join(root, file))

if os.path.exists("render.yaml"):
    replace_in_file("render.yaml")
