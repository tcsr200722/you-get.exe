#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import sys
from itertools import product

ROOT = os.path.normpath(os.path.join(os.path.abspath(__file__), "../../.."))
CI = os.path.join(ROOT, ".ci")

WORKFLOW_MATRIX = {
    "python-version": ["3.7", "3.8", "3.9", "3.10", "3.11"],
    "arch": ["x86", "x64"],
}


def main():
    sys.path.append(ROOT)
    from scripts.artifact import ArtifactInfo

    for item in product(*WORKFLOW_MATRIX.values()):
        py_version = item[0] + ".0"
        py_arch = "64" if item[1] == "64" else "32"
        artifact_dir = os.path.join(CI, "you-get_py{}_{}".format(*item))
        artifact_name = f"you-get_0.9.9999_win{py_arch}_py{py_version}_UB231231.zip"

        info = ArtifactInfo(
            filename=artifact_name,
            sha256=hex(random.getrandbits(256))[2:-1].ljust(64, "z"),
            py_version=py_version,
            py_arch=py_arch,
            poetry_version="0.0.0",
            pyinstaller_version="0.0.0",
        )

        os.makedirs(artifact_dir, exist_ok=True)
        with open(os.path.join(artifact_dir, "artifact_info.json"), "w", encoding="utf-8") as f1:
            f1.write(info.json())
        with open(os.path.join(artifact_dir, artifact_name), "w", encoding="utf-8") as f2:
            f2.write("This is a fake zip archive file.")

    print(f" * To simulate CI environment, a lots of test files have been created under\n   `{CI}`.\n")
    print(" * Now you can test `scripts/ci/main.py` locally with:\n")
    print("     python scripts/ci/main.py --poetry 1.4.0 --main 3.8")


if __name__ == '__main__':
    main()