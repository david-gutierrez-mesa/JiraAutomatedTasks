from __future__ import print_function

import pickle

from jira import JIRAError

from jira_liferay import get_jira_connection
from manageCredentialsCrypto import delete_credentials
from utils.jira_helpers import set_filter_permissions


def main():
    print("Please, enter the URL of Jira instance where you want to import your filters\n")
    jira_url = input("Jira URL: ")
    jira_type = "Cloud"
    delete_credentials()
    jira_connection = get_jira_connection(jira_url, jira_type)
    user_id = jira_connection.user(jira_connection.current_user()).emailAddress.split('@')[0]
    file_name = user_id + '_filters.pkl'
    with open(file_name, 'rb') as inp:
        filters_to_import = pickle.load(inp)
    existing_filters = jira_connection.favourite_filters()
    error = 0
    imported = 0
    skipped = 0
    filters_to_import.sort(key=lambda x: x.id, reverse=False)

    for filter_to_import in filters_to_import:
        if any(obj.name == filter_to_import.name for obj in existing_filters):
            print('[SKIPPING] Filter "' + filter_to_import.name + '" exists in destination. Skipping')
            skipped += 1
        else:
            try:
                description = ''
                if hasattr(filter_to_import, 'property'):
                    description = filter_to_import.description
                new_filter = jira_connection.create_filter(name=filter_to_import.name, description=description,
                                                           jql=filter_to_import.jql,
                                                           favourite=filter_to_import.favourite)
                print(
                    '[IMPORTED] Filter "' + filter_to_import.name + '" did NOT exists in destination and was imported')
                for permission in filter_to_import.sharePermissions:
                    set_filter_permissions(jira_connection, jira_url, new_filter, permission)
                imported += 1
            except JIRAError as err:
                print('[ERROR] Filter "' + filter_to_import.name +
                      '" can not be automatically imported. Please create it manually:\n    ' + filter_to_import.jql +
                      '    Log:\n', err)
                error += 1
    print('\n\nTOTAL RESULTS:\n'
          '   Successfully imported = ' + str(imported) + '\n' +
          '   Skipped since already exist = ' + str(skipped) + '\n' +
          '   Need to be imported manually = ' + str(error) + '\n' +
          ' NOTE: for the imported filters you need to verify the permission since they are not imported')


if __name__ == '__main__':
    main()
