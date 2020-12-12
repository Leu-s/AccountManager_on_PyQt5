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

    # Creating the list with valid characters
    valid_characters = [symbol for symbol in low_register if low_reg],\
                       [symbol for symbol in high_register if high_reg],\
                       [symbol for symbol in numbers if num],\
                       [symbol for symbol in specially_symbols if s_symbols]
    valid_characters = [i for i in valid_characters for i in i]

    # Checking the list with valid characters to lowercase and uppercase symbols or numbers
    if low_reg == high_reg == num is False:
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
                password[0] = random.choice(low_register+high_register+numbers)
            if password[s_amount-1] == '_':
                password[s_amount-1] = random.choice(low_register+high_register+numbers)
            else:
                if '_' not in password:
                    password[random.randint(1, s_amount-2)] = '_'

    return ''.join(password)


def password_security_check(password):
    """
    The function checks the password for strength.


    :param password: str() - Password received from the user
    :return: True if the password is strong, otherwise Falls + recommended password
    """
    global low_register, high_register, numbers
    secure = 0
    password = [i for i in password]
    recommended_password = []

    # Checking if all characters are correct
    for i in password:
        if i not in low_register+high_register+numbers+specially_symbols:
            password[password.index(i)] = random.choice(low_register+high_register+numbers)
            secure += 1

    # Add random characters if password length is less than six.
    if len(password) < 6:
        for i in range(6-len(password)):
            recommended_password.append(random.choice(low_register+high_register+numbers))
        else:
            secure += 1
            password += recommended_password
            if specially_symbols not in password:
                password[random.randint(1, len(password)-2)] = specially_symbols[0]

    if password[0] == specially_symbols[0]:
        password[0] = random.choice(low_register+high_register+numbers)
        secure += 1

    if password[::-1][0] == specially_symbols[0]:
        password[::-1].remove(specially_symbols[0])
        password.append(random.choice(low_register + high_register + numbers))
        secure += 1

    for i, j in enumerate(password):
        if j == password[i-1] == specially_symbols[0]:
            password[i] = random.choice(low_register + high_register + numbers)
            secure += 1

    return [secure == 0, ''.join(password)]

