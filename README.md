# DMC

**DMC**ode - like a *deploy my code*
Allows you to upload your code to an ftp server without any ftp/sftp clients.
[![asciicast](https://asciinema.org/a/XTxHfHiZvhOepzd6wHo36rrIi.svg)](https://asciinema.org/a/XTxHfHiZvhOepzd6wHo36rrIi)


## why is this needed?

for example, you need to quickly deploy code or files to a remote ftp or sftp server directly from a directory with easy-to-understand console commands.

### Where is working? 
Linux, MacOS, ~~Windows~~ - in progress :rocket:

### TODO v1.0

 - add mysql backup restore
 - ask user when replacing file [--replace ASK|NOT|default: replace all]
 - add save rights after deploying
 - add windows support
 - add "paste" method

### dmc.ini

Using the configuration file **dmc.ini**, you can exclude directories, files or file extensions that you do not need, and more.
Just execute the command in the desired directory for **ftp**:
```bash
dmcode --ftp_config
```
or for **sftp**:
```bash
dmcode --sftp_config
```
or specify **ftp** settings right away:
```bash
dmcode --ftp_config|--sftp_config --host <your_ftp_host> --port <your_ftp_port> --password <your_ftp_password> --path /var/www/html
```

this is to create a configuration file **dmc.ini** that you can edit.

```
[DMC]
ignore_ext = ignored extensions for upload
ignore_files = ignored file names for upload
ignore_dirs = ignored directory names for upload
max_size_dir_mb = allowed maximal directory size for upload (in Bytes)
max_size_file_mb = allowed maximal file size for upload (in Bytes)
```

## Deploy your code

Just execute:
```bash
dmcode --ftp|--sftp
```

## Setup
```bash
pip install dmcode
```
or
```bash
git clone https://github.com/foozzi/dmcode.git && cd dmcode
python setup.py install
```


