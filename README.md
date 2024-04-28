Sure, here is a basic template for a `README.md` file for your project:

# Length Extension Attack

This project is a Python implementation of a length extension attack. It includes a custom hash function and a class to perform the attack.

## Description
The developed hash function in this project operates on the principle of the Merkle-Damgård construction, which is used in many common hash functions such as MD5, SHA-1, and SHA-256. This construction allows a message of any length to be broken down into blocks and these blocks to be processed individually to generate a final hash value.

The hash function begins with an initial internal state. Each block of the message is then processed individually by XORing it with the current internal state and then processing it through a helper function `hash_q`, which performs an XOR operation and a left-side bit rotation. The resulting value becomes the new internal state. This process is repeated for each block of the message. In the end, the `hash_q` function is applied one last time to the internal state to generate the final hash value.

Authentication functions that are based on this hash function are vulnerable to length extension attacks. In such an attack, an attacker who knows a valid hash value and its original message can append additional data to the message and calculate a valid hash value for the extended message without knowing the secret used to calculate the original hash value.

In this project, a length extension attack is carried out by first determining the internal state before outputting the hash value for a valid hash value and its message through brute force. Subsequently, the internal state of the hash function is set to the found state and a new valid hash value for the message "Old Message" + "Additional Data" is generated with new data.

It is important that the length of the original message is a multiple of the block size of the hash function because the Merkle-Damgård construction assumes that the message is broken down into equal-sized blocks. If the length of the message is not a multiple of the block size, the message must be padded to fill the missing bits. However, this padding cannot be undone by the attacker, which means that the attacker would not be able to accurately determine the internal state of the hash function after processing the original message. Therefore, for a length extension attack to be successful, the length of the original message must be a multiple of the block size.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3.x
- pip (Python package installer)

Python packages:
- tqdm

### Installing

A step by step series of examples that tell you how to get a development environment running:

1. Clone the repository:
```bash
git clone https://github.com/01-00-11-00/length-extension-attack.git
```
2. Navigate to the project directory:
```bash
cd length-extension-attack
```
3. Install the required Python packages:
```bash
pip install tqm
```
4. Run the main script:
```bash
python main.py
```

## Authors

* **01-00-11-00** - *Initial work* - [01-00-11-00](https://github.com/01-00-11-00)
