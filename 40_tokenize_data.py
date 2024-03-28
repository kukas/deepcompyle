from transformers import PreTrainedTokenizerFast
tokenizer = PreTrainedTokenizerFast(tokenizer_file="../tokenizers/bpe_combined_ByteLevel_8000vocab_10000subset.json")

from glob import glob
from tqdm import tqdm
binary_files = glob("../data/processed/codeparrot-clean-train/compiled-3.8.18/*.txt")
code_files = glob("../data/codeparrot-clean-train/original_code/*.py")

results = []
from collections import Counter
import pandas as pd
counter_bytecode = Counter()
counter_code = Counter()
for filename in tqdm(binary_files + code_files):
    # print(filename)
    with open(filename, "r") as f:
        text = f.read()
        # print(text)
        tokenized = tokenizer(text)
        # tokens = tokenizer.convert_ids_to_tokens(tokenized["input_ids"])
        tokens = tokenized["input_ids"]
        
        type = "bytecode" if filename.endswith(".txt") else "code"
        if type == "bytecode":
            counter_bytecode.update(tokens)
        else:
            counter_code.update(tokens)

        results.append({
            "filename": filename,
            "type": type,
            "tokens": len(tokenized["input_ids"]),
        })

pd.DataFrame(results).to_csv("40_tokenize_data.csv", index=False)
pd.DataFrame(counter_bytecode.most_common()).to_csv("token_stats_bytecode.tsv",sep='\t',index=False,header=False)
pd.DataFrame(counter_code.most_common()).to_csv("token_stats_code.tsv",sep='\t',index=False,header=False)

