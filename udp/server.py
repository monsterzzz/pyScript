import hashlib
import os
import random
import socket
import struct
import time

from tqdm import tqdm


class Server:
    buff_size = 20480
    max_file_name = 255
    fmt = "{}s32siii{}s".format(max_file_name, buff_size)
    stc_len = struct.calcsize(fmt)
    contentStc = struct.Struct(fmt)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, addr, port, save_path="./static/"):
        self.save_path = save_path
        self.addr = addr
        self.port = port
        self.s.bind((self.addr, self.port))

    def file_md5_check(self, file_path, md5):
        f1 = open(file_path, "rb")
        h1 = hashlib.md5()
        h1.update(f1.read())
        f1.close()
        file_md5 = h1.hexdigest()

        tqdm.write("remote file md5: {}".format(md5))
        tqdm.write("local file md5: {}".format(file_md5))
        tqdm.write("md5 check: {} == {} {}".format(file_md5, md5, file_md5 == md5))

    def run(self):
        n = 1
        tm = None

        while True:
            data, client = self.s.recvfrom(self.stc_len)

            file_name, md5, chunk, total_chunk, chunk_size, content = self.contentStc.unpack(data)
            file_name = str(file_name.strip(b"\x00"), "utf-8")
            md5 = str(md5, "utf-8")
            tmp_file = self.save_path + "{}.tmp".format(md5)

            if chunk == 1:

                n = 1
                if tm:
                    tm.close()
                tm = tqdm(total=total_chunk)
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)

            if chunk != n:
                self.s.sendto("error{}".format(n).encode(), client)
                continue

            with open(tmp_file, "ab+") as f:
                f.write(content[:chunk_size])

            self.s.sendto("ok{}".format(n).encode(), client)
            n += 1

            tm.update(1)

            if chunk == total_chunk:
                n = 1
                if not os.path.exists(self.save_path + "{}".format(file_name)):
                    final_name = self.save_path + "{}".format(file_name)
                    os.rename(tmp_file, final_name)
                else:
                    file_str = file_name.split(".")[0]
                    count = 0
                    for i in os.listdir("./static"):
                        if not os.path.isdir(self.save_path + "{}".format(i)) and file_str in i:
                            count += 1

                    file_split = file_name.split(".")
                    final_name = self.save_path + "{}({}).{}".format(file_split[0], count, file_split[1])
                    os.rename(tmp_file, final_name)

                tm.close()
                self.file_md5_check(final_name, md5)





s = Server("127.0.0.1",8888)
s.run()
