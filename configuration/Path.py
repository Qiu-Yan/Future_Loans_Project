# coding=gbk
import os


class Path:
    """��Ŀ·��"""
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    """�����ļ���·��"""
    config_path = os.path.dirname(os.path.abspath(__file__))

    """��������·��"""
    data_path = os.path.join(project_path, 'data')

    """��������·��"""
    test_path = os.path.join(project_path, 'test_cases')

    """���Ա���·��"""
    report_path = os.path.join(project_path, 'report')
    """�ж�report�ļ����Ƿ����"""
    if not os.path.exists(report_path):
        os.mkdir(report_path)

    """��־�ļ�·��"""
    log_path = os.path.join(project_path, 'log')
    """�ж�log�ļ����Ƿ����"""
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
