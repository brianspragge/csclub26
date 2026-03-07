# CS Club 26

## Recommended Reading

- [Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository)
- [Git Cheat Sheet](https://git-scm.com/cheat-sheet)
- [Python Virtual Environments](https://www.w3schools.com/python/python_virtualenv.asp)
- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [Python pip](https://www.w3schools.com/python/python_pip.asp)
- [Pyxel](https://github.com/kitao/pyxel) - A retro game engine for Python
- [Pyxel API Reference](https://kitao.github.io/pyxel/wasm/api-reference/) - Documentation for the Pyxel API

## Options

We have a few options for creating a game with Pyxel.  It works on all platforms, Windows/Mac/Linux, and possibly more.  Use VSCode, Vim, Online, are just a few of the many options.  There are extensions for VSCode that can be used with Pyxel.  It may be best to start a Codebase within github and work directly from there.  Which will you choose?

## Linux Setup for Vim/Nano/Emacs/etc

1. Create your programming directory:
   ```bash
   mkdir Repos; cd Repos
   ```
2. Create a python environment:
   ```bash
   python3 -m venv .env
   ```
3. Activate the new python env:
   ```bash
   source .env/bin/activate
   ```
4. Upgrade the env:
   ```bash
   pip install --upgrade pip
   ```
5. Install Pyxel into that env:
   ```bash
   pip install -U pyxel
   ```
6. Download the github repo for our game code:
   ```bash
   git clone https://github.com/brianspragge/csclub26.git
   ```
7. (Optional) Might need to `git remote add` in order to work on this together.

## Setup for VSCode

0. No idea yet.

## Setup for the Web

1. [None!  Just click here and start](https://kitao.github.io/pyxel/wasm/code-maker/)
