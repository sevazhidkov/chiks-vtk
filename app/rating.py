def exceptance(r, opponent_r):
    """
    Вычисляет математическое ожидание для человека с рейтингом
    r и рейтингом оппонента opponent_r.
    """
    return 1 / (1 + 10 ** ((opponent_r - r) / 400))


def rating(r, s, opponent_r, k=40):
    """
    Вычисляет новый рейтинг для человека с текущим рейтингом r,
    результатом s (1/0.5/0), рейтингом оппотента opponent_r и
    коэффицентом k (по умолчанию - 40).
    """
    return r + 40 * (s - exceptance(r, opponent_r))
