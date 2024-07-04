def read_html(file_path):
    """Load HTML file

    Args:
        file_path: html file

    Returns:
        string: html file
    """
    with open(file_path, "r") as file:
        return file.read()


def write_new_html(data, html_name):
    """Write new html file with replaced animal data

    Args:
        data (string): animal data
        html_name (string): name of the file
    """
    with open(html_name, 'w') as file:
        file.write(data)