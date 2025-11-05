def encrypt_affine(plaintext, a, b):
    """
    Шифрует текст с помощью аффинного шифра.

    Аффинный шифр использует формулу: E(x) = (a*x + b) % m,
    где x - позиция буквы в алфавите, m - количество букв в алфавите (26 для английского).

    Аргументы:
        plaintext (str): Исходный текст для шифрования
        a (int): Первый ключ шифрования (должен быть взаимно прост с 26)
        b (int): Второй ключ шифрования

    Возвращает:
        str: Зашифрованный текст
    """
    m = 26  # кол-во букв в английском алфавите
    result = []

    for char in plaintext:
        if char.isalpha():
            upper_char = char.upper()
            x = ord(upper_char) - ord("A")
            encrypted_pos = (a * x + b) % m
            encrypted_char = chr(encrypted_pos + ord("A"))
            result.append(encrypted_char if char.isupper() else encrypted_char.lower())
        else:
            result.append(char)

    return "".join(result)
