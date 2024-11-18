# О проекте

Консольное приложение, эмулирующее работу ассемблера и интерпретатора.

# 1. Клонирование репозитория

Склонируйте репозиторий с исходным кодом и тестами:

```bash
git clone <URL репозитория>
cd <директория проекта>
```

# 2. Виртуальное окружение

```shell
python -m venv venv
venv\Scripts\activate
```

# 3. Установка зависимостей

```shell
pip install -r requirements.txt
```

# 4. Запуск программы

Ассемблер:

```shell
py main.py assemble <assembler_code> <output_file> <log_file>
```

Интерпретатор:

```shell
py main.py interpret <bin_file> <limitation>
```

# 5. Тестирование

Для запуска тестирования необходимо запустить следующий скрипт:

```shell
pytest -v
```

Для генерации отчета о покрытии тестами необходимо выполнить команду:

```shell
coverage run --branch -m pytest test_assembler.py
```

Просмотр результатов покрытия:

```shell
coverage report
```