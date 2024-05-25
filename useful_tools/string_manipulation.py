import re

def camel_case_to_snake_case(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
    # remove double underscores to handle cases like "camel_Case"
    return re.sub('_+', '_', name)

# simpler version (does not handle HTTPServer or CVShare)
# def camel_case_to_snake_case(string):
#     return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', string).lower()

# simpler version (does not handle repeated capital letters)
# def camel_case_to_snake_case(string):
#     return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

def snake_case_to_camel_case(string):
    return ''.join(word.title() for word in string.split('_'))
    # it is impossible to know whether a word used to be capitalized or not
    # so we just capitalize all words, plain and simple