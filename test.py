# encoding:utf-8
import sys

import time

def progress_bar(i):
        sys.stdout.flush()
        print("\r", end="")
        print("Download progress: {}%: ".format(i), "▋" * (i // 2), end="")
        time.sleep(0.05)

for i in range(100):
    progress_bar(i+1)
