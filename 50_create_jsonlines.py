#!/usr/bin/env python

# sacrebleu format to jsonlines

import io
import json
import re
import pandas as pd
import os

src_lang, tgt_lang = ["bytecode", "code"]

df = pd.read_csv("40_tokenize_data.csv")
df["id"] = df["filename"].map(lambda f: os.path.basename(f).split(".")[0])
df_bytecode = df[df.type=="bytecode"].join(df[df.type=="code"].set_index("id"), on="id", lsuffix="_bytecode", rsuffix="_code")
df_short = df_bytecode[(df_bytecode.tokens_bytecode+df_bytecode.tokens_code < 1024)]

from sklearn.model_selection import train_test_split

# Splitting into train and remaining data
df_train, df_remaining = train_test_split(df_short, test_size=0.2, random_state=42)

# Splitting remaining data into valid and test in equal proportions
df_valid, df_test = train_test_split(df_remaining, test_size=0.5, random_state=42)

# Print the lengths of the datasets to verify proportions
print("Train set length:", len(df_train))
print("Validation set length:", len(df_valid))
print("Test set length:", len(df_test))
# all_ids = set(df_short.id.values)


for split, df in zip(["train", "valid", "test"], [df_train, df_valid, df_test]):
    fout = f"../data/jsonlines/{split}.json"
    with open(fout, "w", encoding="utf-8") as f:
        for i, row in df.iterrows():
            bytecode = open(row["filename_bytecode"], "r").read()
            code = open(row["filename_code"], "r").read()
            out = {"translation": { src_lang: bytecode, tgt_lang: code } }
            x = json.dumps(out, indent=0, ensure_ascii=False)
            x = re.sub(r'\n', ' ', x, 0, re.M)
            f.write(x + "\n")

        # for type in ["source", "target"]:
        #     fin = f"{split}.{type}"
        #     recs.append([line.strip() for line in open(fin)])
        # for src, tgt in zip(*recs):
        #     out = {"translation": { src_lang: src, tgt_lang: tgt } }
        #     x = json.dumps(out, indent=0, ensure_ascii=False)
        #     x = re.sub(r'\n', ' ', x, 0, re.M)
        #     f.write(x + "\n")