# -*- coding: utf-8 -*-
import setuptools
import sg_toolkit


base_url = "https://github.com/ZongXR/SG-Toolkit"
with open("./README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
packages = list(filter(lambda x: not x.startswith("test"), setuptools.find_packages()))
requires_list = open('./requirements.txt', 'r', encoding='utf8').readlines()
requires_list = [x.strip() for x in requires_list if (not x.startswith("setuptools")) and (not x.startswith("twine")) and (not x.startswith("packaging"))]


setuptools.setup(
    name="SG-Toolkit",
    version=sg_toolkit.__version__,
    author="Xiangrui Zong",
    author_email="zxr@tju.edu.cn",
    description="Some automatic scripts to against formalism",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=base_url,
    packages=packages,
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.7,<3.11',
    install_requires=requires_list
)