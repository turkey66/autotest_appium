# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/2/11 13:59'
import pytest

from pages.page_objects import LoginPage


@pytest.fixture(scope='function')
def launch_close_app(handle, logger, request):
    '''启动App'''
    handle.launch_app()

    def fn():
        handle.close_app()

    request.addfinalizer(fn)


@pytest.fixture(scope='function')
def unlock(handle, logger):
    '''九宫格解锁'''
    handle.unlock_by_location([1,5,8,6,3], LoginPage.解锁图)