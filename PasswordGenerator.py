import random

low_register = 'abcdefghijklmnopqrstuvwxyz'
high_register = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '1234567890'
specially_symbols = '_____'


def create_password(s_amount=8, num=False, low_reg=False, high_reg=False, s_symbols=False):
    """
    The function allows you to generate passwords with the specified parameters.

    :param s_amount: Number of characters
    :param num: Numbers
    :param low_reg: Lowercase characters
    :param high_reg: Uppercase characters
    :param s_symbols: Special symbols
    :return: Ready password in string format
    """

    global low_register, high_register, numbers, specially_symbols
    password = []
    # Создаем список с допустимыми символами
    valid_characters = [symbol for symbol in low_register if low_reg],\
                       [symbol for symbol in high_register if high_reg],\
                       [symbol for symbol in numbers if num],\
                       [symbol for symbol in specially_symbols if s_symbols]
    valid_characters = [i for i in valid_characters for i in i]

    if not valid_characters or len(valid_characters) == 5:
        return 'Select characters or number to start!'

    for i in range(s_amount):
        s = random.choice(valid_characters)
        try:
            if password[::-1][0] == '_' and s == '_':
                s = random.choice(valid_characters[:-len(specially_symbols)])
        except IndexError:
            pass
        password.append(s)
    else:
        if s_symbols:
            if password[0] == '_':
                password[0] = random.choice(valid_characters[:-1])
            if password[s_amount-1] == '_':
                password[s_amount-1] = random.choice(valid_characters[:-1])
            else:
                if '_' not in password:
                    password[random.randint(1, s_amount-2)] = '_'
    return ''.join(password)
