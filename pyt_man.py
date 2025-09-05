import os
import subprocess
import json

PYTHON_CMD = "python"  # используем системную команду python

def run_pip(args):
    """Запускаем pip как модуль с нужными аргументами."""
    cmd = [PYTHON_CMD, "-m", "pip"] + args
    print("\n>", " ".join(cmd))
    try:
        return subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\nОперация прервана пользователем.")
    except Exception as e:
        print(f"Ошибка запуска pip: {e}")

def list_installed():
    run_pip(["list"])

def list_outdated():
    run_pip(["list", "--outdated"])

def install_package(name):
    if not name:
        print("Не указано имя пакета.")
        return
    run_pip(["install", name])

def uninstall_package(name):
    if not name:
        print("Не указано имя пакета.")
        return
    run_pip(["uninstall", "-y", name])

def upgrade_package(name):
    if not name:
        print("Не указано имя пакета.")
        return
    run_pip(["install", "--upgrade", name])

def upgrade_all():
    print("Поиск устаревших пакетов...")
    try:
        res = subprocess.run(
            [PYTHON_CMD, "-m", "pip", "list", "--outdated", "--format=json"],
            capture_output=True, text=True, check=False
        )
        if res.returncode != 0:
            print(res.stdout)
            print(res.stderr)
            print("Не удалось получить список устаревших пакетов.")
            return
        data = json.loads(res.stdout or "[]")
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    if not data:
        print("Все пакеты актуальны.")
        return

    for item in data:
        name = item.get("name")
        cur = item.get("version")
        new = item.get("latest_version") or item.get("latest")
        print(f"\nОбновление {name}: {cur} → {new}")
        run_pip(["install", "--upgrade", name])

def ensure_pip():
    # проверка, что команда python существует
    if os.system(f"{PYTHON_CMD} --version") != 0:
        print("Python не найден в системе.")
        return False
    run_pip(["--version"])
    return True

def menu():
    print("\n=== Python Package Manager (pip) ===")
    print("1) Установить пакет")
    print("2) Удалить пакет")
    print("3) Обновить пакет")
    print("4) Обновить все устаревшие")
    print("5) Список установленных")
    print("6) Список устаревших")
    print("7) Выход")

def main():
    if not ensure_pip():
        return
    while True:
        menu()
        choice = input("\nВыберите операцию [1-7]: ").strip()
        if choice == "1":
            name = input("Введите имя пакета для установки: ").strip()
            install_package(name)
        elif choice == "2":
            name = input("Введите имя пакета для удаления: ").strip()
            uninstall_package(name)
        elif choice == "3":
            name = input("Введите имя пакета для обновления: ").strip()
            upgrade_package(name)
        elif choice == "4":
            upgrade_all()
        elif choice == "5":
            list_installed()
        elif choice == "6":
            list_outdated()
        elif choice == "7":
            print("Выход.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
