#You can obtain your own access tokens by
#curl -d grant_type=password -d email=your@email.com -d password=yourpassword https://auth.nettix.fi/oauth2/token
#More info at https://api.nettix.fi/docs/car/#/


secrets = {
    'myToken': "Put your access token here",
    'refresh_token': "Put your refresh token here",
}

def get(token):
    return  secrets[token]