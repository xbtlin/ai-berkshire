---
license: apache-2.0
pipeline_tag: text-generation
library_name: grok
tags:
- grok-1
---
# Grok-1

This repository contains the weights of the Grok-1 open-weights model. You can find the code in the [GitHub Repository](https://github.com/xai-org/grok-1/tree/main).

# Download instruction
Clone the repo & download the `int8` checkpoint to the `checkpoints` directory by executing this command in the repo root directory:

```shell
git clone https://github.com/xai-org/grok-1.git && cd grok-1
pip install huggingface_hub[hf_transfer]
huggingface-cli download xai-org/grok-1 --repo-type model --include ckpt-0/* --local-dir checkpoints --local-dir-use-symlinks False
```

Then, you can run:

```shell
pip install -r requirements.txt
python run.py
```

You should be seeing output from the language model.

Due to the large size of the model (314B parameters), a multi-GPU machine is required to test the model with the example code.

p.s. we're hiring: https://x.ai/careers