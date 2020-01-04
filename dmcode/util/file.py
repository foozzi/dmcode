import os
from dmcode import CONFIG_FILE
import pickle
from binaryornot.check import is_binary
from pathlib import Path


class PrepareFiles:
    def __init__(self, config, ftp_config, is_paste=False):
        self.config = config
        self.is_paste = is_paste

        self.ignore_files_arr = config['ignore_files'].strip().split(',')
        self.ignore_dirs_arr = config['ignore_dirs'].strip().split(',')
        self.ignore_ext_arr = config['ignore_ext'].strip().split(',')
        self.max_size_dir = int(config['max_size_dir_mb'].strip())
        self.max_size_file = int(config['max_size_file_mb'].strip())

        if 'path' in ftp_config:
            self.remote_path = ftp_config['path']
        else:
            self.remote_path = ''

    def _bytesto(self, bytes, to='m', bsize=1024):
        a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
        r = float(bytes)
        for i in range(a[to]):
            r = r / bsize

        return(r)

    def _prepare(self, dirpath, dirnames, filenames):
        # remove ignored dirs
        dirnames = [
            name for name in dirnames if name not in self.ignore_dirs_arr]

        # check and remove config file
        if CONFIG_FILE in filenames:
            filenames.remove(CONFIG_FILE)

        # remove ignore ext files
        if '' not in self.ignore_ext_arr:
            filenames = [name for name in filenames if os.path.splitext(
                name)[1] not in self.ignore_ext_arr]
        # remove ignore files
        filenames = [
            name for name in filenames if name not in self.ignore_files_arr]
        # check allowed size for file
        filenames = [name for name in filenames if self._bytesto(
            os.path.getsize(os.path.join(dirpath.replace('./', ''), name))) < self.max_size_file]

        filenames = list(filter(lambda name: os.path.islink(
            os.path.join(dirpath, name)) is not True, filenames))

        # check allowed size for dir
        dirnames = [name for name in dirnames if self._bytesto(
            self.get_size_dir(name)) < self.max_size_dir]

        return dirnames, filenames

    def get_size_dir(self, dir):
        dir_size = 0
        for dirpath, dirnames, filenames in os.walk(dir):

            for f in filenames:
                fp = os.path.join(dirpath, f)
                dir_size += os.path.getsize(fp)
        return dir_size

    def filter_items(self):
        paths = []
        files = []

        for dirpath, dirnames, filenames in os.walk('./'):
            _dirnames, _filenames = self._prepare(dirpath, dirnames, filenames)
            cleandirpath = dirpath.replace('./', '')
            for _f in _filenames:
                """set dict for `paste` method"""
                if self.is_paste and not os.path.islink(dirpath):
                    if cleandirpath == "":
                        paths.append({'file': _f})
                    else:
                        paths.append({'path': cleandirpath, 'file': _f})
                files.append(os.path.join(dirpath, _f))
            """if don't use `paste` method"""
            if not self.is_paste:
                if not os.path.islink(dirpath):  # check symbolic link
                    paths.append(os.path.join(
                        self.remote_path, cleandirpath))

        return files, paths


class PackFiles():
    def __init__(self, paths):
        self.paths = paths
        self.tmp_package_name = 'package_dmcode.pickle'
        self.data = []

    def create_pkg(self):
        for f in self.paths:
            """join path and file from dict"""
            """if the length is not more than 1 this is the root file"""
            if len(f) == 2:
                __f = os.path.join(f['path'], f['file'])
            else:
                __f = f['file']
            if is_binary(__f):
                continue
            with open(__f, 'rb') as _f:
                def path(f): return f['path'] if len(f) == 2 else ''
                self.data.append({'name': f['file'], 'content': _f.read(
                ), 'path': path(f)})
        with open(self.tmp_package_name, 'wb') as f:
            pickle.dump(self.data, f)

        return Path(self.tmp_package_name).absolute()

    def delete_pkg(self):
        os.remove(self.tmp_package_name)
