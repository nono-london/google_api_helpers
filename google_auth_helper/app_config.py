from pathlib import Path


def get_root_full_path():
    return Path().cwd().parent


if __name__ == '__main__':
    print(get_root_full_path())
