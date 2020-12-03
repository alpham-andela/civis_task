from .lib import transform_keys, pop_fields

def test_transform_keys_1level():
    input_dict = {'a': 'b'}
    output_dict = transform_keys(input_dict, {}, None)

    assert input_dict == output_dict , "For one level dictionary, the input should equal to the output."
    assert input_dict is not output_dict, "The input and the output should be different objects in the memory."

def test_transform_keys_2levels():
    input_dict = {'a': {'b': 'c'}}
    output_dict = transform_keys(input_dict, {}, None)
    expected_output = {'a_b': 'c'}

    assert expected_output == output_dict

def test_transform_keys_3levels():
    input_dict = {'a': {'b': {'c': 'd'}}}
    output_dict = transform_keys(input_dict, {}, None)
    expected_output = {'a_b_c': 'd'}

    assert expected_output == output_dict

def test_transform_keys_3levels_with_list():
    input_dict = {'a': {'b': {'c': ['d']}}}
    output_dict = transform_keys(input_dict, {}, None)
    expected_output = {'a_b_c': ['d']}

    assert expected_output == output_dict


def test_transform_keys_3levels_with_list_of_lists():
    input_dict = {'a': {'b': {'c': [['d', 'e'], ['f', 'g']]}}}
    output_dict = transform_keys(input_dict, {}, None)
    expected_output = {'a_b_c': [['d', 'e'], ['f', 'g']]}

    assert expected_output == output_dict

def test_transform_keys_3levels_with_list_of_lists_multiple_objects():
    input_dict = {'a': {'b': {'c': [['d', 'e'], ['f', 'g']], 'd': 1, 'e': '2'}}}
    output_dict = transform_keys(input_dict, {}, None)
    expected_output = {'a_b_c': [['d', 'e'], ['f', 'g']], 'a_b_d':1, 'a_b_e': '2'}

    assert expected_output == output_dict

def test_transform_keys_3levels_with_list_of_dicts_multiple_objects():
    input_dict = {'a': {'b': {'c': [{'d': 'e'}, {'f': 'g'}], 'd': 1, 'e': '2'}}}
    output_dict = transform_keys(input_dict, {}, None)
    expected_output = {'a_b_c': [{'d': 'e'}, {'f': 'g'}], 'a_b_d':1, 'a_b_e': '2'}

    assert expected_output == output_dict

def test_transform_keys_different_levels_multiple_objects():
    input_dict = {'a': {'b': {'c': [{'d': 'e'}, {'f': 'g'}], 'd': 1, 'e': '2'}, 'c': 3}, 'b': '2'}
    output_dict = transform_keys(input_dict, {}, None)
    expected_output = {'a_b_c': [{'d': 'e'}, {'f': 'g'}], 'a_b_d':1, 'a_b_e': '2', 'a_c': 3, 'b': '2'}

    assert expected_output == output_dict


def test_pop_one_field():
    input_dict = {'a': 1, 'b': 2, 'c': 3}
    output_dict = pop_fields('a')(input_dict)
    expected_output = {'b':2, 'c':3}
    
    assert expected_output == output_dict

def test_pop_two_or_more_fields():
    input_dict = {'a': 1, 'b': 2, 'c': 3}
    output_dict = pop_fields('a', 'b')(input_dict)
    expected_output = {'c':3}
    
    assert expected_output == output_dict


def test_pop_non_exist_fields():
    input_dict = {'a': 1, 'b': 2, 'c': 3}
    output_dict = pop_fields('d', 'b')(input_dict)
    expected_output = {'a':1, 'c':3}
    
    assert expected_output == output_dict