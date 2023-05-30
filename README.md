# py-aws-sam-cdk-app

## pipenv

```sh
# Set pipenv to create the virtual environment in the project directory
export PIPENV_VENV_IN_PROJECT=true

# Create & Activate virtual environment with Python 3.8.7
pipenv shell --python 3.8.7

# Install the requests library as an example
pipenv install requests

# Run a Python script (replace with your actual script)
python myscript.py

# Install all project dependencies from Pipfile
pipenv install # This does NOT install dev dependencies

# Install all dev-dependencies from Pipfile
pipenv install --dev # This installs dev dependencies

# Generate a requirements.txt file for production dependencies
pipenv lock -r > requirements-freeze.txt 

# Generate a requirements.txt file for development dependencies
pipenv lock --dev -r > requirements-freeze-dev.txt

# Exit the virtual environment
exit

# Remove the virtual environment
pipenv --rm
```

## pip

```sh
# Create a virtual environment with Python 3.8.7
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requests library as an example
pip install requests

# Run a Python script (replace with your actual script)
python myscript.py

# Install all project dependencies from requirements.txt
pip install -r requirements.txt

# Install all dev-dependencies from requirements-dev.txt
pip install -r requirements-dev.txt

# Deactivate the virtual environment
deactivate

# Remove the virtual environment
rm -rf .venv
```
