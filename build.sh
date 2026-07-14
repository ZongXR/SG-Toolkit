#!/bin/bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi --config-file .pypirc dist/*
python3 -m twine upload --config-file .pypirc dist/*