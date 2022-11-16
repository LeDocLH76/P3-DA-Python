
def date_fr2iso(date_fr: str) -> str:
    """Transform string date from fr like to iso

    Args:
        str: like dd/mm/yyyy

    Return:
        str: like yyyy-mm-dd

    """
    birth_date_list = date_fr.split("/")
    if len(birth_date_list[0]) < 2:
        birth_date_list[0] = "0" + birth_date_list[0]
    if len(birth_date_list[1]) < 2:
        birth_date_list[1] = "0" + birth_date_list[1]
    birth_date_invert_list = reversed(birth_date_list)
    birth_date_iso = "-".join(birth_date_invert_list)
    return birth_date_iso


def date_iso2fr(date_iso: str) -> str:
    """Transform string date from iso to fr like

    Args:
        str: like yyyy-mm-dd

    Return:
        str: like dd/mm/yyyy

    """

    date_list = date_iso.split("-")
    date_list.reverse()
    date_fr = "/".join(date_list)
    return date_fr


def date_add_0(date_fr: str) -> str:
    """Add 0 for day and month if missing

    Args:
        str: like dd/mm/yyyy or d/m/yyyy or mix of them

    Return:
        str: like dd/mm/yyyy

    """
    date_list = date_fr.split("/")
    if len(date_list[0]) < 2:
        date_list[0] = "0" + date_list[0]
    if len(date_list[1]) < 2:
        date_list[1] = "0" + date_list[1]
    return "/".join(date_list)
