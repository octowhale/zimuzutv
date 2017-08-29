#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
from bs4 import BeautifulSoup
from datetime import datetime as dt


def today(html):
    # dt_date = '2017-08-29'


    dt_date = dt.strftime(dt.now(), "%m-%d")
    soup = BeautifulSoup(html, 'lxml')

    res_list = soup.find('table', class_="d_r_t")

    movies = res_list.find_all('tr', attrs={"day": dt_date})

    # print(len(movies))
    items = []
    for movie in movies:
        m_dict = {}
        """
        使用选择器，可行
        # m_type = movie.select('td.d1')[0].string
        # m_format = movie.select('td.d2')[0].text
        """

        m_area = movie['area']
        m_type = movie.find('td', class_="d1").text
        m_format = movie.find('td', class_="d2").text

        m_title = movie.find('a', attrs={"target": "_blank"}).text
        m_detail = movie.find('a', attrs={"target": "_blank"})['href']
        m_update_time = movie.find('td', class_='d6').text

        m_dict['m_date'] = dt_date
        m_dict['m_update_time'] = m_update_time
        m_dict['area'] = m_area
        m_dict['m_type'] = m_type
        m_dict['m_format'] = m_format
        m_dict['m_title'] = m_title
        m_dict['m_detail'] = m_detail

        # print(m_area)
        # print(m_type, m_format)
        # print(m_title, m_detail)

        m_dict['dl'] = []
        for dl in movie.find('td', class_="dr_ico").find_all('a'):
            try:
                # print("{} : {}".format(dl.text, dl['href']))

                m_dict['dl'].append({'dl_name': dl.text, 'dl_url': dl['href']})
                # print(dl)

                # if dl.text == '驴':
                #     print(m_title)
                #     print(dl['href'])
            except:
                pass

        # print(json.dumps(m_dict))
        # print("\n")

        items.append(m_dict)

    return items
