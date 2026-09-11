import os

import pytest

from src.decorators import log


@log()
def add(x: int, y: int) -> int:
    """Тестовая функция сложения"""
    return x + y


@log()
def divide(x: int, y: int) -> float:
    """Тестовая функция деления для генерации ошибок"""
    return x / y


@log(filename="test_log.txt")
def add_to_file(x: int, y: int) -> int:
    """Тестовая функция для записи в файл"""
    return x + y


@log(filename="test_log.txt")
def divide_to_file(x: int, y: int) -> float:
    """Тестовая функция деления для записи ошибок в файл"""
    return x / y


def test_log_console_success(capsys: pytest.CaptureFixture) -> None:
    """Тест успешного выполнения функции с выводом в консоль"""
    assert add(1, 2) == 3
    captured = capsys.readouterr()
    assert captured.out.strip() == "add ok"


def test_log_console_error(capsys: pytest.CaptureFixture) -> None:
    """Тест логирования ошибки в консоль"""
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError. Inputs: (1, 0), {}" in captured.out.strip()


def test_log_file_success() -> None:
    """Тест успешного выполнения функции с записью в файл"""
    filename = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)

    assert add_to_file(2, 3) == 5

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == "add_to_file ok"
    os.remove(filename)


def test_log_file_error() -> None:
    """Тест логирования ошибки в файл"""
    filename = "test_log.txt"
    if os.path.exists(filename):
        os.remove(filename)

    with pytest.raises(ZeroDivisionError):
        divide_to_file(5, 0)

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert "divide_to_file error: ZeroDivisionError. Inputs: (5, 0), {}" in content
    os.remove(filename)
