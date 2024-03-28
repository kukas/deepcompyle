rm -rf ../models/bart-tiny-dummy
python run_translation.py \
    --config_name ./configs/bart-tiny.json \
    --tokenizer_name ../tokenizers/bpe_combined_ByteLevel_8000vocab_10000subset.json \
    --output_dir ../models/bart-tiny-dummy \
    --train_file ../data/jsonlines/train-dummy-repeat.json \
    --validation_file ../data/jsonlines/train-dummy.json \
    --source_lang bytecode \
    --target_lang code \
    --per_device_train_batch_size 32 \
    --learning_rate 1e-3 \
    --num_train_epochs 200 \
    --generation_max_length 1024 \
    --max_target_length 1024 \
    --evaluation_strategy epoch \
    --do_train \
    --do_eval \
    --predict_with_generate
