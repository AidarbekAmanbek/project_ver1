from data.concrete import CONCRETE_CLASSES

def calc_max_min_beam_rebar(concrete):
    f_ctm = CONCRETE_CLASSES[concrete]["fctm"]
    f_yk = 1
    b_t = 1
    d = 1

    A_smin = 0.26 * (f_ctm/f_yk) * b_t * d
    A_smin_nominal = 0.0013 * b_t * d

    return (A_smin, A_smin_nominal)