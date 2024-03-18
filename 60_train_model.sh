python run_translation.py \
    --config_name ./configs/bart-tiny.json \
    --tokenizer_name ../tokenizers/bpe_combined_ByteLevel_8000vocab_1000subset.json \
    --output_dir ../models/bart-tiny-test \
    --train_file ../data/jsonlines/train.json \
    --validation_file ../data/jsonlines/valid.json \
    --source_lang bytecode \
    --target_lang code \
    --do_train \
    --do_eval
