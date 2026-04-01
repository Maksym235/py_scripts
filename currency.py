from datetime import datetime  # для отримання поточної дати

import openpyxl
import requests


def get_rates():
    # Безкоштовне API Національного банку України
    today = datetime.now().strftime("%Y%m%d")
    url = (
        f"https://bank.gov.ua/NBU_Exchange/exchange_site?start={today}&end={today}&json"
    )

    print("Отримую курси валют від НБУ...")
    response = requests.get(url)

    # Перевіряємо чи запит успішний (200 = OK)
    if response.status_code != 200:
        print(f"Помилка запиту: {response.status_code}")
        return []
    return response.json()  # повертає список словників


def print_rates(rates, currencies=None):
    # currencies — список валют які хочемо показати
    # якщо не вказано — показуємо всі
    print(f"\n{'Валюта':<10} {'Назва':<30} {'Курс':>10}")
    print("-" * 52)

    for rate in rates:
        code = rate["cc"]  # код валюти: USD, EUR...
        name = rate["txt"]  # назва: Долар США...
        value = rate["rate"]  # курс до гривні

        # Якщо фільтр є — пропускаємо непотрібні
        if currencies and code not in currencies:
            continue

        print(f"{code:<10} {name:<30} {value:>10.2f}")


def save_to_excel(rates, filepath):
    wb = openpyxl.Workbook()
    ws = wb.active
    assert ws is not None
    ws.title = "Курси валют"

    ws.append(["Код", "Назва", "Курс", "Дата"])

    today = datetime.now().strftime("%d.%m.%Y")  # поточна дата

    for rate in rates:
        ws.append([rate["cc"], rate["txt"], rate["rate"], today])

    wb.save(filepath)
    print(f"\n✓ Збережено у {filepath}")


# --- Запускаємо ---
rates = get_rates()

if rates:
    # Показуємо тільки популярні валюти
    print_rates(rates, currencies=["USD", "EUR", "GBP", "PLN", "CHF"])

    # Зберігаємо всі валюти в Excel
    save_to_excel(rates, "currency_rates.xlsx")
