from transformers import PreTrainedTokenizerFast
tokenizer = PreTrainedTokenizerFast(tokenizer_file="../tokenizers/bpe_combined_whitespace_8000vocab_500subset.json")
# from tokenizers.models import BPE
# from tokenizers import Tokenizer
# tokenizer = Tokenizer(BPE())
# tokenizer.from_file("../tokenizers/bpe_combined_whitespace_8000vocab_500subset.json")

from glob import glob
from tqdm import tqdm
binary_files = glob("../data/processed/codeparrot-clean-train/compiled-3.8.16/*.txt")
code_files = glob("../data/codeparrot-clean-train/original_code/*.py")

results = []
from collections import Counter
counter_bytecode = Counter()
counter_code = Counter()
for filename in tqdm(binary_files + code_files):
    # print(filename)
    with open(filename, "r") as f:
        text = f.read()
        # print(text)
        tokenized = tokenizer(text)
        tokens = tokenizer.convert_ids_to_tokens(tokenized["input_ids"])
        
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

import pandas as pd
pd.DataFrame(results).to_csv("40_tokenize_data.csv", index=False)
pd.DataFrame(counter_bytecode.most_common()).to_csv("token_stats_bytecode.tsv",sep='\t',index=False,header=False)
pd.DataFrame(counter_code.most_common()).to_csv("token_stats_code.tsv",sep='\t',index=False,header=False)


# from transformers import AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer

# model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

# training_args = Seq2SeqTrainingArguments(
#     output_dir="my_awesome_opus_books_model",
#     evaluation_strategy="epoch",
#     learning_rate=2e-5,
#     per_device_train_batch_size=16,
#     per_device_eval_batch_size=16,
#     weight_decay=0.01,
#     save_total_limit=3,
#     num_train_epochs=2,
#     predict_with_generate=True,
#     fp16=True,
#     push_to_hub=True,
# )

# trainer = Seq2SeqTrainer(
#     model=model, transfo
#     args=training_args,
#     train_dataset=tokenized_books["train"],
#     eval_dataset=tokenized_books["test"],
#     tokenizer=tokenizer,
#     data_collator=data_collator,
#     compute_metrics=compute_metrics,
# )

# trainer.train()