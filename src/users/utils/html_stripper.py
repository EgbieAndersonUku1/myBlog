from re import compile, sub
import html


def strip_html_tags(text):
    """Remove html tags from a string"""

    pattern = compile('<.*?>')
    return sub(pattern, '', text)