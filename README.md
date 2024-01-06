# mlx-whatsapp

This is an experimental project to convert your chat backups from Whatsapp to finetune mistral using mlx. The `lora.py`, `models.py` and `convert.py` are from [https://github.com/ml-explore/mlx-examples](https://github.com/ml-explore/mlx-examples)

## How to backup your chats

Go to whatsapp -> Settings -> Export Chat -> Select group conversation -> Without Media 


## Download Mistral and convert to quantized version

Install the dependencies:

```
pip install -r requirements.txt
```

Next, download and convert the model. The Mistral weights can be downloaded with:

```
curl -O https://files.mistral-7b-v0-1.mistral.ai/mistral-7B-v0.1.tar
tar -xf mistral-7B-v0.1.tar
```

Convert the model with:

```
python convert.py \
    --torch-path mistral-7B-v0.1 \
    --mlx-path mistral_mlx_q -q
```

## Converting the files

Save your file exported from whatsapp as `chat.txt`. Then create the training files below

```bash
python whatsapp.py --input_file chat.txt --output_file chat.jsonl --test_file data/test.jsonl --train_file data/train.jsonl --valid_file data/valid.jsonl
```

By default the test and validation files take 30 samples. You can adjust them.


## Training

```bash
 python lora.py --model mistral_mlx_q --train --iters 600 --data ./data --batch-size 2 --adapter-file whatsapp.npz
```

## Inference

```bash
python lora.py --model ./mistral_mlx_q \
               --adapter-file ./whatsapp.npz \
               --num-tokens 500 \
               --prompt \
               "Mickey Mouse: Hey Minnie, are we going to the fair
               Minnie: "
```