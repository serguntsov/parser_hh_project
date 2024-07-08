import requests
from database import get_vacancy_info

def display_vacancy(vacancy):
    salary = vacancy.get('salary')
    location = vacancy.get('area', {}).get('name', 'N/A')
    experience = vacancy.get('experience', {}).get('name', 'N/A')
    if salary:
        salary_range = f"{salary.get('from', 'N/A')}-{salary.get('to', 'N/A')} {salary.get('value', '')}"
    else:
        salary_range = 'N/A'
    print(f"{vacancy['name']} - {salary_range} - {location} - {experience}")

def get_vacancies(query):
    url = f"https://api.hh.ru/vacancies?query={query}&area=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        vacancies = response.json()
        for vacancy in vacancies['items']:
            salary = vacancy.get('salary')
            location = vacancy.get('area', {}).get('name', 'N/A')
            experience = vacancy.get('experience', {}).get('name', 'N/A')
            id = vacancy.get('id')
            if salary:
                salary_range = f"{salary.get('from', 'N/A')}-{salary.get('to', 'N/A')} {salary.get('value', '')}"
            else:
                salary_range = 'N/A'
            print(f"{vacancy['name']} - {salary_range} - {location} - {experience} - {id}")
        return vacancies
    else:
        return None

def find_vacancies_by_name(name, chat_id):
    url = "https://api.hh.ru/vacancies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36"
    }
    all_vacancies = []
    page = 0
    while True:
        params = {
            "text": name,
            "per_page": 100,
            "page": page
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            vacancies = response.json()
            if not vacancies['items']:
                break
            all_vacancies.extend(vacancies['items'])
            page += 1
            if page >= 10:
                break
        else:
            print(f"Ошибка при запросе данных: {response.status_code}")
            break

    for vacancy in all_vacancies:
        salary = vacancy.get('salary')
        name = vacancy.get('name')
        id = vacancy.get('id')
        location = vacancy.get('area', {}).get('name', 'N/A')
        experience = vacancy.get('experience', {}).get('name', 'N/A')
        if salary:
            salary_min = salary.get('from', 'N/A')
            salary_max = salary.get('to', 'N/A')
            value = salary.get('currency', '')
            salary_range = f"{salary_min}-{salary_max} {value}"
        else:
            salary_min = 'N/A'
            salary_max = 'N/A'
            value = 'N/A'
            salary_range = 'N/A'
        
        print(name, id, location, experience, salary_min, salary_max, value)
        print(f"{vacancy['name']} - {salary_range} - {location} - {experience} - https://hh.ru/vacancy/{id}")
        id = f"https://hh.ru/vacancy/{id}"
        get_vacancy_info(name, location, experience, salary_min, salary_max, value, id, chat_id)

    return all_vacancies
