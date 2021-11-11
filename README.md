# Date filter application

The purpose of this application is to filter CSV files containing medical records by the proximity of each record to a particular date.

## Usage

The application expects a .csv file containing the information from an RPDR-formatted .txt file
(it needs to be converted from pipe-delimited to comma-delimited format first. Most importantly,
there needs to be a Report\_Date\_Time column with the date formatted as month/day/year.

In order to filter the data, you also need a separate .csv file containing information about each
patient. The header will look like
```
EMPI,Report_Date_Time,days_before,days_after
```
For each EMPI, you specify the anchor date (again as month/day/year) as well as how many days
before and after the date you are interested in collecting data from. By default, if a patient is
not included in the filter file, their records will not be included in the output. To change this
behavior, check the check box.

If you want to specify patient information using other information than the EMPI (e.g. the MRN),
that works too. Simply change `EMPI` above to `MRN` (or whatever column name you choose).
Similarly, if the date column is called something else, you can change `Report_Date_Time` to the
appropriate column name. However, the third and fourth columns must be `days_before` and
`days_after` as above.

In the application, simply select your data file and filter file, and press "Filter". You will be
asked for a location to save the filtered data. The application will let you know when it is done
filtering.

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
