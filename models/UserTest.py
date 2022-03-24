import unittest

import User as users

User = users.User
class UserTest(unittest.TestCase):
    user_name = "Teste"
    user_password = "password"
    class_object = User

    def test_create_user(self):
        user = User(name=self.user_name, password=self.user_password)
        self.assertEqual(user.name, self.user_name, msg="Erro ao criar Usuário")  # add assertion here
        self.assertEqual(user.password, self.user_password, msg="Erro ao criar Usuário")  # add assertion here
        user.save()

    def test_load_user(self):
        user = User(name=self.user_name, password=self.user_password)
        user.save()
        self.assertEqual(type(User.get(name=self.user_name)), User, "Tipo retornado do método get Invalido")
        self.assertEqual(type(User.get(name=self.user_name)), self.class_object,
                         "Tipo contido na lista retornada do método get Invalido")

    def test_delete_user(self):
        self.assertEqual(User.get(name=self.user_name).delete(), True, "Erro ao deletar usuario")

    def test_verify_password(self):
        user = User(name=self.user_name, password=self.user_password)
        user.save()
        self.assertEqual(user.verify_password(self.user_password), True)


if __name__ == '__main__':
    unittest.main()
