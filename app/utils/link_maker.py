import hashlib

def make_link_by_id(card_id: int) -> str:
    link = hashlib.md5(str(card_id).encode("utf-8"))
    return link.hexdigest()