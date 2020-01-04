import paramiko
import os
import sys
from .error import UploadFileNotFoundError


def tqdmWrapViewBar(*args, **kwargs):
    from tqdm import tqdm
    pbar = tqdm(*args, **kwargs)  # make a progressbar
    last = [0]  # last known iteration, start at 0

    def viewBar2(a, b):
        pbar.total = int(b)
        pbar.update(int(a - last[0]))  # update pbar with increment
        last[0] = a  # update last known iteration
    return viewBar2, pbar  # return callback, tqdmInstance


class SFTP():
    def __init__(self, host, port, login, password):
        transport = paramiko.Transport((host, port))
        transport.connect(username=login, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(transport)

    def directory_exists(self, dir):
        result = None
        try:
            self.sftp.stat(dir)
        except FileNotFoundError:
            result = False
        else:
            result = True

        return result

    def mkdir(self, dir):
        if self.directory_exists(dir) is False:
            self.sftp.mkdir(dir)

    def _chdir(self, dir):
        self.sftp.chdir(dir)

    def chdir_recursive(self, dir):
        if not self.directory_exists(dir):
            self.sftp.mkdir(dir)
            self.sftp.chdir(dir)
        else:
            self.sftp.chdir(dir)

    def upload_file(self, filepath, remote_path):
        if not os.path.exists(filepath):
            raise UploadFileNotFoundError('File {} not found'.format(filepath))

        cbk, pbar = tqdmWrapViewBar(
            unit='B',
            unit_scale=True,
            desc='[DMC upload {}]: '.format(filepath),
            miniters=1,
            file=sys.stdout,
            leave=False)
        remote_path = os.path.join(remote_path, filepath)
        self.sftp.put(filepath, remote_path, callback=cbk)
