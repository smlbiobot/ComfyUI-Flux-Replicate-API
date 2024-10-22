# ComfyUI-Flux-Replicate-API
Flux Pro via Replicate API

- Create API key at https://replicate.com/account/api-tokens
- Copy `config.ini.example` to `config.ini` and put the replicate key there. 

## Node

![workflow-1.1.png](static/workflow-1.1.png)

## Installation

Navigate to where you have installed ComfyUI. For example:

```shell
cd ~/dev/ComfyUI/
```

Go to the custom nodes folder:

```shell
cd custom_nodes
```

Clone this repo

```shell
git clone https://github.com/smlbiobot/ComfyUI-Flux-Replicate-API
```

Go inside the repo folder

```shell
cd ComfyUI-Flux-Replicate-API
```

Install the requirements

```shell
pip install -r requirements.txt
```

Copy the example config `config.ini.example` to `config.ini`, then edit the `config.ini` with the actual Repliate API token.

```shell
cp config.ini.example config.ini
```

Start ComfyUI.

## Version History

- 2024-10-22: Updated to Replicate Flex Pro 1.1. Please note that this version is not compatible with Replicate Flex Pro 1.0 because of changed parameter