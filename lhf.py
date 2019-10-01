#!/usr/bin/env python3

import os
import re
import argparse
import time
import os.path

TIME_PATTERN = re.compile(r"^\w+\s\d{1,2}\s\w+\s\d{2,4}\s(\d{2}:\d{2}:\d{2})\.\d{3}", re.IGNORECASE)

def secs(t):
    return (t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec)

def process_file(file_path, delta):
    print("process file: {0}".format(file_path))
    with open(file_path) as f:
        count = 0
        prev_time = 0
        prev_log = ""
        prev_count = 0
        for line in f:
            match = TIME_PATTERN.search(line)
            if not match:
                #print("Invalid line: {0}".format(line))
                count += 1
                continue
            ts = int(secs(time.strptime(match.group(1), "%H:%M:%S")))
            if prev_time > 0:
                if (ts - prev_time) >= delta:
                    print("********************************")
                    print("{0}: {1}{2}: {3}\n".format(prev_count, prev_log, count, line))
            prev_time = ts
            prev_log = line
            prev_count = count
            count += 1

def process_dir(dir_path, delta):
    with os.scandir(dir_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                process_file(os.path.join(dir_path, entry.name), delta)

def main():
    parser = argparse.ArgumentParser(description="log hole finder")
    parser.add_argument("root", action="store", help="root directory for scan log files")
    parser.add_argument("-d", "--delta", dest="delta", required=False, type=int, default=4, help="time diff between separate lines(secs)")
    args = parser.parse_args()

    start_time = time.time()

    if os.path.isfile(args.root):
        process_file(args.root, args.delta)
    else:
        process_dir(args.root, args.delta)

    end_time = time.time()
    print("script execution: {0} ms".format((end_time - start_time) * 1000))


if __name__ == "__main__":
    main()