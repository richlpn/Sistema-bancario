import getpass
from typing import Any, List

from models.User import User, UserSettings

verified_user: User = None


def __clear_terminal():
    for _ in range(2):
        print()


def __show_users():
    print(User.all())


def get_name_input(name_txt_input="Digite um nome de usuario valido: ") -> str:
    username = ""
    while UserSettings.MIN_NAME_LENGTH > len(username) < UserSettings.MAX_NAME_LENGTH:
        username = input(name_txt_input)
    return username


def get_valid_value(txt_input: str) -> float:
    while 1:
        value = input(txt_input)
        try:
            value = float(value)
            break
        except Exception:
            print("Valor invalido!!!")
    return value


def get_password_input(pass_txt_input="Digite uma senha valida: ") -> str:
    password = ""
    while UserSettings.MIN_PASSWORD_LENGTH > len(password) < UserSettings.MAX_PASSWORD_LENGTH:
        password = getpass.getpass(pass_txt_input)
    return password


def login_user() -> bool:
    """:returns false if the login process failed"""

    username = get_name_input()
    password = get_password_input()

    users = User.filter(name=username)

    if len(users) == 0:
        print('debug ONE!!!')
        return False

    for user in users:

        if user.verify_password(password):
            break

        globals()['verified_user'] = user

        print("Logado com sucesso!!!")
        return True
    print("nome ou senha invalidas")
    return False

def register_user() -> Any:
    option = input("Digite 1 para continuar:")
    if option != '1':
        return
    user = User()
    user.name = get_name_input()
    user.password = get_password_input()
    user.save()
    print("Registrado com sucesso!!!")

def logoff_user() -> bool:
    user: User = globals()["verified_user"]

    if user is None: return False

    print(f"Até mais {user.name}")
    user.save()
    globals()["verified_user"] = None

    return True


def deposit():
    value = get_valid_value("Digite o valor a ser depositado: ")

    try:
        print(verified_user.deposit(value))
        print("Transação finalizada com exito!!!")
    except Exception:
        print("Um erro ocorreu durante a transação!\nTente novamente!!!")
    verified_user.save()


def withdraw():
    value = get_valid_value("Digite o valor a ser a ser sacado: ")

    try:
        print(verified_user.withdraw(value))
        print("Transação finalizada com exito!!!")
    except Exception:
        print("Um erro ocorreu durante a transação!\nTente novamente!!!")
    verified_user.save()


def transfer():
    user: List[User] = User.filter(name=get_name_input())
    value = get_valid_value("Digite o valor a ser transferido: ")
    if len(user) == 0:
        print("usuaŕio invalido ou inexistente")
        return
    try:
        verified_user.transfer(value, user[0])
        print("Transferencia executada com exito!")
    except Exception:
        print("Um erro ocorreu tente novamente!")

    verified_user.save()
    user[0].save()


def user_menu():
    __clear_terminal()
    user = globals()["verified_user"]
    print(f"Olá {verified_user.name}")
    menu_text = "Escolha uma das operações a seguir\n" \
                "1-Mostrar transações\n" \
                "2-Depositar\n" \
                "3-Sacar\n" \
                "4-transferir\n" \
                "5-Ver Saldo\n" \
                "0-sair"
    option = -1
    while option != 0:
        print(menu_text)
        try:
            option = int((input("Operação: ")))
        except ValueError as err:
            print("Operação invalida!!!")
            continue
        if option == 1:
            for t in verified_user.transactions:
                print(t)
        elif option == 2:
            deposit()
        elif option == 3:
            withdraw()
        elif option == 4:
            transfer()
        elif option == 5:
            print(f"Usuário: {user.name}\nSaldo: R${user.balance}")
    logoff_user()


def change_password() -> bool:
    """:return False if the username informed is invalid"""
    username = get_name_input()
    password = get_password_input("Digite a nova senha: ")
    user = User.filter(name=username)

    if len(user) <= 0:
        return False

    user = user[0]
    user.password = password

    user.validate_user()
    user.save()

    print("Senha alterada com sucesso!!!")


def main_menu():
    menu_text = "Escolha uma das operações a seguir\n" \
                "1-Login\n" \
                "2-Criar Conta\n" \
                "3-Esqueceu senha\n" \
                "0-Sair"
    option: int = -1

    while option != 0:
        print(menu_text)
        print("->", end=" ")
        try:
            option = int((input()))
        except ValueError:
            print("Operação invalida!!!")
            continue
        if option == 1:
            # Loging User
            if login_user():
                user_menu()
        elif option == 2:
            register_user()
        elif option == 3:
            change_password()
        elif option == 5:
            __show_users()


print("Finalizado com sucesso!!!")


def main():
    main_menu()


if __name__ == "__main__":
    main()
