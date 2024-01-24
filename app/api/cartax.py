import requests
from bs4 import BeautifulSoup
import re
import json
import sys

def get_data(registration_mark):
    base_url = "https://eteenindus.mnt.ee/public/soidukTaustakontroll.jsf?lang=et"

    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    view_state = soup.find('input', {'name': 'javax.faces.ViewState'})['value']
    captcha_id = soup.find('div', {'id': 'j_idt136:captcha'})['id']

    captcha_data = {
        'javax.faces.ViewState': view_state,
        captcha_id: '',
    }
    response = requests.post(base_url, data=captcha_data)

    form_data = {
        'javax.faces.ViewState': view_state,
        'j_idt136:regMark': registration_mark,
        'j_idt136:j_idt169': 'j_idt136:j_idt169',
    }
    response = requests.post(base_url, data=form_data)

    soup = BeautifulSoup(response.content, 'html.parser')

    kategooria = soup.find('td', text='Kategooria:').find_next_sibling('td').get_text(strip=True)
    esmane_registreerimine = soup.find('td', text='Esmane registreerimine:').find_next_sibling('td').get_text(strip=True)
    
    taismass = soup.find('td', text='Täismass').find_next_sibling('td').get_text(strip=True)

    co2_elements = soup.find_all('td', text=re.compile(r'^CO2'))

    co2_number = None

    for co2_element in co2_elements:
        co2_value = co2_element.find_next_sibling('td').get_text(strip=True)
        co2_number_match = re.search(r'\d+', co2_value)

        if co2_number_match:
            co2_number = int(co2_number_match.group())
            co2_type = co2_element.get_text(strip=True)

            print(f"{co2_type}: {co2_number} g/km")

    result = {
        "Kategooria": kategooria,
        "Esmane registreerimine": esmane_registreerimine,
        "Täismass": taismass,
        "CO2 Number": co2_number
    }

    print(json.dumps(result))

    calculate(kategooria, esmane_registreerimine, taismass, co2_number)

def calculate(kategooria, esmane_registreerimine, taismass, co2_type, co2_number):
    base_url = "https://www.err.ee/1609128527/kalkulaator-vaata-kui-suur-tuleb-sinu-automaks"

    try:
        response = requests.get(base_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        kategooria_id = f"type_{kategooria.capitalize()}"
        try:
            label_element = soup.find('label', {'for': kategooria_id})
            if label_element:
                kategooria_input = label_element.find_next('input', {'type': 'radio'})
                kategooria_value = kategooria_input['value']
            else:
                raise ValueError(f"Element with id '{kategooria_id}' not found. Continuing without selecting kategooria.")
        except Exception as e:
            print(str(e))
            return

        payload = {
            'register-year': esmane_registreerimine.split('.')[-1],
            'vehicle-mass': taismass.replace('kg', ''),
            'c-type': co2_type,
            'co2-value': co2_number,
            kategooria_value: '',
        }

        response = requests.post(base_url, data=payload)

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            aastamaks = soup.find('div', text='Aastamaks').find_next('div').get_text(strip=True)
            print("Aastamaks:", aastamaks)
        except AttributeError:
            print("Element for 'Aastamaks' not found.")

        try:
            registreerimistasu = soup.find('div', text='Registreerimistasu').find_next('div').get_text(strip=True)
            print("Registreerimistasu:", registreerimistasu)
        except AttributeError:
            print("Element for 'Registreerimistasu' not found.")

    except Exception as e:
        print(str(e))
try:
    if __name__ == "__main__":
        registration_mark = sys.argv[1] if len(sys.argv) > 1 else ""

        get_data(registration_mark)
except Exception as e:
    print(f"Error: {str(e)}")
    sys.exit(1)