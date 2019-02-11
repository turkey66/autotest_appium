# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/2/10 18:03'
import os
import time

from appium import webdriver
import pytest
from py.xml import html

from common.parse_yaml import get_yaml_info
from common.logger import Logger
from common.base_appium import Base

cwd = os.getcwd()  # 当前目录路径
cap_file = os.path.join(cwd, 'config', 'devices_capabilities.yaml')  # yaml文件路径
devices_cap = get_yaml_info(cap_file)


_driver = None

def pytest_addoption(parser):
    '''添加命令行参数--device、--host'''
    parser.addoption(
        "--device", action="store", default="device_1", help="device option: device_1"
             )
    # 添加host参数，设置默认测试环境地址
    parser.addoption(
        "--host", action="store", default="127.0.0.1:4723", help="test host->127.0.0.1:4723"
    )


@pytest.fixture(scope='session')
def host(request):
    '''全局host参数'''
    return request.config.getoption("--host")


@pytest.fixture(scope='session')
def device(request):
    '''全局device参数'''
    return request.config.getoption("--device")


@pytest.fixture(scope='session')
def logger(request):
    '''全局logger'''
    date = time.strftime("%Y-%m-%d_", time.localtime())
    device = request.config.getoption("--device")
    device_name = devices_cap[device]['name']
    dir_path = os.path.join(cwd, 'logs')
    _logger = Logger(file_name=date+device_name+'.log', dir_path=dir_path, console=False)
    return _logger


@pytest.fixture(scope='session')
def handle(request, logger):
    '''定义全局driver参数'''
    global _driver
    host = request.config.getoption("--host")
    device = request.config.getoption("--device")
    capabilities = devices_cap[device]['cap']
    _driver = webdriver.Remote("http://{}/wd/hub".format(host), capabilities)
    _driver.close_app()
    handle = Base(driver=_driver, logger=logger)


    def fn():
        logger.info("当全部用例执行完：teardown quit driver！")
        _driver.quit()

    request.addfinalizer(fn)
    return handle


@pytest.fixture(scope="module", autouse=True)
def module_log(request, logger):
    logger.info('开始执行module: %s' % request.module.__name__)

    def fin():
        logger.info('结束执行module: %s' % request.module.__name__)

    request.addfinalizer(fin)


@pytest.fixture(scope="function", autouse=True)
def func_log(request, logger):
    logger.info('执行case: %s' % request.function.__name__)

    def fin():
        logger.info('结束执行case: %s' % request.function.__name__)

    request.addfinalizer(fin)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_")+".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.description = str(item.function.__doc__)
        report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")


def _capture_screenshot():
    '''
    截图保存为base64
    :return:
    '''
    return _driver.get_screenshot_as_base64()


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


