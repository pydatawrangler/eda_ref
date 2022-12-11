# %% [markdown]
# # Chapter 3

# %% [markdown]
# ## Imports

# %%
import requests
import pprint

# %% [markdown]
# ## Exploring an API to find and collect temperature data

# %%
def make_request(endpoint, payload=None):
    """
    Make a request to a specific endpoint on the
    weather API passing headers and optional payload.
    
    Parameters:
        - endpoint: The endpoint of the API you want to
                    make a GET request to.
        - payload:  A dictionary of data to pass along
                    with the request.
    
    returns:
        A response object.
    """
    return requests.get(
        'https://www.ncdc.noaa.gov/cdo-web/'
        f'api/v2/{endpoint}',
        headers={'token': 'jzZnLpQjvZhVYseBfrCwSXgoIXTCyTbE'},
        params=payload
    )

# %%
response = make_request(
    'datasets',
    {'startdate': '2018-10-01'}
)

# %%
response.status_code

# %%
response.ok

# %%
payload=response.json()

# %%
payload.keys()

# %%
payload['metadata']

# %%
payload['results'][0].keys()

# %%
[(data['id'], data['name']) for data in payload['results']]

# %%
response = make_request(
    'datacategories', payload={'datasetid': 'GHCND'}
)

# %%
response.status_code

# %%
response.json()['results']

# %%
response = make_request(
    'datatypes',
    payload={'datacategoryid': 'TEMP', 'limit': 100}
)

# %%
response.status_code

# %%
[(datatype['id'], datatype['name'])
for datatype in response.json()['results']]

# %%
response = make_request(
    'locationcategories', payload={'datasetid': 'GHCND'}
)

# %%
response.status_code

# %%
pprint.pprint(response.json())

# %%
# Stopped at page 132


