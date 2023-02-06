def create_output_files(*args):
    for message_file in args:
        create_output_file(message_file[0], message_file[1])


def create_output_file(message, message_file_name):
    if message != '':
        f = open(message_file_name, "a")
        f.write(message)
        f.close()
