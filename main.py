import requests as r
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
from datetime import datetime

info_list = []
adress_list = []
price_list = []
link_list = []


def collect_info():
    ads_list = []
    page = 1
    number = 1
    user = UserAgent().random

    # подаем запрос на страницу с объявлениями
    header = {'user-agent': user}
    url = "https://krisha.kz/prodazha/kvartiry/almaty/?das[flat.building]=1&das[live.rooms]=3&das[price][from]=30000000&das[price][to]=50000000&sort_by=price-asc"

    page_responce = r.get(url, headers=header).text
    page_soup = BeautifulSoup(page_responce, 'lxml')

    # находим общее количество страниц
    total_pages = int(page_soup.find_all('a', class_="paginator__btn")[-2].get_text(strip=True))

    # проходим циклом по всем страницам
    for j in range(total_pages):
        page_link = f'{url}&page={page}'
        responce = r.get(page_link, headers=header).text
        soup = BeautifulSoup(responce, 'lxml')

        # подаем запрос на каждую следующую страницу с объявлениями
        ad_responce = r.get(page_link, headers=header).text
        ads_soup = BeautifulSoup(ad_responce, 'lxml')

        # находим общее количество объявлений на странице
        ads = ads_soup.find_all('a', class_="a-card__image")
        for ad in ads:
            ads_list.append(ad.get('href'))
        total_ads = len(ads_list)

        block = soup.find('section', class_="a-list a-search-list a-list-with-favs")

        # проходим циклом по всем объявлениям на странице
        for i in range(total_ads):
            advert_main_info = block.find_all('div',
                                              class_="a-card__header-left")[i].get_text(strip=True).replace('Все заметкиУдалить', '')
            advert_adress = block.find_all('div',
                                           class_="a-card__subtitle")[i].get_text(strip=True)
            advert_price = block.find_all('div',
                                          class_="a-card__price")[i].get_text(strip=True)
            advert_link = block.find_all('a',
                                         class_="a-card__image")[i].get('href')

            # заносим всю инфу в списки
            info_list.append(advert_main_info)
            adress_list.append(advert_adress)
            price_list.append(advert_price)
            link_list.append(f'https://krisha.kz{advert_link}')

            ads_list.clear()
        print(f'Собрали инфу со страницы {page}')
        page += 1


def save_info_to_excel():
    date = datetime.now()
    file_name = f'{date.day}.{date.month}.{date.year}'

    excel_path = rf"C:\Users\dd_27\Desktop\krisha_kz_flats_data\flats_data_{file_name}.xlsx"

    info_col = "Краткая информация"
    adress_col = "Адрес"
    price_col = "Стоимость"
    link_col = "Ссылка"

    data = pd.DataFrame({info_col: info_list,
                         adress_col: adress_list,
                         price_col: price_list,
                         link_col: link_list})

    # добавляем всю инфу в таблицу
    data.to_excel(excel_path, sheet_name=file_name, index=False)
    print(f'Информация собрана со всех страниц. Можете посмотреть файл по данному пути: {excel_path}')


collect_info()
save_info_to_excel()
