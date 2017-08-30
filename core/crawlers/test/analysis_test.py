#!/usr/bin/env python
# encoding: utf-8

# python 3.6

import os
import sys
from bs4 import BeautifulSoup
from datetime import datetime as dt


def today(html):
    """分析 zimuzu.tv/today 信息"""
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

        m_dict['dl'] = []
        for dl in movie.find('td', class_="dr_ico").find_all('a'):
            try:
                m_dict['dl'].append({'dl_name': dl.text, 'dl_url': dl['href']})
            except:
                pass

        items.append(m_dict)

    return items


def detail(html, items=None):
    """分析页面详细信息 /resource/list/id"""

    soup = BeautifulSoup(html, 'lxml')

    if items is None:
        items = {}

    movie_name = soup.find('h2').text.strip("返回详情介绍页")
    items['m_name'] = movie_name
    # fmts = soup.find('div', class_="download-filter").find_all('a')

    # fmts_list = ['MP4', 'HDTV']
    """格式列表"""
    fmts_list = ['MP4', 'HDTV', '720P', 'WEB-DL']

    """格式字典"""
    episode_dict = {}

    """季字典"""
    # seasons = {}
    seasons_list = []
    seasons_dict = {}
    # li_tags = soup.find_all('li', class_='clearfix')
    for fmt in fmts_list:
        fmt_season_dict = {}
        # li_tags = soup.find_all('li', class_='clearfix', format_='MP4')
        li_tags = soup.find_all('li', attrs={"class": "clearfix", "format": fmt})

        if len(li_tags) == 0:
            continue

        # print(len(li_tags))
        for li_tag in li_tags:

            season_episode_dict = {}
            fmt = li_tag['format']
            season = li_tag['season']
            episode = li_tag['episode']

            enp_title = li_tag.find('div', class_='fl').a.text
            # print(enp_title)

            a_tags = li_tag.find('div', class_='fr').find_all('a')

            """集字典"""
            dl_ways_dict = {}

            # fmts["第_{}_集".format(episode)] = episodes
            episode_dict["_".join(enp_title.split('.'))] = dl_ways_dict

            # seasons[fmt] = fmts
            # seasons_dict[season] = {}

            # items["第_{}_季".format(season)] = seasons
            for dl in a_tags:

                dl_name = dl.text.strip()

                try:
                    if dl_name == '小米路由下载':
                        dl_url = dl['xmhref']
                    else:
                        dl_url = dl['href']
                except:
                    dl_url = None

                if dl_url is not None:
                    dl_ways_dict[dl_name] = dl_url

            episode_dict["_".join(enp_title.split('.'))] = dl_ways_dict
        season_episode_dict = episode_dict
        fmt_season_dict = season_episode_dict
        seasons_dict[fmt] = fmt_season_dict
    print("页面分析成功")
    items['season'] = seasons_dict
    return items
