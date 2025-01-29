import sys
import os
import torrent_reader as tr
import public_common as pc
import math
import hashlib


def split_string_into_chunks(s, chunk_size=10):
    return [s[i : i + chunk_size] for i in range(0, len(s), chunk_size)]


def check_chunk(chunk):
    global checked_hash_list, check_result_simple
    hash_val = hashlib.new("sha1", chunk).hexdigest().upper()

    if hash_val != hash_list[len(checked_hash_list)]:
        check_result_simple[file_real_path] = False

    checked_hash_list.append(hash_val)


torrent_file_path = input("种子文件路径：")
# torrent_file_path = "./[2023.11.01] BanG Dream! MyGO!!!!! 1stアルバム「迷跡波」[FLAC 96kHz／24bit].torrent"

torrent_info = tr.read_file(torrent_file_path)

pc.j.save_json(torrent_info, "torrent_info.json")

# 获取 info 部分
info = torrent_info["info"]
torrent_name = info["name"]
print(torrent_name)
for each_file in info["files"]:
    print("\t" + "\\".join(each_file["path"]))

file_size_total = sum([each["length"] for each in info["files"]])
chunk_size = info["piece length"]
piece_count = math.ceil(file_size_total / chunk_size)
hash_length = int(len(info["pieces"]) / piece_count)

hash_list = split_string_into_chunks(info["pieces"], hash_length)
pc.j.save_json(hash_list, "hash_list")

need_check_file_path = input("校验文件路径：")
# need_check_file_path = (
#     ".\\[2023.11.01] BanG Dream! MyGO!!!!! 1stアルバム「迷跡波」[FLAC 96kHz／24bit]"
# )

checking_file_path = False
chunk = b""
checked_hash_list = []

check_result = {}
check_result_simple = {}

for each_file in info["files"]:
    file_path = "\\".join(each_file["path"])
    file_real_path = os.path.realpath(os.path.join(need_check_file_path, file_path))
    check_result_simple[file_real_path] = True
    checking_file_path = file_real_path
    print(file_real_path)
    with open(file_real_path, "rb") as file:
        chunk += file.read(chunk_size - len(chunk))
        while len(chunk) == chunk_size:
            check_chunk(chunk)
            chunk = file.read(chunk_size)

if len(chunk) != 0:
    check_chunk(chunk)

# pc.j.save_json(checked_hash_list, "checked_hash_list")
try:
    pc.j.save_json(check_result_simple, torrent_name + "_check_result_simple")
except:
    pc.j.save_json(check_result_simple, "_check_result_simple")
