import simplejson as json


def list_to_str(data):
    return json.dumps(data)


def str_to_list(data):
    dec = json.decoder.JSONDecoder()
    return dec.decode(data)
