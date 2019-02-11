# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/2/10 19:41'
from pages.page_objects import LoginPage
from time import sleep




def test_01(handle, launch_close_app):
    '''用例的名字这里'''
    loc_1 = LoginPage.一
    loc_2 = LoginPage.二
    loc_3 = LoginPage.三
    loc_4 = LoginPage.四
    loc_5 = LoginPage.五
    loc_6 = LoginPage.六
    loc_7 = LoginPage.七
    loc_8 = LoginPage.八
    loc_9 = LoginPage.九
    loc_jiu = LoginPage.解锁图
    handle.unlock_by_elements(elements_list=[loc_1, loc_4, loc_8, loc_6, loc_3])
    sleep(5)
    raise Exception("报错截图阿")

if __name__ == "__main__":
    import pytest
    pytest.main(['-q', 'test_unlock.py'])