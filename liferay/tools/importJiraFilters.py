from __future__ import print_function

import logging
import pickle

from jira import JIRAError

from utils.liferay_utils.jira_utils.jira_helpers import set_filter_permissions
from utils.liferay_utils.jira_utils.jira_liferay import get_jira_connection
from utils.liferay_utils.manageCredentialsCrypto import delete_credentials

DEFAULT_URL = "https://liferay.atlassian.net/"
LOG_FILE_NAME = '_log_file.log.log'


def main():
    print("Please, enter the URL of Jira instance where you want to import your filters\n")
    jira_url = input("Jira URL (pres enter to use " + DEFAULT_URL + "): ") or DEFAULT_URL
    jira_type = "Cloud"
    delete_credentials()
    jira_connection = get_jira_connection(jira_url, jira_type)
    user_id = jira_connection.user(jira_connection.current_user()).emailAddress.split('@')[0]
    log_file_name = user_id + LOG_FILE_NAME
    logging.basicConfig(filename=log_file_name,
                        filemode='w',
                        format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
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
            logging.info('[SKIPPING] Filter "' + filter_to_import.name + '" exists in destination. Skipping')
            skipped += 1
        else:
            try:
                description = ''
                if hasattr(filter_to_import, 'property'):
                    description = filter_to_import.description
                new_filter = jira_connection.create_filter(name=filter_to_import.name,
                                                           description=description,
                                                           jql=filter_to_import.jql,
                                                           favourite=filter_to_import.favourite)
                logging.info('[IMPORTED] Filter "' + filter_to_import.name + '" did NOT exists in destination and was '
                                                                             'imported')
                permissions_message = set_filter_permissions(jira_connection,
                                                             jira_url,
                                                             new_filter,
                                                             filter_to_import.sharePermissions)
                logging.error(permissions_message)
                imported += 1
            except JIRAError as err:
                logging.error('Filter "' + filter_to_import.name +
                              '" can not be automatically imported. Please create it manually:\n    ' +
                              filter_to_import.name + '\n    ' +
                              filter_to_import.jql +
                              '\n  Error message:' + err.text)
                error += 1
    jira_connection.close()
    summary = ('\n\nTOTAL RESULTS:\n'
               '   Successfully imported = ' + str(imported) + '\n' +
               '   Skipped since already exist = ' + str(skipped) + '\n' +
               '   Need to be imported manually = ' + str(error) + '\n' +
               ' NOTE: for the imported filters you need to verify the permission since they may not been imported\n' +
               'Check ' + LOG_FILE_NAME + ' file for details.')

    logging.info(summary)
    print(summary)


if __name__ == '__main__':
    main()
