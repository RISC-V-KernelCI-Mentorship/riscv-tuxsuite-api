import hashlib

def generate_test_id(test_uid: str, test_collection: str, test: str) -> str:
    test_id = f"{test_uid}-{test_collection}-{test}".encode()
    sha256 = hashlib.sha256()
    sha256.update(test_id)
    return sha256.hexdigest()

def get_test_path(collection: str, test: str, separator:str="-") -> str:
    split_test = test.split(separator)
    if len(split_test) == 1:
        parsed_test = split_test[0]
    else:
        parsed_test = separator.join(split_test[1:])
    return f"{collection}.{parsed_test}"