import requests

BASE_URL = 'http://127.0.0.1:8000'


def loggin(user):
    """Функция принимет словарь с ключами username и password,
    вернет токен, либо ошибку авторизации"""

    response = requests.post(url=f'{BASE_URL}/login',json=user)
    if response.status_code == 200:
        print('Твой токен:\n', response.json())
        return response.json()['token']
    else:
        print('Ошибка авторизации', response.text)

def get_salary_info(token):
    """Функция принимет токен,
       вернет либо инфу по ЗП, либо ошибку токена"""

    response = requests.get(url=f'{BASE_URL}/salary_info',
                            headers={'Authorization': f'Bearer {token}'})
    if response.status_code == 200:
        print(response.json())
    else:
        print('Ошибка токена', response.text)

# Проверка авторизации
user_1 = {'username': 'Ivan', 'password': 'Ivan1'}
user_2 = {'username': 'Kate', 'password': 'Kate1'}
user_3 = {'username': 'Horse', 'password': 'Igogo'}

token_1 = loggin(user_1)
token_2 = loggin(user_2)
loggin(user_3)

# Проверка инфы по ЗП
get_salary_info(token_1)
get_salary_info(token_2)
get_salary_info('IGOGOG')


