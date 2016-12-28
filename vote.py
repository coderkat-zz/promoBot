#!/usr/bin/python
from datetime import datetime, time
import random
import requests
import urllib.request

from bs4 import BeautifulSoup

import constants


def num_converter(s):
    try:
        return int(s)
    except ValueError:
        print('problem converting str to an int')
        pass


def upvote(votes, *uids):
    for _ in range(votes):
        for uid in uids:
            values = {'text' : random.choice(constants.upvote_comments), 'vote':'yes', 'uniq':uid}
            # Send HTTP POST request to upvote
            r = requests.post(constants.post_url, data=values)


def downvote(uid, votes):
    for _ in range(votes):

        values = {'text' : random.choice(constants.downvote_comments), 'vote':'no', 'uniq':uid}
        # Send HTTP POST request to downvote
        r = requests.post(constants.post_url, data=values)


def determine_vote_needs(num_votes):
    found_me = 0
    others_found = False

    # Once a day, upvote my codes no matter what
    earliest = datetime.strptime('17:45', '%H:%M').time()
    latest = datetime.strptime('18:5', '%H:%M').time()
    if earliest < datetime.utcnow().time() < latest:
        print(datetime.utcnow().time())

        upvote(num_votes, *constants.my_unique_ids)

    # Fetch current version of website, write to txt file
    with urllib.request.urlopen(constants.get_url) as response, open(
        constants.write_file, 'wb'
    ) as out_file:
        data = response.read()
        out_file.write(data)

    # Use newly written file for soup
    soup = BeautifulSoup(open(constants.write_file),  'html.parser')
    code_id_list = soup.find_all(id="vote_number_text")

    for _ in range(num_votes):

        for code_id in code_id_list:
            uid = num_converter(code_id.attrs['c_id'])  # will fetch the unique_id & cast to int
            if found_me == 3:
                # If we've gotten to 3, we've iterated through every code that's above me.
                return others_found
            elif uid not in constants.my_unique_ids:
                # If we find a uid that's not mine, mark that we need to re-run this
                others_found = True
                # Then downvote once, and upvote each of mine once.
                downvote(uid, num_votes)
                upvote(num_votes, *constants.my_unique_ids)
            else:
                found_me += 1
    return others_found

others_found = determine_vote_needs(constants.num_votes)
tries = 1
while others_found and tries <= 10:
    tries += 1
    determine_vote_needs(constants.force_it_votes)
else:
    print("we're number one")
    

