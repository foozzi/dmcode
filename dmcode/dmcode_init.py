from .settings import __version__, FTP_CONFIG, SFTP_CONFIG, PASTE_CONFIG, CONFIG_FILE
from configparser import ConfigParser
import os
from pathlib import Path


class DMC_INIT:
    def __init__(
            self,
            type,  # - ftp/sftp or paste method
            host='',
            port='',
            login='',
            password='',
            path='',
            api_key='',
            name_paste='',
            api_url='',
            ignore_ext='',
            ignore_files='',
            ignore_dirs=''):
        config = ConfigParser()

        if not os.path.exists(Path(CONFIG_FILE).absolute()):
            config['DMC'] = {
                'ignore_ext': ignore_ext,
                'ignore_files': ignore_files,
                'ignore_dirs': ignore_dirs,
                'max_size_dir_mb': 5,
                'max_size_file_mb': 5
            }
            config['FTP_SETTINGS'] = {
                'host': '',
                'port': '',
                'login': '',
                'password': '',
                'path': ''
            }
            config['SFTP_SETTINGS'] = {
                'host': '',
                'port': '',
                'login': '',
                'password': '',
                'path': ''
            }
            config['PASTE_SETTINGS'] = {
                'name_paste': name_paste,
                'api_key': api_key,
                'api_url': api_url
            }

            with open(Path(CONFIG_FILE).absolute(), 'w') as configfile:
                config.write(configfile)
            
            if type == PASTE_CONFIG:
                return

        config.read(Path(CONFIG_FILE).absolute())
        """paste configs"""
        if type == PASTE_CONFIG:
            config['{}_SETTINGS'.format(type)]['api_key'] = api_key.strip()
            config['{}_SETTINGS'.format(type)]['api_url'] = api_url.strip()
            config['{}_SETTINGS'.format(
                type)]['name_paste'] = name_paste.strip()
        else:
            """s/ftp configs"""
            config['{}_SETTINGS'.format(type)]['host'] = host.strip()
            port = str(port)
            config['{}_SETTINGS'.format(type)]['port'] = port.strip()
            config['{}_SETTINGS'.format(type)]['login'] = login.strip()
            config['{}_SETTINGS'.format(type)]['password'] = password.strip()
            config['{}_SETTINGS'.format(type)]['path'] = path.strip()

        with open(Path(CONFIG_FILE).absolute(), 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def set_paste_token(token):
        config = ConfigParser()
        config.read(Path(CONFIG_FILE).absolute())
        config['{}_SETTINGS'.format(PASTE_CONFIG)]['token'] = token
        with open(Path(CONFIG_FILE).absolute(), 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def get_paste_token():
        config = ConfigParser()
        config.read(Path(CONFIG_FILE).absolute())
        return config['{}_SETTINGS'.format(PASTE_CONFIG)]['token']
