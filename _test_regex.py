import re


# while True:
#     date_ = input("Entrer la date > jj/mm/aaaa ")
#     if date_ == "Q":
#         break
#     # date_regex = re.compile('^[0-9]{0,1}[0-9]$')
#     date_regex = re.compile(
#         r"^(0?[1-9]|[1-2]\d|3[01])/(0?[1-9]|1[0-2])/(19|20)\d\d$")
#     # $')
#     resp = date_regex.match(date_)
#     print(resp)

classification = None
while classification is None:
    if classification == "Q":
        break
    classification = input("Classement > Entier positif non nul ou vide ")
    if classification == "":
        classification = None
        break
    classification_regex = re.compile(r"^[1-9]\d{0,5}$")
    classification = classification_regex.match(classification)
    print(classification)
if classification is not None:
    print(classification.group())
else:
    print(classification)
