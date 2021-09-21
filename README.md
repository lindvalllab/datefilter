# Date filter application

The purpose of this application is to filter CSV files containing medical records by the proximity of each record to a particular date.

## Getting started developing

Make sure you have Python 3 installed and that `python` points to a version > 3.
```
python --version
```
In the root directory of the project create a virtual environment.
```
python -m venv dfenv
```
Activate the virtual environment and install dependencies.
```
source dfenv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```
