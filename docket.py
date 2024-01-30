import requests
from dotenv import dotenv_values
import json
import urllib
import json
import pandas as pd
import math

config = dotenv_values(".env")

def get_login_token():
    """Log in to the DocketAlarm API and retrieve login token

    Returns:
        str: Login token that lasts 90 minutes
    """
    url = 'https://www.docketalarm.com/api/v1/login/'

    data = {
        'username': config['USERNAME'],
        'password': config['PASSWORD']
    }

    try:
        response = requests.post(url, data)
        response.raise_for_status()

        token = json.loads(response.text)
        if token['success'] == True:
            return token['login_token']
        else:
            return token['error']
    except requests.exceptions.RequestException as e:
        print('Error occurred:', e)

def search_case_by_date(type, months, party=None, firm=None, attorney=None, court=None, user_limit=50):
    """This function uses the login token, generates a query string and retrieves cases from DocketAlarm.

    Args:
        type (str): The type of case required to be searched, patent, trade secrets, etc.
        months (int): The number of months to the discovery deadline.
        party (str, optional): The name of the party, Apple etc. Defaults to None.
        firm (str, optional): The name of the firm, Gibson Dunn etc. Defaults to None.
        attorney (str, optional): The name of the attorney. Defaults to None.
        court (str, optional): The name of the court/state, Texas etc. Defaults to None.
        user_limit (int, optional): Number of cases to be returned. Defaults to 50.

    Returns:
        df: A Dataframe of cases, with party names, case numbers and links to dockets.
    """
    try:
        login_token = get_login_token()
    except:
        return
    results = pd.DataFrame(columns=["cache_unofficial", "court", "datetime_cached", "date_filed", "title", "link_snippet", 
                                    "link", "docket", "result_type", "date_cached"])
    # Temp variable for limit control
    curr = user_limit
    limit=50

    # Iterate to re-query the API, getting around the 50 case limit
    for i in range(math.ceil(user_limit/50)):
        print("Running iteration", i)
        new_offset = i + limit if i>0 else 0
        if curr < 50:
            limit = curr
        args = {
            'login_token': login_token,
            'q': 'is:docket type:{}'.format(type)
            + ' court:{}'.format(court) if court is not None else print("no court") 
            + ' deadline:(discovery next:({} months))'.format(months)
            + ' party:{}'.format(party) if party is not None else print("no party")
            + ' firm:{}'.format(firm) if firm is not None else print("no firm")
            + ' attorney:{}'.format(attorney) if attorney is not None else print("no attorney"),
            "limit": limit,
            "offset": new_offset
        }

        encoded_args = urllib.parse.urlencode(args)
        url = 'http://www.docketalarm.com/api/v1/search/?'+ encoded_args

        fp = urllib.request.urlopen(url)

        response = fp.read()

        json_response = json.loads(response)

        curr -= limit
    
        # Print the output
        if json_response['success'] is True:
            temp = pd.DataFrame(json_response['search_results'])
            results = pd.concat([results, temp], ignore_index=True)
        else:
            print(json_response['error'])
    return results


if __name__ == "__main__":
    print("This docket search identifies dockets where discovery is within a user specified number of months.\n")
    type = input("Enter the type of matter you want cases for (e.g. patent, trade secrets): ")
    months = input("Enter the number of months to the discovery deadline: ")
    party = input("Enter the party name (leave blank if none): ")
    firm = input("Enter the firm name (leave blank if none): ")
    attorney = input("Enter the attorney's name (leave blank if none): ")
    court = input("Enter the court for your search (leave blank if none): ")
    user_limit = input("Enter the number of cases you want returned: ")
    cases = search_case_by_date(type, int(months), party, firm, attorney, court, int(user_limit))
    print("\nYour search results have been stored in a csv file.")
    cases.to_csv("results.csv")