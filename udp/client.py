import math
import os
import socket
import struct
import hashlib

from tqdm import tqdm


class Client:
    buff_size = 20480
    max_file_name = 255
    fmt = "{}s32siii{}s".format(max_file_name, buff_size)

    def __init__(self, addr, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((addr, port))
        self.s.settimeout(1)

    def send_file(self, send_to):
        file_path = input("please input file path:")
        file_size = os.stat(file_path).st_size
        file_name = os.path.basename(file_path)

        if len(file_name) > 255:
            raise Exception("file name is too long!")

        file_name = bytes(file_name, encoding="utf-8")
        source_file = open(file_path, 'rb')

        source_file.seek(0)
        h1 = hashlib.md5()
        h1.update(source_file.read())
        file_md5 = bytes(h1.hexdigest(), encoding="utf-8")

        source_file.seek(0)
        total_chunks = math.ceil(file_size / self.buff_size)
        current_chunk = 1

        send_pack = 0
        chunk_queue = [source_file.read(self.buff_size)]

        bar = tqdm(total=total_chunks)

        while True:
            if current_chunk >= total_chunks + 1:
                break

            if len(chunk_queue) == 0:
                chunk_queue.append(source_file.read(self.buff_size))
            chunk_size = len(chunk_queue[0])
            s = struct.pack(self.fmt, file_name, file_md5, current_chunk, total_chunks, chunk_size, chunk_queue[0])

            self.s.sendto(s, send_to)
            send_pack += 1

            # if no reply, resend!
            while True:
                try:
                    data, client = self.s.recvfrom(255)
                    break
                except socket.timeout:
                    self.s.sendto(s, send_to)
                    send_pack += 1

            # if reply != ok-chunk, resend!
            # print(data, current_chunk)
            if data == "ok{}".format(current_chunk).encode():
                bar.update()
                chunk_queue = chunk_queue[1:]
                current_chunk += 1
            else:
                continue
        source_file.close()
        bar.close()

        tqdm.write("total send packs : {}".format(send_pack))
        self.s.close()


c = Client("127.0.0.1", 12345)
c.send_file(("127.0.0.1", 8888))
# print(math.ceil(os.stat("test.rmvb").st_size/2048) )
