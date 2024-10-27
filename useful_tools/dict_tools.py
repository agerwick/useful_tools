def get_dict_slice(ordered_dict, position, end_position=None):
    """
    Get dictionary item(s) by position from an ordered dictionary
    
    Args:
        ordered_dict (dict): The ordered dictionary (or regular dict from python 3.7) to extract the item from
        position (int): The position of the item to extract
        end_position (int): The end position of the item to extract (default: same as position)
    
    Returns:
        dict: The dictionary item(s) at the specified position(s)

    Raises:
        IndexError: If the position or end_position is out of range
        TypeError: If ordered_dict is not a dictionary
    """
    if not isinstance(ordered_dict, dict):
        raise TypeError(f"Ordered dict must be a dictionary. {ordered_dict} {type(ordered_dict).__name__}")
    if not isinstance(position, int):
        raise TypeError(f"Position must be an integer. {position} is a {type(position).__name__}")
    if end_position is not None and not isinstance(end_position, int):
        raise TypeError(f"End position must be an integer. Got {type(end_position).__name__}")

    part_of_dict = {}
    if len(ordered_dict) > 0:
        if end_position is None:
            end_position = position
        if position < 0 or position >= len(ordered_dict):
            raise IndexError(f"Position {position} out of range for dictionary of length {len(ordered_dict)}")
        if end_position < 0 or end_position >= len(ordered_dict):
            raise IndexError(f"End position {end_position} out of range for dictionary of length {len(ordered_dict)}")
        for i, (key, value) in enumerate(ordered_dict.items()):
            if i >= position and i <= end_position:
                part_of_dict[key] = value
    return part_of_dict
