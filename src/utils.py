from datetime import datetime

import requests
import json
import os



def get_all_data_file_names(path):
    """
    Get all the data file names in the data directory.
    :return: a list of file names.
    """
    return [filename for filename in os.listdir(path) if filename.endswith(".json")]

def save_json_data(data, filename):
    with open(filename, 'x') as file:
        json.dump(data, file, indent=4)

def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def get_data(url):
    """
    Get data from the given url.
    :param url: the url of the data.
    :return: the data.
    """
    
    return requests.get(url).json()


def get_generated_date(data):
    guild_dt = data["DateGenerated"]

    guild_dt = guild_dt[:19]

    guild_dt = guild_dt.replace(":", "")

    return guild_dt


def convert_generated_dt_to_object(generated_dt):
    return datetime.strptime(generated_dt, "%Y-%m-%dT%H%M%S")



def get_all_election_data():

    """
    IDs:
    1 - AGE
    2 - Data source
    3 - Fee status
    4 - Mode of Study
    5 - Residency
    6 - Sex
    7 - Student Type (UG, PGT, PGR)
    8 - Year of Study
    9 - Department
    """

    election_url = "https://www.guildofstudents.com/svc/voting/stats/election/paramstats/189?groupIds=1,6,7,8,9&sortBy=itemname&sortDirection=ascending"

    data = get_data(election_url)

    date_generated = get_generated_date(data)

    save_json_data(data, "../data/json/raw/" + date_generated + ".json")