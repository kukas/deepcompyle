import re
def generate_alphabet():
    for _i in range(256):
        i = _i
        if _i >= 0 and _i <= 31:
            i = _i + 255
        # if _i == 32:
        #    i = 0x005F
        if _i >= 127 and _i <= 160:
            i = _i + 255
        char = chr(i)
        # print(_i, char, re.match(r"\s", char))
        yield (_i, char)

alphabet = dict(generate_alphabet())
print(alphabet, file=open("alphabet.txt", "w"))
# print(alphabet)

from glob import glob
import os

path = "../data/codeparrot-clean-train/compiled-3.8.16"
outdir = "../data/processed/codeparrot-clean-train/compiled-3.8.16"
os.makedirs(outdir, exist_ok=True)
for pyc in glob("../data/codeparrot-clean-train/compiled-3.8.16/*.pyc"):
    filename = os.path.basename(pyc)
    out_path = os.path.join(outdir, filename+".txt")
    with open(pyc, "rb") as f, open(out_path, "w") as out:
        code = f.read()
        output = []
        for byte in code:
            output.append(alphabet[byte])

        out.write("".join(output))
