#!/usr/bin/env python

import getpass
from pathlib import Path
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from os.path import expanduser
from shutil import rmtree

FOLDER_NAME = ".jira_user"


def delete_credentials():
    home = Path(expanduser("~"))
    folder = home / FOLDER_NAME
    rmtree(folder)


def get_credentials():
    home = Path(expanduser("~"))
    folder = home / FOLDER_NAME
    path_to_user = folder / "user"
    path_to_password = folder / "credentials"
    private_key_file = folder / "keys"

    if path_to_user.is_file():

        with open(private_key_file, 'rb') as f:
            key = RSA.import_key(f.read())

        with open(path_to_user, 'rb') as f:
            username = f.readline().decode().rstrip()

        with open(path_to_password, 'rb') as f:
            encrypted_password = f.read()

        decryptor = PKCS1_OAEP.new(key)
        password = decryptor.decrypt(encrypted_password).decode()

    else:
        print('The file', path_to_user, 'does not exist')
        print("Enter e-mail and token to access Jira instance. Password is not allowed anymore.\n")
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        key = RSA.generate(2048)
        encryptor = PKCS1_OAEP.new(key)
        encrypted_password = encryptor.encrypt(password.encode())

        if not os.path.exists(folder):
            os.makedirs(folder)

        f = open(path_to_user, 'wb')
        f.write(username.encode())
        f.close()

        f = open(path_to_password, 'wb')
        f.write(encrypted_password)
        f.close()

        private_handle = open(private_key_file, 'wb')
        private_handle.write(key.export_key('PEM'))
        private_handle.close()

    return username, password


if __name__ == "__main__":
    print("Set the credentials to be used when accessing jira.")
    delete_credentials()
    get_credentials()
    print("Credentials set.")
