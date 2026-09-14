# Grok 2

This repository contains the weights of Grok 2, a model trained and used at xAI in 2024.

## Usage: Serving with SGLang

- Download the weights. You can replace `/local/grok-2` with any other folder name you prefer.

  ```
  hf download xai-org/grok-2 --local-dir /local/grok-2
  ```

  You might encounter some errors during the download. Please retry until the download is successful.  
  If the download succeeds, the folder should contain **42 files** and be approximately 500 GB.

- Launch a server.

  Install the latest SGLang inference engine (>= v0.5.1) from https://github.com/sgl-project/sglang/

  Use the command below to launch an inference server. This checkpoint is TP=8, so you will need 8 GPUs (each with > 40GB of memory).
  ```
  python3 -m sglang.launch_server --model /local/grok-2 --tokenizer-path /local/grok-2/tokenizer.tok.json --tp 8 --quantization fp8 --attention-backend triton
  ```

- Send a request.

  This is a post-trained model, so please use the correct [chat template](https://github.com/sgl-project/sglang/blob/97a38ee85ba62e268bde6388f1bf8edfe2ca9d76/python/sglang/srt/tokenizer/tiktoken_tokenizer.py#L106).

  ```
  python3 -m sglang.test.send_one --prompt "Human: What is your name?<|separator|>\n\nAssistant:"
  ```

  You should be able to see the model output its name, Grok.

  Learn more about other ways to send requests [here](https://docs.sglang.ai/basic_usage/send_request.html).

## License

The weights are licensed under the [Grok 2 Community License Agreement](https://huggingface.co/xai-org/grok-2/blob/main/LICENSE).