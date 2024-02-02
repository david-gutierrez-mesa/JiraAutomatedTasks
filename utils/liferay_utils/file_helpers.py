import glob


def create_output_files(*args):
    for message_file in args:
        create_output_file(message_file[0], message_file[1])


def create_output_file(message, message_file_name):
    if message != '':
        f = open(message_file_name, "a")
        f.write(message)
        f.close()


def search_file_inside_dir(dir_path, file_name):
    for path in glob.glob(f'{dir_path}/**/{file_name}', recursive=True):
        return path
