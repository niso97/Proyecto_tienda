def validar_rut(rut):
    """
    Verifica si un RUT chileno es válido.

    Args:
        rut (str): El RUT a verificar en formato "XXXXXXXX-X"

    Returns:
        bool: True si el RUT es válido, False en caso contrario.
    """
    rut = rut.replace(".", "").replace("-", "")
    cuerpo = rut[:-1]
    dv = rut[-1].upper()

    suma = 0
    factor = 2

    for i in reversed(cuerpo):
        suma += int(i) * factor
        factor += 1
        if factor > 7:
            factor = 2

    resto = suma % 11
    dv_calculado = 11 - resto

    if dv_calculado == 11:
        dv_calculado = "0"
    elif dv_calculado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_calculado)

    return dv_calculado == dv
