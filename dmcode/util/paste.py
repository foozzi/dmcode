import requests
from dmcode import API_URL
from dmcode.dmcode_init import DMC_INIT
from .error import ServerApiIsNotResponding, ServerApiError


class PASTE():
    def __init__(self, package, config):
        self.config = config
        self.package = package
        self.name_paste = self.config['name_paste']
        """check custom api url"""
        if 'api_url' not in config or config['api_url'].strip() != "":
            self.api_url = config['api_url']
        else:
            self.api_url = API_URL

    def fetch_token(self, expire):
        """first fetch uniq token for upload files"""
        method = '/fetch_token'
        values = {'name_paste': self.name_paste, 'expire_paste': expire}
        r = requests.post(self.api_url + method, data=values)
        if r.status_code != 200:
            raise ServerApiIsNotResponding(
                'Response api server {}, method: `{}`'.format(r.status_code, method))

        if r.json()['error']:
            raise ServerApiError(r.json()['message'])

        DMC_INIT.set_paste_token(r.json()['token'])

    def paste_files(self):
        method = '/paste_files'
        headers = {'DMTOKEN': DMC_INIT.get_paste_token()}
        files = {'dmfiles': open(self.package, 'rb')}
        r = requests.post(self.api_url + method,
                          headers=headers, files=files)

        if r.status_code != 200:
            raise ServerApiIsNotResponding(
                'Response api server {}, method: `{}`'.format(r.status_code, method))

        if r.json()['error']:
            raise ServerApiError(r.json()['message'])

        return r.json()['link'], DMC_INIT.get_paste_token()
