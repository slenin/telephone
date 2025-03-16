
## Create new python environment
python3 -m venv env

## Activate the environment
source env/bin/activate

## Select python interpreter in VS Code
Ctrl + Shift + P and select interpreter to be env/bin/python

## Install depedencies
pip install -r requirement.txt

## Create a .env file in the folder with the following content
OPENAI_API_KEY=<key here>
HYPEBOLIC_API_KEY=<key here>

## Run the code
Run from VS Code