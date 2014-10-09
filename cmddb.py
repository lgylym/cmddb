__author__ = 'yluo'
"""
cmddb stick to GNU Coreutils commands and gawk:
https://www.gnu.org/software/coreutils/manual/html_node/index.html

also inspired by
http://www.catonmat.net/blog/set-operations-in-unix-shell/
http://matt.might.net/articles/sql-in-the-shell/
"""

import ssqlparser
opened_files = {}


def add_file(alias, file_path, delimiter=' '):
    """
    This function add a text file to the db
    :param alias: alias of the file in db
    :param file_path: path of the file, the presentation in the command
    :param delimiter: delimiter to separate fields
    """
    if delimiter == '\t':
        delimiter = '\\t'
    opened_files[alias] = (file_path, delimiter)
    #print(opened_files)


def generate_command(script):
    """
    This function generate an executable command from the script
    :param script: the SQL script
    :return: the command(s)
    """
    result = ssqlparser.parse(script)
    #print(len(result[2]))
    command = ''

    output_file = None
    if result[0] not in ssqlparser.reserved.keys():  # then the first must be the output folder
        output_file = opened_files[result[0]]  # output_file is a list now
        result = result[1]

    print result
    if (result[0] == 'select') & (len(result[2]) == 1):  # one data source
        input_file = result[2][0]
        assert input_file in opened_files

        if output_file:
            output_columns = output_file[1].join(result[1])

        where_condition = result[3]
        if where_condition:
            

        print output_columns
#        command = 'cut -d\'' + opened_files[result[2][0]][1] + '\' -f ' +  + ' ' + \
#                  opened_files[result[2][0]][0]
    return 'command'


if __name__ == "__main__":
    add_file('data', '/123/456/data', '\t')
    add_file('output', '12334', '" "')
    print(generate_command('output = select $1,$2 from data;'))