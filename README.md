# OpenAI ChatGPT Jupyter Kernel

This repository contains a Jupyter kernel module that utilizes the OpenAI ChatGPT API to provide a chatbot-like interface within Jupyter notebooks.

## Installation

To install the Jupyter Kernel Module, you can use pip:

pip install git+https://github.com/kasehiroyuki/openai_chat_kernel.git

Additionally, you will need to obtain an API key from OpenAI to use the ChatGPT API by following the instructions at https://platform.openai.com/docs/quickstart .

The OpenAI API key should be stored in the environment variable OPENAI_API_KEY.

To install the kernel, run the following command in the terminal:

python -m openai_chat_kernel.install 

## Usage

To use the ChatGPT Jupyter kernel module, create a new notebook and select "OpenAI Chat Kernel" in the kernel dropdown menu.

Once selected, you can start communicating with the ChatGPT API through the Jupyter notebook.

## Contributing

If you'd like to contribute to this project, please feel free to submit a pull request or open an issue.

## Tested Platforms

This Jupyter kernel module has been tested on the following platforms:

    Windows 11 Pro
    Python 3.10
    Jupyter Lab 3.6.1

## License

This project is licensed under the BSD 3-Clause License. See the LICENSE file for details.

