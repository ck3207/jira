import configparser


class LoadingConfig:
    """读取配置文件"""
    def __init__(self):
        pass

    def loading(self, filename):
        cf = configparser.ConfigParser()
        cf.read(filenames=filename, encoding="utf8")
        return cf

loading_config = LoadingConfig()
config_obj_of_jira_relation = loading_config.loading(filename="config/jira.conf")
config_obj_of_authority = loading_config.loading(filename="config/authority.conf")

