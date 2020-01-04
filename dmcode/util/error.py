class FilesSizeError(Exception):
    """Raise if size greaten more than permitted"""


class FileDeployNotFound(Exception):
    """Raise if file not found for deploying"""


class FileConfigNotFound(Exception):
    pass


class ErrorSettingsFTP(Exception):
    """Raise when ftp settings is empty"""


class ErrorSettingsSFTP(Exception):
    """Raise when sftp settings is empty"""


class ConfigSectionNotFound(Exception):
    """Raise if config section not found in file dmc.ini"""


class UploadFileNotFoundError(Exception):
    """Raise if not found file for upload"""

class ServerApiIsNotResponding(Exception):
    """Raise if api server not working or not responding"""

class NotFoundPasteName(Exception):
    """Raise if not set `paste_name` in config"""

class ServerApiError(Exception):
    """Raise if server return error"""
