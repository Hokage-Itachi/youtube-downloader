import re

def title_formatter(title):
    title = re.sub("[!@#$%\^&*()<>/?`~\'\" ]", "-", title)
    return title
