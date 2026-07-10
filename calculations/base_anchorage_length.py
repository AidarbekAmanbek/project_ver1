def calculate_base_anchorage_length(diameter, sigma_sd, f_bd):
    """
    Calculate the required base anchorage length.

    Parameters:
    diameter (float): Diameter of the reinforcement bar.
    sigma_sd (float): Design stress in the reinforcement.
    f_bd (float): Design bond stress.

    Returns:
    float: Required base anchorage length.
    """

    l_brqd = round((diameter / 4) * (sigma_sd / f_bd),3)

    return l_brqd