#!/bin/python3
from .util.file import PrepareFiles, PackFiles
from .util.error import FilesSizeError, \
    FileConfigNotFound, \
    ConfigSectionNotFound, \
    ErrorSettingsFTP, \
    ErrorSettingsSFTP, \
    NotFoundPasteName
import os
from configparser import ConfigParser
import crayons
from pathlib import Path
from .util.ftp import _FTP
from .util.sftp import SFTP
from .util.paste import PASTE
from .settings import __version__, FTP_CONFIG, SFTP_CONFIG, PASTE_CONFIG


class DMC:
    def __init__(
            self,
            protocol=FTP_CONFIG,  # - BY DEFAULT FTP CONNECT
            config_file='dmc.ini',
            config_section='DMC',
            config_section_ftp='FTP_SETTINGS',
            config_section_sftp='SFTP_SETTINGS',
            config_section_paste='PASTE_SETTINGS',
            paste_expire='1month'):

        self.config_file = config_file
        self.config_section = config_section
        self.config_section_ftp = config_section_ftp
        self.config_section_sftp = config_section_sftp
        self.config_section_paste = config_section_paste

        self.paste_expire = paste_expire

        self.config = ConfigParser()

        if os.path.exists(Path(self.config_file).absolute()) is False:
            raise FileConfigNotFound(
                'File config dmc.ini is not found! See `dmc -h`')

        self.config.read(self.config_file)

        # check main config section
        if self.config_section not in self.config.sections():
            raise ConfigSectionNotFound('{} section not found in dmc.ini'.format(
                self.config_section))  # - сделать пользовательские секции при инициализации

        self.dmc_config_section = self.config[self.config_section]

        # now checking ftp or sftp by argument passed 'protocol'
        if protocol == FTP_CONFIG:
            if self.config_section_ftp not in self.config.sections():
                raise ConfigSectionNotFound('{} section not found in dmc.ini'.format(
                    self.config_section))
            else:
                self.dmc_config_section_ftp = self.config[self.config_section_ftp]

                if self.dmc_config_section_ftp['host'].strip() == '':
                    raise ErrorSettingsFTP(
                        'Please edit dmc.ini for setting ftp connection')

                # fix value for port string
                port_ftp = self.dmc_config_section_ftp['port']

                # test connect server
                self.connect = _FTP(
                    host=self.dmc_config_section_ftp['host'],
                    port=int(port_ftp),
                    login=self.dmc_config_section_ftp['login'],
                    password=self.dmc_config_section_ftp['password'])
                self.deploy(self.dmc_config_section_ftp, FTP_CONFIG)

        if protocol == SFTP_CONFIG:
            if self.config_section_sftp not in self.config.sections():
                raise ConfigSectionNotFound('{} section not found in dmc.ini'.format(
                    self.config_section))
            else:
                self.dmc_config_section_sftp = self.config[self.config_section_sftp]

                if self.dmc_config_section_sftp['host'].strip() == '':
                    raise ErrorSettingsSFTP(
                        'Please edit dmc.ini for setting ftp connection')

                # fix value for port string
                port_sftp = self.dmc_config_section_sftp['port']

                # test connect server
                self.connect = SFTP(
                    host=self.dmc_config_section_sftp['host'],
                    port=int(port_sftp),
                    login=self.dmc_config_section_sftp['login'],
                    password=self.dmc_config_section_sftp['password'])

                self.deploy(self.dmc_config_section_sftp, SFTP_CONFIG)

        if protocol == PASTE_CONFIG:
            if self.config_section_paste not in self.config.sections():
                raise ConfigSectionNotFound('{} section not found in dmc.ini'.format(
                    self.config_section))
            else:
                self.dmc_config_section_paste = self.config[self.config_section_paste]

                self.deploy(self.dmc_config_section_paste, PASTE_CONFIG)

    def deploy(self, config_protocol, protocol):
        self._banner()

        if protocol == FTP_CONFIG:
            prepare_files = PrepareFiles(
                self.dmc_config_section, self.dmc_config_section_ftp)
        elif protocol == SFTP_CONFIG:
            prepare_files = PrepareFiles(
                self.dmc_config_section, self.dmc_config_section_sftp)
        elif protocol == PASTE_CONFIG:
            prepare_files = PrepareFiles(
                self.dmc_config_section, self.dmc_config_section_paste, True)

        filepaths, dirpaths = prepare_files.filter_items()
        if 'path' in config_protocol:
            remote_path = config_protocol['path'].strip()
            # create recursive remote paths
            remote_path_arr = remote_path.split('/')
        else:
            remote_path_arr = []

        if protocol != PASTE_CONFIG:
            # open root dir for sftp
            if protocol == SFTP_CONFIG:
                self.connect._chdir('/')
            for rpa in remote_path_arr:
                if rpa != '':
                    self.connect.chdir_recursive(rpa.strip())

            for dp in dirpaths:
                if dp == '.' or dp == './':
                    continue

                self.connect.mkdir(dp)

            for f in filepaths:
                self.connect.upload_file(f, remote_path)

            print(crayons.green('All files is deployed!', bold=True))
        else:
            """`dirpaths` for method `paste` is an a dict like {'path_file': 'file_name'}"""
            pack_files = PackFiles(dirpaths)
            package = pack_files.create_pkg()
            if 'name_paste' not in config_protocol:
                raise NotFoundPasteName(
                    'Please set `paste_name` in you `dmc.ini` config file for this dir')
            paste = PASTE(package, config_protocol)
            if 'token' not in config_protocol:
                paste.fetch_token(self.paste_expire)

            link, token = paste.paste_files()
            pack_files.delete_pkg()

            print(crayons.green(
                'You paste available: {}'.format(crayons.yellow(link, bold=True))))
            print(crayons.green('Token: {}'.format(
                crayons.yellow(token, bold=True))))

    def _banner(self):
        print(crayons.yellow(
            ' ____  _____ _____\n|    \|     |     |\n|  |  | | | |   --| Start! v.{}\n|____/|_|_|_|_____|\n'.format(__version__), bold=True))
