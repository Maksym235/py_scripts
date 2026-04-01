import os


def search_in_file(filepath, query):
    results = []
    lines = []  # одразу задаємо порожній список — тепер lines завжди визначена

    for encoding in ["utf-8", "cp1251", "latin-1"]:
        try:
            with open(filepath, "r", encoding=encoding) as f:
                lines = f.readlines()
            break
        except UnicodeDecodeError:
            continue

    for line_number, line in enumerate(lines, start=1):
        if query.lower() in line.lower():
            results.append({"line": line_number, "text": line.strip()})

    return results


def search_in_folder(folder, query):
    if not os.path.exists(folder):
        print(f"Папка '{folder}' не існує.")
        return False

    found_any = False  # чи знайшли хоч щось
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isdir(filepath):
            search_in_folder(filepath, query)
            found_any = True
        else:
            if not filename.endswith(".txt") and not filename.endswith(".md"):
                continue

            filepath = os.path.join(folder, filename)
            results = search_in_file(filepath, query)

            if results:
                found_any = True
                print(f"📄 {filepath}:")
                for result in results:
                    print(f"   Рядок {result['line']}: {result['text']}")
                print()

        # Беремо тільки .txt файли
        # if not filename.endswith(".txt") and not filename.endswith(".md"):
        #     continue

        # filepath = os.path.join(folder, filename)
        # results = search_in_file(filepath, query)

        # if results:
        #     found_any = True
        #     print(f"📄 {filename}:")
        #     for result in results:
        #         print(f"   Рядок {result['line']}: {result['text']}")
        #     print()

    return found_any


# --- Запускаємо ---
folder = r"D:\repo\obs_v3"  # зміни на свою папку
query = input("Що шукаємо? ")  # input() питає користувача і чекає відповідь

print(f"\nШукаю '{query}' у папці: {folder}\n")

if not search_in_folder(folder, query):
    print("Нічого не знайдено.")
