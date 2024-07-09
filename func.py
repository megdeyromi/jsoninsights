#
# hello-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.  All rights reserved.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import base64
from openai import AzureOpenAI

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
    api_url = "https"
    body = {}  # Initialize body with an empty dictionary
    query = ""
    json_data_encoded = ""
    decoded_text_base64 = ""
    try:
        # Read the incoming JSON data
        body = json.loads(data.getvalue())
        
        # Extract query and json_data from the input JSON
        query = body.get("query", "")
        json_data_encoded = body.get("json_data", "")
        body = json.loads(data.getvalue())
        #encoded_name = body.get("name")
        encoding_type = body.get("encoding_type", "base64")  # Default to 'base64' if not provided

        # Convert the encoded name to plain text
        decoded_text_base64 = convert_to_text(json_data_encoded, encoding_type)
        prompt = f"Provide answers based on the following data and query:\n\nQuery: {query}\n\n{decoded_text_base64}\n\nInsights:"
        client = AzureOpenAI( azure_endpoint="https://jaguksouth6726803320.openai.azure.com/", 
                              api_key="efa992652f52414cb5934735efa47288",
                            api_version="2024-02-15-preview",
                            )
        response = client.completions.create(
            model="gpt-35-turbo",
            prompt=prompt,
            max_tokens=150,  # Adjust based on how detailed you want the insights to be
            temperature=0.8  # Adjust temperature for creativity vs. precision
        )

        # Extract insights from OpenAI response
        insights = response.choices[0].text.strip()
                            

    except (Exception, ValueError) as ex:
        print(str(ex), flush=True)

    # Process the name using the new function
    #name = process_name(name)

    #print("Value of name = ", name, flush=True)
    # Prepare the response data
    response_data = { "insights": insights  }
    print("Exiting Python Hello World handler", flush=True)
    return response.Response(
        ctx, response_data=json.dumps(response_data),
        headers={"Content-Type": "application/json"}
    )
