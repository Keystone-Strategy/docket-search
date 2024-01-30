# Docket-Search

This project leverages DocketAlarm's API to search for new cases to identify leads.

## Structure

This project 1 .py file, `docket.py`. This file authenticates the script with the DocketAlarm API, and also constructs the query.

For now, `docket.py` is interactable via the CLI, with specific user supplied arguments. 

## API Reference

You will need access to the following:

1. `DocketAlarm Login Email Address`, and

2. `DocketAlarm Login Password`

These can be found on [KWIC](https://keystonestrategy.atlassian.net/wiki/spaces/KB/pages/3175809448/Research+Resources+Subscriptions).

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`USERNAME`

`PASSWORD`

## Installation

Once you have downloaded the project directory, 

```bash
  cd docket-search
  pip3 install -r requirements.txt
```

## Run Locally

1. Add a .env file, and include the environment variables as listed above.
2. Run the `docket.py` script, and follow the instructions to search for cases.
3. The output is a `results.csv` file stored in the same project directory.
