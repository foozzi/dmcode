#!/bin/python3
import argparse
import sys
import random
import crayons
import string
from .dmcode import DMC
from .dmcode_init import DMC_INIT
from .settings import __version__, FTP_CONFIG, SFTP_CONFIG, PASTE_CONFIG


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ftp_config', help='initialization for FTP settings',
                        required=False, action='store_true')
    parser.add_argument('--sftp_config', help='initialization for SFTP settings',
                        required=False, action='store_true')
    parser.add_argument('--paste_config', help='initialization for PASTE-server settings',
                        required=False, action='store_true')
    parser.add_argument('--host', help='ftp host', required=False, default='')
    parser.add_argument('--port', help='ftp port (deafult 21)',
                        required=False, default='')
    parser.add_argument('--login', help='ftp login user',
                        required=False, default='')
    parser.add_argument('--password', help='ftp password user',
                        required=False, default='')
    parser.add_argument('--path', help='remote path',
                        required=False, default='')
    parser.add_argument('--ftp', help='deploying files from dir to ftp server',
                        required=False, action='store_true')
    parser.add_argument('--sftp', help='deploying files from dir to sftp server',
                        required=False, action='store_true')
    parser.add_argument('--paste', help='deploying files from dir to paste server like a `pastebin`',
                        required=False, action='store_true')
    parser.add_argument(
        '--api_key', help='api key for deploying files to paste server [API IN DEVELOPING]', required=False, default='test')
    parser.add_argument(
        '--api_url', help='if you have own dmcode-server you can set custom api_url [SERVER IN DEVELOPMENT]', required=False, default='')
    parser.add_argument(
        '--name_paste', help='name paste name when you deploying files to paste-server', required=False, default='')
    parser.add_argument(
        '--expire', help='expire paste, default 1 month [format: 10min 1hour, 1day, 1week, 1month] example: --parse 10min, 1hour, 1day, 1week, 1month',
        required=False, default='1month')
    parser.add_argument('-v', '--version', help='dmc version',
                        required=False, action='store_true')

    return parser


def main():
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if parser.parse_args().version is True:
        parser.exit(0, "dmcode %s\n" % __version__)

    random_paste_name = ''.join(random.choice(
        string.ascii_lowercase) for i in range(10))

    if parser.parse_args().ftp_config is True or parser.parse_args().sftp_config is True or \
            parser.parse_args().paste_config is True:
        type = FTP_CONFIG
        _parser = parser.parse_args()
        if _parser.ftp_config is True:
            if _parser.port.strip() == '':
                _parser.port = 21
        elif _parser.sftp_config is True:
            type = SFTP_CONFIG
            if _parser.port.strip() == '':
                _parser.port = 22
        elif _parser.paste_config is True:
            parser.exit('PASTE METHOD NOT WORKING IN THIS VERSION')
            type = PASTE_CONFIG

        """if paste name is empty"""
        # if _parser.name_paste == "":
        #    """set random paste name"""
        #    _parser.name_paste = random_paste_name

        DMC_INIT(type, _parser.host, _parser.port, _parser.login,
                 _parser.password, _parser.path, _parser.api_key,
                 random_paste_name, _parser.api_url)

        print(crayons.green(
            '\nConfig created: You can open dmc.ini and edit file config in directory'))
        parser.exit()

    _parser = parser.parse_args()
    if _parser.ftp is True:
        DMC(protocol=FTP_CONFIG)
    elif _parser.sftp is True:
        DMC(protocol=SFTP_CONFIG)
    elif _parser.paste is True:
        """checking expire paste"""
        parser.exit('PASTE METHOD NOT WORKING IN THIS VERSION')
        """init simple config file for work with paste"""
        DMC_INIT(PASTE_CONFIG, name_paste=random_paste_name)
        print(crayons.green(
            '\nConfig created: You can open dmc.ini and edit file config in directory'))
        DMC(protocol=PASTE_CONFIG, paste_expire=_parser.expire)


if __name__ == "__main__":
    main()
