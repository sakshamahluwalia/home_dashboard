import os
import webbrowser
import msal

from gen_helper.config import CONFIG

app_id = CONFIG.app_id
SCOPES = CONFIG.SCOPES
authority_url = CONFIG.authority_url


def generate_token():

    access_token_cache = msal.SerializableTokenCache()

    file_path = os.path.join(CONFIG.dir_to_save_api_token, CONFIG.api_token_access_file)
    if os.path.exists(file_path):
        access_token_cache.deserialize(open(file_path, "r").read())

    client = msal.PublicClientApplication(
        client_id=app_id, authority=authority_url, token_cache=access_token_cache
    )
    accounts = client.get_accounts()
    if accounts:
        token_response = client.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        flow = client.initiate_device_flow(scopes=SCOPES)
        print(flow)
        webbrowser.open(flow["verification_uri"])
        token_response = client.acquire_token_by_device_flow(flow)

    with open(file_path, "w") as f:
        f.write(access_token_cache.serialize())

    return token_response["access_token"]


if __name__ == "__main__":
    # file to store the access token
    os.makedirs(CONFIG.dir_to_save_api_token, exist_ok=True)

    # generate token
    token_response = generate_token()
    print(token_response)
