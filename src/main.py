from urllib import request
from urllib.parse import quote_plus as urlencode
from os import environ as env
import sys
import socket
import boto3
from botocore.exceptions import ClientError


# TODO: Better exiting and logging
# TODO: Tests for getApiKey
def getSummonerByName(summonerName, region):
    summonerName = urlencode(summonerName)
    if region not in ["na1"]:
        sys.exit(f"Invalid region: {region}")
    if not summonerName:
        sys.exit("Summoner Name is empty!")
    url = f"https://{region}.api.riotgames.com/" \
          f"lol/summoner/v4/summoners/by-name/{summonerName}"
    headers = {
        "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": f"{getApiKey()}"
    }
    req = request.Request(url, headers=headers)
    try:
        response = request.urlopen(req, timeout=2)
    except (request.HTTPError, request.URLError) as error:
        sys.exit(f"Error while accessing Riot API: [{error}]\nURL: [{url}]")
    except socket.timeout:
        sys.exit("API call to riot timed out!")

    return response.read()


def getApiKey():
    apiKey = env.get("RIOT_API_KEY")
    if not apiKey:
        sys.exit("API Key is missing!")
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=apiKey
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            print("The requested secret " + apiKey + " was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            print("The request was invalid due to:", e)
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            print("The request had invalid params:", e)
        elif e.response["Error"]["Code"] == "DecryptionFailure":
            print("The requested secret can't be decrypted"
                  "using the provided KMS key:", e)
        elif e.response["Error"]["Code"] == "InternalServiceError":
            print("An error occurred on service side:", e)
    return get_secret_value_response["SecretString"]


# TODO: Use actual inputs
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": getSummonerByName(event["summonerName"], event["region"])
    }
