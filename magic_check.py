import argparse
import binascii
import os
import sys

import requests
from colorama import Fore, Style, init

__author__ = 'DFIRSec (@pulsecode)'
__version__ = "v0.0.3"
__description__ = 'Confirm file type by matching the magic signature ("number")'


# Ref: https://www.garykessler.net/library/file_sigs.html
file_types = {
    '7z': b'37 7a bc af 27 1c',
    'aac': b'41 41 43 00 01 00',
    'asm': b'00 61 73 6d',
    'avi': b'52 49 46 46',
    'au': b'64 6e 73 2e',
    'bin': b'53 50 30 31',
    'exe': b'4d 5a',
    'bmp': b'42 4d',
    'bz2': b'42 5a 68',
    'dat': b'50 4d 4f 43 43 4d 4f 43',
    'deb': b'21 3c 61 72 63 68 3e',
    'doc': b'cf 11 e0 a1 b1 1a e1 00',
    'elf': b'7f 45 4c 46',
    'flash': b'43 57 53',
    'flv': b'46 4c 56 01',
    'gif': b'47 49 46 38',
    'jfif': b'ff d8 ff e0 00 10 4a 46 49 46 00 01',
    'jpg': b'ff d8 ff db',
    'mkv': b'1a 45 df a3',
    'mp3': b'49 44 33',
    'mp3_hd': b'49 44 33 03 00 00 00',
    'mpeg': b'00 00 01 ba',
    'mpg2': b'00 00 01 ba 44',
    'ogg': b'4f 67 67 53',
    'ovpn': b'63 6c 69 65 6e 74 0a 64 65 76',
    'pcap': b'd4 c3 b2 a1',
    'pcapng': b'0a 0d 0d 0a',
    'pdf': b'25 50 44 46 2d',
    'png': b'89 50 4e 47 0d 0a 1a 0a',
    'rar': b'52 61 72 21 1a 07 01 00',
    'raw': b'52 41 57 41 44 41 54 41',
    'reg': b'72 65 67 66',
    'rtf': b'7b 5c 72 74 66 31',
    'sqlite': b'53 51 4c 69 74 65',
    'tar': b'75 73 74 61 72',
    'tor': b'64 38 3a 61 6e 6e 6f 75 6e 63 65',
    'vmdk': b'4b 44 4d',
    'vmem': b'53 ff 00 f0',
    'webp': b'52 49 46 46 94 45 0a 00 57 45 42 50 56 50 38',
    'wmv': b'30 26 b2 75 8e 66 cf 11 a6 d9 00 aa 00 62 ce 6c',
    'xar': b'78 61 72 21',
    'xml': b'3c 3f 78 6d 6c',
    'zip': b'50 4b 03 04'
}


class Termcolor:
    # Unicode Symbols and colors
    BOLD = Fore.LIGHTWHITE_EX
    CYAN = Fore.CYAN
    GRAY = Fore.LIGHTBLACK_EX
    GREEN = Fore.LIGHTGREEN_EX
    RED = Fore.RED
    YELLOW = Fore.LIGHTYELLOW_EX
    RESET = Style.RESET_ALL


# Initizlize colorama and termcolors
init()
tc = Termcolor()


def scan_dir(path):
    try:
        for files in os.scandir(path):
            try:
                with open(files, 'rb') as fd:
                    file_head = fd.read(20)
                    yield binascii.hexlify(file_head, ' '), files.path
            except KeyboardInterrupt:
                sys.exit("\nExited")
            except Exception:
                continue
    except PermissionError as e:
        print(e)


def main(path, filetype=None):
    found = []
    count = 0
    for x in scan_dir(path):
        try:
            if filetype:
                if file_types[filetype] in x[0]:
                    found.append(x[1])
            else:
                for k, v in file_types.items():
                    if v in x[0]:
                        print(f" {tc.BOLD}{k.upper():7}{tc.RESET}{x[1]}")
                        count += 1
        except KeyError:
            sys.exit(f"{tc.RED}[ERROR]{tc.RESET} File format '{tc.YELLOW}{filetype}{tc.RESET}' is not an available selection.")  # nopep8
        except KeyboardInterrupt:
            sys.exit("\nExited")

    if found:
        print('\n'.join([x for x in found]))

    if not found and count == 0:
        print(f"{tc.YELLOW}No matching file types found{tc.RESET}")


if __name__ == '__main__':
    banner = fr"""
        __  ___            _         ________              __  
       /  |/  /___ _____ _(_)____   / ____/ /_  ___  _____/ /__
      / /|_/ / __ `/ __ `/ / ___/  / /   / __ \/ _ \/ ___/ //_/
     / /  / / /_/ / /_/ / / /__   / /___/ / / /  __/ /__/ ,<
    /_/  /_/\__,_/\__, /_/\___/   \____/_/ /_/\___/\___/_/|_|
                 /____/
                                                {__version__}
                                                {__author__}
    """

    print(f"{tc.CYAN}{banner}{tc.RESET}")

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='path', help="Path to search")
    parser.add_argument('-f', '--filetype', help="file type selector")
    parser.add_argument('-l', '--listtype', action='store_true',
                        help="list file types")

    args = parser.parse_args()
    
    # check if new version is available
    try:
        latest = requests.get("https://api.github.com/repos/dfirsec/magic_check/releases/latest").json()["tag_name"]  # nopep8
        if latest != __version__:
            print(f"{Fore.YELLOW}* Release {latest} of magic_check is available{Fore.RESET}")  # nopep8
    except Exception as err:
        print(f"{Fore.LIGHTRED_EX}[Error]{Fore.RESET} {err}\n")

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    if args.listtype:
        print(f"{tc.GREEN}Choose from the following:{tc.RESET}")
        for k in file_types:
            print(f" {tc.GRAY}-{tc.RESET} {tc.BOLD}{k}{tc.RESET}")
    elif args.filetype:
        main(args.path, args.filetype.lower())
    else:
        main(args.path)
