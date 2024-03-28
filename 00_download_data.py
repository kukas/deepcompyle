from datasets import load_dataset
from tqdm import tqdm
# download only the first archive
dataset = load_dataset(
    "codeparrot/codeparrot-clean-train", data_files="file-000000000001.json.gz"
)

print(dataset)

for sample in tqdm(dataset["train"]):
    # todo: shard the data according to the gz archives
    with open(
        f"../data/codeparrot-clean-train/original_code/{sample['hash']}.py", "w"
    ) as f:
        f.write(sample["content"])

    # py_compile.compile('data/codeparrot-clean-train/test.py', 'data/codeparrot-clean-train/test.pyc')
