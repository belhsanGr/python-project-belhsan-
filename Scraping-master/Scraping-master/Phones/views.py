from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def scrape_and_filter(request):
    base_url = "https://www.jumia.com.tn"
    phones = []
    brands = set()  # To store unique brands
    for i in range(1, 16):
        url = f"https://www.jumia.com.tn/telephones-smartphones/?page={i}#catalog-listing"
        response = requests.get(url)
        response = response.content
        soup = BeautifulSoup(response, 'html.parser')
        div = soup.find('div', class_='-paxs row _no-g _4cl-3cm-shs')
        arts = div.find_all('article', class_='prd _fb col c-prd')

        for art in arts:
            img = art.find('div', class_='img-c')
            titre = art.find('div', class_='info')
            nom_tel = titre.find('h3', class_='name').text
            prix = art.find('div', class_='prc').text
            prix = prix.replace(',', '').replace('.', '').replace('TND', '')
            prix = float(prix) / 100
            marque = nom_tel.strip()
            marque = marque.split()[0]
            img_url = img.find('img')['data-src']
            tel_link = art.find('a', class_='core')['href']
            link = base_url + tel_link

            # Add the brand to the set of unique brands
            brands.add(marque)

            phone_data = {
                'marque': marque,
                'nom_tel': nom_tel,
                'prix': prix,
                'img_url': img_url,
                'link': link
            }
            phones.append(phone_data)

    context = {
        'phones': phones,
        'brands': sorted(brands)  # Sort the brands alphabetically
    }

    if request.method == 'POST':
        brand = request.POST.get('brand')
        max_price = request.POST.get('max_price')

        # Apply filtering based on brand and/or price
        filtered_phones = []
        for phone in phones:
            if brand:
                if max_price and phone['prix'] <= float(max_price):
                    if phone['marque'] == brand:
                        filtered_phones.append(phone)
                elif not max_price:
                    if phone['marque'] == brand:
                        filtered_phones.append(phone)
            elif max_price:
                if phone['prix'] <= float(max_price):
                    filtered_phones.append(phone)

        context['phones'] = filtered_phones

    return render(request, 'Phones/phone_list.html', context)
