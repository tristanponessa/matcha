import json
def dict_to_str(idict):
    return json.dumps(idict)

def str_to_dict(istr):
    return json.loads(istr)

def get_dict_elem(dct, info):
    #hint key
    x = len(info)

    
    for hint_k,v in info.items():
        

    
