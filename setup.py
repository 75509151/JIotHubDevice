import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'requirements.txt'), 'r', 'utf-8') as f:
    requires = f.read()

setup(name="jdevice",
        version="1.0",
        description="IotDevice SDK",
        author="jay",
        author_email="75509151@qq.com",
        install_requires=requires,
        )
