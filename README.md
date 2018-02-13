# Insight-donation-analytics
Solution to https://github.com/InsightDataScience/donation-analytics


## Set up prerequisites
My solution is written in **Python3** (3.6.4) with **Numpy** (1.14.0).

Create and activate a virtual environment with Python3:
```
python3 -m venv myenv
source myenv/bin/activate
```
And then install the dependencies:
```
pip install -r requirements.txt
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
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── percentile.txt
            |   │   └── itcont.txt
            |   |__ output
            |   │   └── repeat_donors.txt
            └── test_2
                ├── input
                │   └── percentile.txt
                │   └── itcont.txt
                |__ output
                    └── repeat_donors.txt

This shows my submission has the correct directory structure and the correct format of the input/output files.

#### test_1:
From https://github.com/InsightDataScience/donation-analytics/blob/master/README.md#example

#### test_2:
From https://github.com/InsightDataScience/donation-analytics/blob/master/README.md#example-1


## Instructions to test

```
(myenv) tongs-mbp:Insight-donation-analytics tongliu$ ls
```
`LICENSE
backup
insight_testsuite
output
run.sh
README.md
input
myenv
requirements.txt
src
`

```
(myenv) tongs-mbp:Insight-donation-analytics tongliu$ cd insight_testsuite/
```

```
(myenv) Tongs-MBP:insight_testsuite tongliu$ ./run_tests.sh
```