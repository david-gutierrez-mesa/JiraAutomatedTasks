#!/usr/bin/env python

import getpass
import os
from os.path import expanduser
from pathlib import Path
import keyring


def get_credentials():
    home = Path(expanduser("~"))
    folder = home / ".jira_user"
    path_to_file = folder / "credentials"

    if path_to_file.is_file():
        f = open(path_to_file, 'r')
        username = f.readline()
        f.close()
    else:
        print("The file ", path_to_file, " does not exist")
        print("No user for Jira access set as environment variable. Please set one.")
        print("Enter User and password to access Jira instance https://issues.liferay.com\n")
        username = input("Username: ")
        if not os.path.exists(folder):
            os.makedirs(folder)
        f = open(path_to_file, 'w')
        f.write(username)
        f.close()

    password = keyring.get_password("jira", username)
    if password is None:
        print("Enter credentials for jira user " + username)
        password = getpass.getpass("Password: ")
        keyring.set_password("jira", username, password)

    return username, password


if __name__ == "__main__":
    print("Set the credentials to be used when accessing jira.")
    get_credentials()
    print("Credentials set.")
