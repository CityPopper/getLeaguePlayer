from urllib import request
from urllib.parse import quote_plus as urlencode
from os import environ as env
import sys
import socket


# TODO: Better exiting and logging
def getSummonerByName(summonerName, region):
    summonerName = urlencode(summonerName)
    apiKey = env.get("RIOT_API_KEY")

    if region not in ["na1"]:
        sys.exit(f"Invalid region: {region}")
    if not apiKey:
        sys.exit("API Key is missing!")
    if not summonerName:
        sys.exit("Summoner Name is empty!")

    url = f"https://{region}.api.riotgames.com/" \
          f"lol/summoner/v4/summoners/by-name/{summonerName}"

    headers = {
        "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": f"{apiKey}"
    }

    req = request.Request(url, headers=headers)
    try:
        response = request.urlopen(req, timeout=2)
    except (request.HTTPError, request.URLError) as error:
        sys.exit(f"Error while accessing Riot API: [{error}]\nURL: [{url}]")
    except socket.timeout:
        sys.exit("API call to riot timed out!")

    return response.read()


# TODO: Use actual inputs
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": getSummonerByName("Beast Machine", "na")
    }
