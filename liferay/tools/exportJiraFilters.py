from __future__ import print_function

import pickle

from utils.liferay_utils.jira_utils.jira_liferay import get_jira_connection
from utils.liferay_utils.manageCredentialsCrypto import delete_credentials


def main():
    jira_url = "https://issues.liferay.com"
    jira_type = "Server"
    delete_credentials()
    jira_connection = get_jira_connection(jira_url, jira_type)
    favorite_filters = jira_connection.favourite_filters()
    user_id = jira_connection.current_user()
    jira_connection.close()
    file_name = user_id + '_filters.pkl'
    with open(file_name, 'wb') as f:
        pickle.dump(favorite_filters, f, pickle.HIGHEST_PROTOCOL)
    print('Favorite filters from user ' + user_id + ' has been exported to ' + file_name)


if __name__ == '__main__':
    main()
