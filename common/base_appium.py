import os

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction


class Base:
    '''
    appium api 封装
    '''
    def __init__(self, logger, driver=None):
        self.driver = driver
        self.timeout = 20
        self.t = 0.5
        self.logger = logger

    def return_driver(self):
        return self.driver
    
    def _get_driver(self, driver):
        '''获取driver，判断用初始化的driver还是传入的driver，传入的优先级的driver优先级最高'''
        return driver or self.driver

    def _get_element(self, locator, element, driver, timeout=None):
        '''判断传入的是locator还是element；返回element; 只传其中一个'''
        if element:
            return element
        return self.find_element(locator, driver, timeout=timeout)
    
    def find_element(self, locator, driver=None, timeout=None):
        '''
        定位元素
        返回定位到的元素，没定位到则抛timeout异常
        locator： ('id', 'kw')/('css selector', 'input#kw')
         ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"
        '''
        if not isinstance(locator, tuple):
            self.logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            raise Exception('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        driver = self._get_driver(driver)
        try:
            element = WebDriverWait(driver, timeout or self.timeout, self.t).until(EC.presence_of_element_located(locator))
            self.logger.info("定位元素信息：定位方式->%s, value值->%s"%(locator[0], locator[1]))
        except Exception:
            self.logger.error("定位方式报错->%s, value值->%s"%(locator[0], locator[1]), exc_info=True)
            #raise Exception("定位方式报错->%s, value值->%s"%(locator[0], locator[1]))
            return False
        else:
            return element

    def find_elements(self, locator, driver=None):
        # 定位元素, 返回元素[]
        if not isinstance(locator, tuple):
            self.logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            raise Exception('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        driver = self._get_driver(driver)
        try:
            elements = WebDriverWait(driver, self.timeout, self.t).until(EC.presence_of_all_elements_located(locator))
            self.logger.info("定位元素信息：定位方式->%s, value值->%s"%(locator[0], locator[1]))
            return elements
        except Exception:
            self.logger.error("查找元素报错->%s, value值->%s"%(locator[0], locator[1]), exc_info=True)

    def send_keys(self, locator=None, text='', element=None, driver=None):
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        element.send_keys(text)
        self.logger.info("输入信息：%s"% text)

    def tap_(self, position=(None, None), locator=None, element=None, driver=None):
        '''单点触摸元素'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        TouchAction(driver).tap(element=element, x=position[0], y=position[1]).perform()
        self.logger.info("tap元素%s，坐标%s" %(element, position))

    def press(self, position=(None, None), locator=None, element=None, driver=None):
        '''按压元素'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        TouchAction(driver).press(el=element, x=position[0], y=position[1]).perform()
        self.logger.info("按压元素%s，坐标%s" % (element, position))

    def long_press(self, position=(None, None), locator=None, element=None, duration=1000, driver=None):
        '''长按元素'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        TouchAction(driver).long_press(el=element, x=position[0], y=position[1], duration=duration).perform()
        self.logger.info("长按元素%s，坐标%s" % (element, position))

    def unlock_by_elements(self, elements_list, driver=None):
        '''
        九宫格解锁
        传入 [locator,locators,locators]   元素或者定位都可以
        按顺序滑动解锁
        '''
        driver = self._get_driver(driver)
        action_list = []
        for element in elements_list:
            if isinstance(element, tuple):
                action_list.append(self.find_element(element, driver=driver))
            else:
                action_list.append(element)

        num = len(action_list)
        ta = TouchAction(driver)
        for i, element in enumerate(action_list, start=1):
            if i == 1:
                ta.press(el=element).wait(150)
            elif i != num:
                ta.move_to(el=element).wait(50)
            else:
                ta.move_to(el=element).wait(150).release()
        ta.perform()
        self.logger.info("解锁九宫格：%s" % action_list)

    def unlock_by_location(self, pwd_list, locator=None, element=None, driver=None):
        '''
        九宫格解锁
        传入 pwd [1,5,7,8,9]
        九宫格 element或者locator, 必须传一个
        '''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        location = self.get_element_location(element=element, driver=driver)
        size =self.get_element_size(element=element, driver=driver)

        pwd_location = []
        for i in pwd_list:
            if str(i) == '1':
                pwd_location.append((location['x'] + size['width'] * 1/4,
                                    location['y'] + size['height'] * 1/4))
            elif str(i) == '2':
                pwd_location.append((location['x'] + size['width'] * 2 / 4,
                                    location['y'] + size['height'] * 1 / 4))
            elif str(i) == '3':
                pwd_location.append((location['x'] + size['width'] * 3 / 4,
                                    location['y'] + size['height'] * 1 / 4))
            elif str(i) == '4':
                pwd_location.append((location['x'] + size['width'] * 1 / 4,
                                    location['y'] + size['height'] * 2 / 4))
            elif str(i) == '5':
                pwd_location.append((location['x'] + size['width'] * 2 / 4,
                                    location['y'] + size['height'] * 2 / 4))
            elif str(i) == '6':
                pwd_location.append((location['x'] + size['width'] * 3 / 4,
                                    location['y'] + size['height'] * 2 / 4))
            elif str(i) == '7':
                pwd_location.append((location['x'] + size['width'] * 1 / 4,
                                    location['y'] + size['height'] * 3 / 4))
            elif str(i) == '8':
                pwd_location.append((location['x'] + size['width'] * 2 / 4,
                                    location['y'] + size['height'] * 3 / 4))
            elif str(i) == '9':
                pwd_location.append((location['x'] + size['width'] * 3 / 4,
                                    location['y'] + size['height'] * 3 / 4))

        num = len(pwd_location)
        ta = TouchAction(driver)
        for i, location in enumerate(pwd_location, start=1):
            if i == 1:
                ta.press(x=location[0], y=location[1]).wait(150)
            elif i != num:
                ta.move_to(x=location[0], y=location[1]).wait(50)
            else:
                ta.move_to(x=location[0], y=location[1]).wait(150).release()
        ta.perform()
        self.logger.info("解锁九宫格：%s" % pwd_list)

    def click(self, locator=None, element=None, driver=None):
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        element.click()
        self.logger.info("点击元素")

    def clear(self, locator=None, element=None, driver=None):
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        element.clear()
        self.logger.info("清空输入框")

    def is_enabled(self, locator=None, element=None, driver=None):
        '''判断input\select等元素是否可编辑状态，返回bool值'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        r = element.is_enabled()
        self.logger.info("元素是否可编辑：%s" %r)
        return r

    def is_element_exist(self, locator=None, element=None, driver=None, timeout=None):
        '''判断元素是否存在，返回bool值'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver, timeout=timeout)
        if element:
            self.logger.info("元素存在")
            return element
        self.logger.info("元素不存在")
        return False

    def is_element_contains_text(self, locator, text='', driver=None):
        '''判断元素是否包含预期的字符串，返回bool'''
        if not isinstance(locator, tuple):
            self.logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            raise Exception('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        driver = self._get_driver(driver)
        try:
            result = WebDriverWait(driver, self.timeout, self.t).until(EC.text_to_be_present_in_element(locator, text))
            self.logger.info('元素文本值包含：%s'%text)
            return result
        except:
            self.logger.info('元素文本值没有包含：%s' % text)
            return False

    def is_elementValue_contains_value(self, locator, value='', driver=None):
        '''判断元素的value属性值是否包含预期的value，返回bool'''
        if not isinstance(locator, tuple):
            self.logger.error('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
            raise Exception('locator参数类型错误，必须传元祖类型：loc = ("id", "value1")')
        driver = self._get_driver(driver)
        try:
            result = WebDriverWait(driver, self.timeout, self.t).until(EC.text_to_be_present_in_element_value(locator, value))
            self.logger.info('元素的value属性值包含：%s'%value)
            return result
        except:
            self.logger.info('元素的value属性值没有包含：%s' % value)
            return False

    def close(self, driver=None):
        '''关闭浏览器'''
        driver = self._get_driver(driver)
        driver.quit()
        self.logger.info('关闭浏览器')

    def get_element_text(self, locator=None, element=None, driver=None):
        '''获取元素的文本'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        text = element.text
        self.logger.info('获取元素的文本：%s' %text)
        return text

    def get_attribute(self, name, locator=None, element=None, driver=None):
        '''获取元素的属性值'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        value = element.get_attribute(name)
        self.logger.info('获取%s元素%s属性：%s' %(element, name, value))
        return value

    def get_element_size(self, locator=None, element=None, driver=None):
        '''获取元素的尺寸，返回字典 {'width': 84, 'height': 99}'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        size = element.size
        self.logger.info('获取%s元素尺寸：%s' %(element, size))
        return size

    def get_element_location(self, locator=None, element=None, driver=None):
        '''获取元素的坐标，返回字典 {'x': 84, 'y': 99}'''
        driver = self._get_driver(driver)
        element = self._get_element(locator, element, driver)
        location = element.location
        self.logger.info('获取%s元素坐标：%s' % (element, location))
        return location

    def get_phone_size(self, type, driver=None):
        '''获取手机的宽width、高height'''
        driver = self._get_driver(driver)
        size = driver.get_window_size()
        self.logger.info("获取%s: %s" %(type, size[type]))
        return size[type]

    def swipe(self, from_position, to_position, duration=None, driver=None):
        '''根据坐标滑动'''
        driver = self._get_driver(driver)
        driver.swipe(from_position[0], from_position[1], to_position[0], to_position[1], duration=duration)
        self.logger.info("滑动%s --> %s" % (from_position, to_position))

    def swipe_up(self, duration=None, driver=None):
        '''向上滑动'''
        driver = self._get_driver(driver)
        x = self.get_phone_size('width', driver=driver)/2
        height = self.get_phone_size('height', driver=driver)
        from_y = height / 10 * 9
        to_y = height / 10
        self.swipe((x, from_y), (x, to_y), duration=duration, driver=driver)
        self.logger.info("向上滑动")

    def swipe_down(self, duration=None, driver=None):
        '''向下滑动'''
        driver = self._get_driver(driver)
        x = self.get_phone_size('width', driver=driver)/2
        height = self.get_phone_size('height', driver=driver)
        from_y = height / 10
        to_y = height / 10 * 9
        self.swipe((x, from_y), (x, to_y), duration=duration, driver=driver)
        self.logger.info("向下滑动")

    def swipe_left(self, duration=None, driver=None):
        '''向左滑动'''
        driver = self._get_driver(driver)
        width = self.get_phone_size('width', driver=driver)
        from_x = width / 10 * 9
        to_x = width / 10
        y = self.get_phone_size('height', driver=driver)/2
        self.swipe((from_x, y), (to_x, y), duration=duration, driver=driver)
        self.logger.info("向左滑动")

    def swipe_right(self, duration=None, driver=None):
        '''向右滑动'''
        driver = self._get_driver(driver)
        width = self.get_phone_size('width', driver=driver)
        from_x = width / 10
        to_x = width / 10 * 9
        y = self.get_phone_size('height', driver=driver)/2
        self.swipe((from_x, y), (to_x, y), duration=duration, driver=driver)
        self.logger.info("向右滑动")

    def contexts(self, driver=None):
        '''获取当前页面的contexts，返回list'''
        driver = self._get_driver(driver)
        contexts = driver.contexts
        self.logger.info("获取当前页面contexts：%s" %contexts)
        return contexts

    def switch_to_context(self, context, driver=None):
        '''native和webview切换'''
        driver = self._get_driver(driver)
        driver.switch_to.context(context)
        self.logger.info("切换到context：%s" %context)

    def switch_to_native(self, driver=None):
        '''切换回到native'''
        driver = self._get_driver(driver)
        driver.switch_to.context("NATIVE_APP")
        self.logger.info("切换到native app")

    def tap(self, positions, duration=None, driver=None):
        '''多点触摸positions  # 需要传list 做多传5个坐标  [(1,2),(3,4)]'''
        driver = self._get_driver(driver)
        driver.tap(positions=positions, duration=duration)
        self.logger.info("触摸：%s，持续：%s毫秒" %(positions, duration))

    def wait_activity(self, activity, timeout=10, interval=0.5, driver=None):
        '''等待activity出现，返回bool，#安卓特有'''
        driver = self._get_driver(driver)
        res = driver.wait_activity(activity=activity, timeout=timeout, interval=interval)
        self.logger.info("等待activity：%s %s" % (activity, res))
        return res

    def current_activity(self, driver=None):
        '''获取当前activity, #安卓特有'''
        driver = self._get_driver(driver)
        current_activity = driver.current_activity
        self.logger.info("获取当前activity：%s" % current_activity)
        return current_activity

    def is_toast_exist(self, text, timeout=10, poll_frequency=0.5, driver=None):
        '''
        toast元素检查
        cap里面需要加 “automationName”: "Uiautomator2"
        '''
        driver = self._get_driver(driver)
        try:
            toast_loc = ("xpath", ".//*[contains(@text, '%s')]" % text)
            toast_ele = WebDriverWait(driver, timeout, poll_frequency).until(EC.presence_of_element_located(toast_loc))
            self.logger.info("检查 %s toast，存在%s" %(text, toast_ele))
            return toast_ele
        except:
            self.logger.info("检查 %s toast，不存在" % text)
            return False

    def always_allows(self, num=5, driver=None):
        '''安卓启动App 获取权限的弹框 点击始终允许'''
        driver = self._get_driver(driver)
        for i in range(num):
            loc = ("xpath", "//*[@text='始终允许']")
            try:
                element = WebDriverWait(driver, 3, 0.5).until(EC.presence_of_element_located(loc))
                element.click()
                self.logger.info("权限获取，点击始终允许")
            except:
                pass

    def get_screenshot_as_base64(self, driver=None):
        '''截图'''
        driver = self._get_driver(driver)
        pic_base64 = driver.get_screenshot_as_base64()
        self.logger.info("截图")
        return pic_base64

    def exec_adb(self, command):
        '''执行adb命令'''
        os.system(command)
        self.logger.info("执行command：%s" %command)

    def close_app(self, driver=None):
        '''关闭App'''
        driver = self._get_driver(driver)
        driver.close_app()
        self.logger.info("关闭App")

    def launch_app(self, driver=None):
        driver = self._get_driver(driver)
        driver.launch_app()
        self.logger.info("启动App")


if __name__ == '__main__':
    from selenium import webdriver
    from time import sleep
    from selenium.webdriver.chrome.options import Options
    from logger import Logger

    logger = Logger()

    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)


    handle = Base(logger=logger, driver=driver) # logger是必传的，driver可以不传
    handle.maximize_window()
    handle.set_page_load_timeout()
    handle.get('http://www.baidu.com')
    handle.send_keys(('id', 'kw'), '哦哦哦哦')  # 初始化传了driver的，默认用初始化的driver
    sleep(1)

    handle.clear(('id', 'kw'), driver=driver)   # 初始化没有传driver，或者传了driver的；调方法时，传driver会优先用方法传的driver

    sleep(2)
    search_btn_ele = handle.find_element(('id', 'su'))
    handle.double_click(element=search_btn_ele) # 可以传locator或者element，其中一个，去操作
    sleep(2)
    handle.close()

