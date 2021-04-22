import random
import string
from pathlib import Path
from typing import Optional

import magic


class FormData:
    def __init__(self, headers: dict = {}):
        rand = "".join([random.choice(string.digits) for _ in range(25)])
        self.__boundary = f"{'-' * 25}{rand}"
        self.__payload = b""

        self.__headers = headers
        self.__headers["Content-Type"] = f"multipart/form-data; boundary={self.__boundary}"

        self.__len = 0

    def append_value(self, name: str, value: str):
        payload = f"--{self.__boundary}\r\n".encode()
        payload += f'Content-Disposition: form-data; name="{name}"\r\n'.encode()
        payload += "\r\n".encode()
        payload += f"{value}\r\n".encode()
        self.__payload += payload

    def append_file(self, name: str, file: str, filename: Optional[str] = None):
        path = Path(file)

        if filename is None:
            filename = path.name

        if not path.exists():
            raise FileNotFoundError(f"{file}が見つかりません")

        if not path.is_file():
            raise FileNotFoundError(f"{file}に指定できるのはファイルだけです")

        with open(str(path), mode="br") as f:
            buffer = f.read()

        content_type = magic.from_buffer(buffer, mime=True)

        payload = f"--{self.__boundary}\r\n".encode()
        payload += f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
        payload += f"Content-Type: {content_type}\r\n".encode()
        payload += "\r\n".encode()
        payload = payload + buffer + "\r\n".encode()
        self.__payload += payload

    def end(self):
        payload = f"--{self.__boundary}--\r\n".encode()
        self.__payload += payload
        self.__len = len(self.__payload)
        self.__headers["Content-Length"] = str(self.__len)

    @property
    def headers(self):
        return self.__headers

    @property
    def payload(self):
        return self.__payload


if __name__ == "__main__":
    formdata = FormData()

    formdata.append_value("name", "test")
    formdata.append_file("file0", r"C:\Users\root\Downloads\GRMSDK_EN_DVD.iso")
    formdata.end()

    # print(formdata.payload)

    import requests

    res = requests.post("http://127.0.0.1:5000/send", headers=formdata.headers, data=formdata.payload)
    print(res)
