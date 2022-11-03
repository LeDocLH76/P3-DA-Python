def transform_date_fr_to_iso(date_fr: str) -> str:
    birth_date_list = date_fr.split("/")
    if len(birth_date_list[0]) < 2:
        birth_date_list[0] = "0" + birth_date_list[0]
    if len(birth_date_list[1]) < 2:
        birth_date_list[1] = "0" + birth_date_list[1]
    birth_date_invert_list = reversed(birth_date_list)
    birth_date_iso = "-".join(birth_date_invert_list)
    return birth_date_iso
