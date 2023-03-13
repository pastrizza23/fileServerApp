#!/bin/bash

pip install -r requirements.txt

pylint src utils auth

pytest tests