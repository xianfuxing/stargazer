resp = {}


def get_salt_resp_stdout(data):
    # find stdout key
    for k, v in data.items():
        if type(v) is dict:
            # yield (k, v)
            v = get_salt_resp_stdout(v)
            if v:
                return v
        else:
            if k == 'stdout':
                resp[k] = v
            if k == 'stderr':
                resp[k] = v
            if k == 'result':
                resp[k] = v
    return resp
