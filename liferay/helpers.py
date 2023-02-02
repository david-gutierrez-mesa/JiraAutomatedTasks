def create_output_files(warning, info, warning_file_name, info_file_name):
    create_output_file(warning, warning_file_name)
    create_output_file(info, info_file_name)


def create_output_file(message, message_file_name):
    if message != '':
        f = open(message_file_name, "a")
        f.write(message)
        f.close()
