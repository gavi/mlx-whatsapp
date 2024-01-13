# mlx-whatsapp

This is an experimental project to convert your chat backups from Whatsapp to finetune mistral using mlx. The `lora.py`, `models.py`, `models` directory and `convert.py` are from [https://github.com/ml-explore/mlx-examples](https://github.com/ml-explore/mlx-examples)

## How to backup your chats

Go to whatsapp -> Settings -> Export Chat -> Select group conversation -> Without Media 


## Download Mistral and convert to quantized version

Install the dependencies:

```
pip install -r requirements.txt
```

Next, download and convert the model. The following command will download mistral from huggingface and convert it to quantized version

```
python convert.py --hf-path mistralai/Mistral-7B-v0.1 -q  
```


## Converting the files

Save your file exported from whatsapp as `chat.txt`. Then create the training files below

```bash
python whatsapp.py --input_file chat.txt --output_file chat.jsonl --test_file data/test.jsonl --train_file data/train.jsonl --valid_file data/valid.jsonl
```

By default the test and validation files take 30 samples. You can adjust them.


## Training

```bash
 python lora.py --model mlx_model --train --iters 600 --data ./data --batch-size 2 --adapter-file whatsapp.npz
```

## Inference

```bash
python lora.py --model ./mlx_model \
               --adapter-file ./whatsapp.npz \
               --max-tokens 500 \
               --prompt \
               "Mickey Mouse: Hey Minnie, are we going to the fair?
               Minnie: "
```

## Combine your adapter and model together

```bash
python fuse.py --model mlx_model --adapter-file whatsapp.npz --save-path fused
```

Now the folder fused contains `safetensors` that can be used directly with transformers. 

## Warning

A word of caution - Dont upload your fused models to public sites such a huggingface as your model can leak personal data that you trained it on. 