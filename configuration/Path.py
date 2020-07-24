# coding=gbk
import os


class Path:
    """项目路径"""
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    """配置文件夹路径"""
    config_path = os.path.dirname(os.path.abspath(__file__))

    """测试数据路径"""
    data_path = os.path.join(project_path, 'data')

    """测试用例路径"""
    test_path = os.path.join(project_path, 'test_cases')

    """测试报告路径"""
    report_path = os.path.join(project_path, 'report')
    """判断report文件夹是否存在"""
    if not os.path.exists(report_path):
        os.mkdir(report_path)

    """日志文件路径"""
    log_path = os.path.join(project_path, 'log')
    """判断log文件夹是否存在"""
    if not os.path.exists(log_path):
        os.mkdir(log_path)


path = Path()

if __name__ == '__main__':
    print(path.project_path)
    print(path.config_path)
    print(path.data_path)
    print(path.test_path)
    print(path.report_path)
    print(path.log_path)
