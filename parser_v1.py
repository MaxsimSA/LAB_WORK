import requests
from bs4 import BeautifulSoup
import random

# Список различных User-Agent
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]


user_agent = random.choice(user_agents)
headers = {
    'User-Agent': user_agent
}

# Формируем запрос
url = 'https://yandex.ru/pogoda/search?request='
zapros = input('город и район: ')
url += zapros.replace(' ', '+')
print(f"Формируемый URL: {url}")  # Для отладки

# Отправляем запрос с заголовками
response = requests.get(url, headers=headers)
print(f"Статус код: {response.status_code}")

if response.status_code == 200:
    print("Запрос успешен, статус: 200")
else:
    print(f"Ошибка запроса, статус: {response.status_code}")

# Парсим HTML с помощью BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')


#links = soup.find_all('a', class_='link place-list__item-name i-bem')
# if links:
#     for link in links:
#         print(f"Найдена ссылка: {link['href']} - {link.text}")
# if links:
#     print(links['href'])


link = soup.select_one('a.link.place-list__item-name.i-bem')
if link:
    print(f'{link['href']}')


else:
    print("Элементы не найдены")

print(user_agent)