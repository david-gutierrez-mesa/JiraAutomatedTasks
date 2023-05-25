from __future__ import print_function

import pickle

from jira_liferay import get_jira_connection


def main():
    jira_connection = get_jira_connection()
    favorite_filters = jira_connection.favourite_filters()
    user_id = jira_connection.current_user()
    file_name = user_id + '_filters.pkl'
    with open(file_name, 'wb') as f:
        pickle.dump(favorite_filters, f, pickle.HIGHEST_PROTOCOL)
    print('Favorite filters from user ' + user_id + ' has been exported to ' + file_name)


if __name__ == '__main__':
    main()
