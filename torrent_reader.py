__file_content = ""
__read_current = 0
__content_val = False
__encode = "utf8"
__hash_type = "hex"


def read_file(file_path, encode="utf8", hash_type="hex"):
    global __file_content
    global __read_current
    global __content_val
    global __encode
    global __hash_type
    with open(file_path, "rb") as file:
        __file_content = file.read()
    __read_current = 0
    __encode = encode
    __hash_type = hash_type

    __file_content = __read()

    return __file_content


def read(file_content, encode="utf8", hash_type="hex"):
    global __file_content
    global __read_current
    global __content_val
    global __encode
    global __hash_type
    __file_content = file_content
    __read_current = 0
    __encode = encode
    __hash_type = hash_type

    __file_content = __read()

    return __file_content


def __read():
    type = True
    while True:
        type, val = __next()
        return val


def __next():
    global __read_current
    type_value = __file_content[__read_current]
    if type_value == 100:
        # 字典型
        __read_current += 1
        return "dict", __dict()
    elif type_value == 108:
        # 列表型
        __read_current += 1
        return "list", __list()
    elif type_value >= 48 and type_value <= 57:
        # 字符串型
        return "str", __str()
    elif type_value == 105:
        # 整数型
        __read_current += 1
        return "int", __int()


def __dict():
    dict_val = {}
    while not __is_end():
        type, val = __next()
        key = val

        type, val = __next()
        value = val

        dict_val[key] = value
    return dict_val


def __list():
    global __read_current
    list_val = []
    while not __is_end():
        type, val = __next()
        list_val.append(val)
    return list_val


def __str():
    global __read_current
    length = int(__read_until_colon())
    end = __read_current + length
    bytes = __file_content[__read_current:end]
    __read_current += length
    try:
        string = str(bytes, encoding=__encode)
    except UnicodeDecodeError:
        if __hash_type == "hex":
            string = "".join([hex(byte)[2:].upper().rjust(2, "0") for byte in bytes])
        else:
            string = bytes
    return string


def __int():
    global __read_current
    content = ""
    while not __is_end():
        content += chr(__file_content[__read_current])
        __read_current += 1
    return int(content)


def __read_until_colon():
    global __read_current
    content = ""
    byte = __file_content[__read_current]
    __read_current += 1
    while byte != 58:
        content += chr(byte)
        byte = __file_content[__read_current]
        __read_current += 1
    return content


def __is_end():
    # 字典或列表是否结束
    global __read_current
    if __file_content[__read_current] == 101:
        __read_current += 1
        return True
    else:
        return False
