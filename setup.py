import os
import sys
from setuptools import setup

try:
    import dmcode
except ImportError:
    print("error: dmcode requires Python 3 or greater.")
    sys.exit(1)

base_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_path, 'requirements.txt'), 'r') as f:
    requirements = f.read().split('\n')

with open(os.path.join(base_path, 'README.md'), 'r') as f:
    description = f.read()

VERSION = dmcode.__version__
DOWNLOAD = "https://github.com/foozzi/dmcode/archive/%s.tar.gz" % VERSION

setup(
    name='dmcode',
    version=VERSION,
    author='Tkachenko Igor',
    author_email='foozzione@gmail.com',
    description='Allows you to upload your code to an ftp server without any ftp-clients.',
    packages=['dmcode', 'dmcode.util'],
    install_requires=requirements,
    entry_points={
            'console_scripts':
                ['dmcode = dmcode.__main__:main']
        },
    long_description=description,
    long_description_content_type='text/markdown',
    keywords='ftp, ftp-client, deploy, upload',
    license='GNU',
    url='https://github.com/foozzi/dmcode',
    download_url=DOWNLOAD,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only"
    ],
    test_suite="tests"
)
