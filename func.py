#
# hello-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import base64

from fdk import response

def convert_to_text(encoded_str, encoding_type='base64'):
    """
    Convert an encoded string to plain text.
    
    Parameters:
    encoded_str (str): The encoded string.
    encoding_type (str): The type of encoding ('base64', 'utf-8', etc.). Default is 'base64'.
    
    Returns:
    str: The decoded text.
    """
    if encoding_type == 'base64':
        # Decode from Base64
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
    elif encoding_type == 'utf-8':
        # Assume the string is encoded in utf-8
        decoded_str = encoded_str.encode('utf-8').decode('utf-8')
    else:
        raise ValueError("Unsupported encoding type")
    
    return decoded_str

def process_name(name: str) -> str:
    # This function processes the name string and returns the modified string
    return name.upper()

def handler(ctx, data: io.BytesIO=None):
    print("Entering Python Hello World handler", flush=True)
    name = "World"
    try:
        body = json.loads(data.getvalue())
        encoded_name = body.get("name")
        encoding_type = body.get("encoding_type", "base64")  # Default to 'base64' if not provided

        # Convert the encoded name to plain text
        name = convert_to_text(encoded_name, encoding_type)
    except (Exception, ValueError) as ex:
        print(str(ex), flush=True)

    # Process the name using the new function
    name = process_name(name)

    print("Value of name = ", name, flush=True)
    print("Exiting Python Hello World handler", flush=True)
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello {0}".format(name)}),
        headers={"Content-Type": "application/json"}
    )
