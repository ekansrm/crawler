def load_cookies(path: str):
    with open(path, "r") as fp:
        rv = []
        for line in fp.readlines():
            cookies = dict({key.strip(): val.strip() for key, val in [item.split("=") for item in line.split(";")]})
            rv.append(cookies)
        return rv


if __name__ == '__main__':
    cookies_list = load_cookies("cookies.txt")
    print(cookies_list)
