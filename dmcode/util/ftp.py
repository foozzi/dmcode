import os
import tqdm
from ftplib import FTP, error_perm
import sys
from .error import UploadFileNotFoundError


class _FTP():
    def __init__(self, host, port, login, password):
        self.host = host
        self.port = port
        self.login = login
        self.password = password

        self.ftp = FTP()
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.login, self.password)

    def directory_exists(self, dir):
        filelist = []
        self.ftp.retrlines('LIST', filelist.append)
        for f in filelist:

            if f.split()[-1] == dir and f.upper().startswith('D'):
                return True
        return False

    def mkdir(self, dir):
        # (or negate, whatever you prefer for readability)
        if self.directory_exists(dir) is False:
            try:
                self.ftp.mkd(dir)
            except error_perm:
                pass

    def chdir_recursive(self, dir):
        # (or negate, whatever you prefer for readability)
        if self.directory_exists(dir) is False:
            self.ftp.mkd(dir)
        self.ftp.cwd(dir)

    def upload_file(self, filepath, remote_path):
        if not os.path.exists(filepath):
            raise UploadFileNotFoundError('File {} not found'.format(filepath))

        self.ftp.cwd(remote_path)
        with open(filepath, 'rb') as fd:
            total = os.path.getsize(filepath)
            with tqdm.tqdm(total=total,
                           unit_scale=True,
                           unit='B',
                           desc='[DMC upload {}]: '.format(filepath),
                           miniters=1,
                           file=sys.stdout,
                           leave=False) as tqdm_inst:
                self.ftp.storbinary('STOR {}'.format(filepath), fd,
                                    callback=lambda sent: tqdm_inst.update(len(sent)))
