# 🔧 python-tree-sitter-types

This repository contains a python typed interface generation tool for tree-sitter grammars.


## Installation
Installation is simple with pip:
```bash
pip install tree-sitter-types
```

## Usage
This library provides two functions.

As a CLI you can use it to generate the types for your tree-sitter grammar:
```bash
python-tree-sitter-types node-types.json your_language_types.py
```

You can then package these and distribute them on pypi, following tree-sitters naming standard `tree-sitter-yourlang`.

As a library it provides the functions to install tree-sitter parsers and to load them into python.


## Why is this useful?

Tree-sitter is a great library for parsing source code. It is fast, easy to use and has a lot of great features. 
However, it is written in C and does not provide a typed interface for python. This makes writing tools on top of it a bit cumbersome.

With this library you'll be able to use pythons types for your advantage, leveraging autocompletion for fast coding,
types for correctness, and nice features like matching.
