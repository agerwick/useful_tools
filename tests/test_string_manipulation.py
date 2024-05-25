import unittest
from useful_tools.string_manipulation import camel_case_to_snake_case, snake_case_to_camel_case

def test_camel_case_to_snake_case_1():
    assert camel_case_to_snake_case('camelCase') == 'camel_case'
def test_camel_case_to_snake_case_2():
    assert camel_case_to_snake_case('CamelCase') == 'camel_case'
def test_camel_case_to_snake_case_3():
    assert camel_case_to_snake_case('camelCASE') == 'camel_case'
def test_camel_case_to_snake_case_4():
    assert camel_case_to_snake_case('CamelCASE') == 'camel_case'
def test_camel_case_to_snake_case_5():
    assert camel_case_to_snake_case('camel_Case') == 'camel_case'
def test_camel_case_to_snake_case_6():
    assert camel_case_to_snake_case('CVShare') == 'cv_share'
    assert camel_case_to_snake_case('CAMELCase') == 'camel_case'
def test_snake_case_to_camel_case():
    assert snake_case_to_camel_case('snake_case') == 'SnakeCase'
    assert snake_case_to_camel_case('SNAKE_CASE') == 'SnakeCase'
    assert snake_case_to_camel_case('snake_Case') == 'SnakeCase'
    assert snake_case_to_camel_case('SNAKE_Case') == 'SnakeCase'
