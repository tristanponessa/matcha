import json

def dict_to_str(idict):
    return json.dumps(idict)

def str_to_dict(istr):
    return json.loads(istr)

def dict_val_similar_key(dct, key):
    for k,v in dct.items():
        if key in k:
            return v

def is_sub_dict(dct, sub_dct):
    match = 0
    for k,v in sub_dct.items():
        if dict_val_similar_key(dct, k) == v:
            match += 1
    if len(sub_dct) == match:
        return True



    
