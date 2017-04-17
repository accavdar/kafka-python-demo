# kafka-python-demo

This is a demo repo for using `kafka-python` client library. It creates a random topic and sends
 a bunch of messages to the cluster. You can set the `kafka` and `request` config params using `prod
 .conf` file.  

## Setup

- Clone repo 
- Create a new virtual environment with a name (i.e `kafka-python-env`. I'm using python `3.4.4` 
version)

```shell
pyenv virtualenv 3.4.4 kafka-python-env
```
- Install dependencies:
```shell
pyenv activate kafka-pyhton-env
pip install -r requirements/prod.txt
```

## Run
- Run `run_test.py` directly (it sends 1000 messages as default) or with `num_messages` param
```shell
python run_test.py
python run_test.py 10000 # send 10000 messages, default is 1000
```
