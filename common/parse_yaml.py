# _*_ coding:utf-8 _*_

import yaml


def get_yaml_info(file_path):
    # 返回yaml文件信息，dict
    with open(file_path, 'r', encoding='UTF-8') as f:
        content = yaml.load(f)
        return content


if __name__ == '__main__':
    import os
    cwd = os.getcwd()  # 当前目录路径
    file_path = os.path.join(cwd, 'test.yaml')  # yaml文件路径
    yaml_dict = get_yaml_info(file_path)
    print(yaml_dict)