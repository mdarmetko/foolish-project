import json


def get_articles():
  return read_json_from_file('content_api.json')

def get_quotes():
  return read_json_from_file('quotes_api.json')

def read_json_from_file(filename):
  with open(filename, encoding='utf8') as file:
    s = file.read()
  return json.loads(s)
