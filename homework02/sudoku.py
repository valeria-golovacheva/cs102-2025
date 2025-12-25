"""Sudoku solver and generator."""

import pathlib
import random
import typing as tp

T = tp.TypeVar("T")
DIGITS = set("123456789")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> list[list[str]]:
    """Прочитать судоку из файла и вернуть сетку 9×9."""
    path = pathlib.Path(path)
    with path.open(encoding="utf-8") as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> list[list[str]]:
    """Создать двумерную сетку судоку из строки puzzle."""
    digits = [c for c in puzzle if c in "123456789."]
    # Заполняем недостающие элементы точками
    digits += ["."] * (81 - len(digits))
    return group(digits, 9)


def display(grid: list[list[str]]) -> None:
    """Вывести судоку на экран в читаемом виде."""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if col in (2, 5) else "") for col in range(9)))
        if row in (2, 5):
            print(line)
    print()


def group(values: list[T], n: int) -> list[list[T]]:
    """Сгруппировать список values в подсписки по n элементов."""
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: list[list[str]], pos: tuple[int, int]) -> list[str]:
    """Вернуть значения строки судоку для позиции pos."""
    row, _ = pos
    return grid[row]


def get_col(grid: list[list[str]], pos: tuple[int, int]) -> list[str]:
    """Вернуть столбец судоку для позиции pos."""
    _, col = pos
    return [grid[row][col] for row in range(len(grid)) if col < len(grid[row])]


def get_block(grid: list[list[str]], pos: tuple[int, int]) -> list[str]:
    """Вернуть значения 3×3 блока, содержащего позицию pos."""
    row, col = pos
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    return [grid[r][c] for r in range(start_row, start_row + 3) for c in range(start_col, start_col + 3)]


def find_empty_positions(grid: list[list[str]]) -> tp.Optional[tuple[int, int]]:
    """Найти первую пустую ячейку в судоку."""
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ".":
                return row, col
    return None


def find_possible_values(grid: list[list[str]], pos: tuple[int, int]) -> set[str]:
    """Вернуть множество допустимых значений для позиции pos."""
    used = set(get_row(grid, pos)) | set(get_col(grid, pos)) | set(get_block(grid, pos))
    return DIGITS - used


def solve(grid: list[list[str]]) -> tp.Optional[list[list[str]]]:
    """Решить судоку методом рекурсивного бэктрекинга."""
    empty = find_empty_positions(grid)
    if empty is None:
        return grid

    row, col = empty
    for value in find_possible_values(grid, empty):
        grid[row][col] = value
        if solve(grid):
            return grid
        grid[row][col] = "."

    return None


def check_solution(solution: tp.Optional[list[list[str]]]) -> bool:
    """Проверить корректность решения судоку."""
    if solution is None:
        return False
    for i in range(9):
        if set(solution[i]) != DIGITS:
            return False
        if set(row[i] for row in solution) != DIGITS:
            return False

    for row in (0, 3, 6):
        for col in (0, 3, 6):
            block = [solution[r][c] for r in range(row, row + 3) for c in range(col, col + 3)]
            if set(block) != DIGITS:
                return False
    return True


def generate_sudoku(n: int) -> list[list[str]]:
    """Сгенерировать судоку с n заполненными клетками."""
    grid = [["." for _ in range(9)] for _ in range(9)]
    solve(grid)

    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    for r, c in cells[: 81 - n]:
        grid[r][c] = "."

    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
