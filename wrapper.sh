#!/bin/bash

pip install -r requirements.txt

pylint src utils

pytest tests