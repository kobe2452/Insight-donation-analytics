# Insight-donation-analytics
Solution to https://github.com/InsightDataScience/donation-analytics


## Set up prerequisites
My solution is written in **Python3** (3.6.4) with **Numpy** (1.14.0).

Once you clone my repo, please create and activate a virtual environment with **Python3**:
```
Insight-donation-analytics~$ python3 -m venv myenv
Insight-donation-analytics~$ source myenv/bin/activate
```
And then install the dependencies:
```
(myenv) Insight-donation-analytics~$ pip install -r requirements.txt
```
Now, you are good to test my submission.


## Repository structure

The submission directory structure is:

    ├── README.md 
    ├── run.sh
    ├── src
    │   └── donation-analytics.py
    ├── input
    │   └── percentile.txt
    │   └── itcont.txt
    ├── output
    |   └── repeat_donors.txt
    ├── insight_testsuite
    |   └── run_tests.sh
    |   └── tests
    |       └── test_1
    |       |   ├── input
    |       |   │   └── percentile.txt
    |       |   │   └── itcont.txt
    |       |   |__ output
    |       |   │   └── repeat_donors.txt
    |       └── test_2
    |           ├── input
    |           │   └── percentile.txt
    |           │   └── itcont.txt
    |           |__ output
    |               └── repeat_donors.txt
    ├── .gitignore
    ├── LICENSE
    ├── requirements.txt

The test suite contains:

#### test_1 (default):
From https://github.com/InsightDataScience/donation-analytics/blob/master/README.md#example

#### test_2:
From https://github.com/InsightDataScience/donation-analytics/blob/master/README.md#example-1


## Instructions to test

```
(myenv) Insight-donation-analytics~$ cd insight_testsuite/
```

```
(myenv) insight_testsuite~$ ./run_tests.sh
```

The output of `run_tests.sh` should look like the following:
```
Line 1 in input/itcont.txt is invalid.
[PASS]: test_1 repeat_donors.txt
[PASS]: test_2 repeat_donors.txt
[Mon Feb 12 18:47:31 EST 2018] 2 of 2 tests passed
```


## Approach brief

1. Utilizing the header information and format (source: https://classic.fec.gov/finance/disclosure/metadata/indiv_header_file.csv), I streamed the input lines one by one (not at one time).

2. For each line, I checked its validity based on given rules (source: https://github.com/InsightDataScience/donation-analytics/blob/master/README.md#input-file-considerations), and then continued with valid lines in extraction and analysis and returned error message for invalid ones.

3. For each unique donor, I recorded their transaction years so that obtained the repeat donors with their latest donation year.

4. For each calendar year found in (3.), recipient and zip code, I retrieved and calculated the running percentile of contributions from repeat donors (reference: https://stackoverflow.com/a/26071170/), the total amount of donations streaming in, and the total number of transactions from repeat donors.

5. Write the extraction and calculation results to `repeat_donors.txt` in the same order as the donation appeared in the input file, thanks to Python 3.6 (reference: https://stackoverflow.com/a/39537308/ and https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-compactdict).