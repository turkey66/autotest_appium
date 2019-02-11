# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2019/2/10 2:28'

import os

import yaml
import jinja2

# 当前文件所在文件夹路径
current_path = os.path.dirname(os.path.realpath(__file__))
# yaml文件夹路径
yaml_path = os.path.join(current_path, 'locators')

def parseyaml():
    '''遍历读取所有yaml文件'''
    pageElements = {}
    for fpath, dirname, fnames in os.walk(yaml_path):
        for name in fnames:
            yaml_file_path = os.path.join(fpath, name)  # 绝对路径
            if yaml_file_path.endswith(".yaml"):    # 筛选.yaml文件
                with open(yaml_file_path, 'r', encoding='utf-8') as f:
                    page = yaml.load(f)
                    pageElements.update(page)
    return pageElements


def create_pages_py(pageElements):
    template_loader = jinja2.FileSystemLoader(searchpath=current_path)
    template_env = jinja2.Environment(loader=template_loader)
    templateVars = {
        'pageElements': pageElements
    }
    template = template_env.get_template("template")
    with open(os.path.join(current_path, "page_objects.py"), 'w', encoding='utf-8') as f:
        f.write(template.render(templateVars))


def yamlLocator_to_pageObject():
    create_pages_py(parseyaml())

if __name__ == '__main__':
    create_pages_py(parseyaml())
    p = parseyaml()
    print(p)
    for i in p["LoginPage"]["locators"]:
        print(i)