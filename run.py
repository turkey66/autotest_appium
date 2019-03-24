# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/2/11 0:17'
import os

from pages.tools import yamlLocator_to_pageObject

# ?collapsed=Passed,XFailed,Skipped

yamlLocator_to_pageObject()


os.system('cd C:/autotest_appium')
os.system('pytest \
--host=127.0.0.1:4723 --device=device_1 \
--html=./reports/report.html --self-contained-html -q ./cases/test_unlock.py')