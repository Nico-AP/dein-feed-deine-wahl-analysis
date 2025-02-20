import json


def save_json_file(path, data):
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def flatten_responses(responses):
    """
    Response dict has initially the following structure:
    {
        'participant_id': _,
        'response_data': {'var_1': _, 'var_2': _, etc.}
    }

    Flattens this structure to:
    {
        'participant_id': _,
        'var_1': _,
        'var_2': _,
        etc.
    }
    """
    flat_responses = []
    for response in responses:
        d = dict()
        for key, value in response.items():
            if key == 'response_data':
                for k, v in value.items():
                    d[k] = v
            else:
                d[key] = value
        flat_responses.append(d.copy())
    return flat_responses
