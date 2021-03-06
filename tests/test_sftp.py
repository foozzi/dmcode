import pytest
import os
import re
from dmcode.__main__ import create_parser
from dmcode.dmcode import DMC
from dmcode.dmcode_init import DMC_INIT
from dmcode.settings import SFTP_CONFIG


def test_config_sftp():
    if os.getcwd().split('/')[-1] != 'deploy_test':
        os.chdir('tests/deploy_test')
        if os.path.exists('./dmc.ini'):
            os.remove('./dmc.ini')
    else:
        if os.path.exists('./dmc.ini'):
            os.remove('./dmc.ini')

    parser = create_parser()
    _parser = parser.parse_args()
    _parser.sftp = True
    _parser.host = ''  # host for test
    _parser.port = 22
    _parser.login = ''  # login for test
    _parser.password = ''  # password for test
    _parser.path = '/var/www/test'  # remote path for test

    DMC_INIT(SFTP_CONFIG, _parser.host, _parser.port,
             _parser.login, _parser.password, _parser.path)
    assert os.path.exists('./dmc.ini') is True


def test_deploy_sftp(capsys):
    parser = create_parser()
    _parser = parser.parse_args()
    _parser.dmc_sftp = True

    DMC(protocol=SFTP_CONFIG)
    captured = capsys.readouterr()
    assert re.search('All files is deployed!', captured.out) is not None
