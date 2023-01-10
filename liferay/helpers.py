def create_output_files(warning, info, warning_file_name, info_file_name):
    if warning != '':
        f = open(warning_file_name, "a")
        f.write(warning)
        f.close()

    if info != '':
        f = open(info_file_name, "a")
        f.write(info)
        f.close()