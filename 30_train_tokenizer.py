from tokenizers.trainers import BpeTrainer
from tokenizers.models import BPE
from tokenizers import Tokenizer, decoders, processors, normalizers, pre_tokenizers
tokenizer = Tokenizer(BPE())
processing = "ByteLevel"
if processing == "ByteLevel":
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    # tokenizer.normalizer = normalizers.NFKC()
    tokenizer.decoder = decoders.ByteLevel(add_prefix_space=False)
    tokenizer.post_processor = processors.ByteLevel(add_prefix_space=False)
elif processing == "Metaspace":
    tokenizer.pre_tokenizer = pre_tokenizers.Metaspace()
    tokenizer.decoder = decoders.Metaspace()

# tokenizer.pre_tokenizer = Split(pattern=r'\w+|\s', behavior='isolated')
vocab_size = 8000
trainer = BpeTrainer(
    vocab_size=vocab_size,
    max_token_length=16,
    initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
    # limit_alphabet=350,
    special_tokens=["<PAD>", "<BOS>", "<EOS>"],
)

subset = 1000
from glob import glob
from random import shuffle
binary_files = glob("../data/processed/codeparrot-clean-train/compiled-3.8.16/*.txt")
shuffle(binary_files)
binary_files = binary_files[:subset]
code_files = glob("../data/codeparrot-clean-train/original_code/*.py")
shuffle(code_files)
code_files = code_files[:subset]

all_files = binary_files + code_files

# convert binary to hex
# def data_iterator():
#     for file in glob("../data/processed/codeparrot-clean-train/compiled-3.8.16/*.txt"):
        # code = open(file, "rb").read()
        # yield code.hex()
# tokenizer.train_from_iterator(iter(data_iterator()), trainer=trainer)

tokenizer.train(all_files, trainer=trainer)
import os
os.makedirs(f"../tokenizers", exist_ok=True)
tokenizer_path = f"../tokenizers/bpe_combined_{processing}_{vocab_size}vocab_{subset}subset.json"
tokenizer.save(tokenizer_path)
# try loading the tokenizer
tokenizer.from_file(tokenizer_path)
# tokenizer loading fails if the trained tokens contain whitespaces...
