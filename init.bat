@echo off

py -3 -m venv .venv && .venv\Scripts\activate && pip install pipenv && pipenv install