import os
import shutil

user_folder = input("Введіть шлях до папки: ")
folder = user_folder

categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt"],
    "Excel": [".xlsx", ".xls", ".csv"],
    "Video": [".mp4", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".m4a"],
    "Archives": [".zip", ".rar", ".tar"],
    "Apps": [".exe", ".msi", ".apk"],
    "Books": [".epub", ".mobi", ".azw3"],
    "Code": [".py", ".js", ".css", ".html", ".json", ".xml", ".md"],
}
moved = 0  # лічильник переміщених файлів
skipped = 0  # лічильник пропущених

list_files = os.listdir(folder)

for filename in list_files:
    filepath = os.path.join(folder, filename)

    if os.path.isdir(filepath):
        continue

    file_ext = os.path.splitext(filename)[1].lower()

    for category, extensions in categories.items():
        if file_ext in extensions:
            dest_folder = os.path.join(folder, category)
            os.makedirs(dest_folder, exist_ok=True)

            try:
                shutil.move(filepath, os.path.join(dest_folder, filename))
                print(f"✓ Переміщено: {filename} → {category}")
                moved += 1
            except PermissionError:
                print(f"✗ Пропущено (файл зайнятий): {filename}")
                skipped += 1

            break

    print(f"\nГотово! Переміщено: {moved}, пропущено: {skipped}")
