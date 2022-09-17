import string
from web3 import Web3
from web3.middleware import geth_poa_middleware
from requests import get
import json

f = open('AuthenticContentAbi.json')

authentic_content_abi = json.load(f)

account_from = {
  'private_key': "4c10e86705877caff5680eb446f7360d2fb72b9f8936d8bab5b17eb45ddbd37c",
  'address': "0x51349f6D250A50AA73b599EcB953f008BEF4FCbC"
}

metadata_sample = {
  'name': 'video.mp4',
  'rootHash': 'some-hash-string'
}

metadataUrl = "https://pastebin.com/raw/ByjtCGnt"

alchemy_url = "https://polygon-mumbai.g.alchemy.com/v2/rXZnrDW_tn8eJKsFn-IXJaOR5TntMTPK"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)


###########################################
def mint_authenticity_token(metadataURL: json):
  authentic_contract = w3.eth.contract(address=Web3.toChecksumAddress('0xcbf1502abc69ba54631a99c4901b652a9e8f4308'), abi=authentic_content_abi)
  nonce = w3.eth.get_transaction_count(account_from['address'])
  
  mint_NFT_txn = authentic_contract.functions.mintNFTForMyself(metadataURL).buildTransaction(
    {
      'from': account_from['address'],
      'nonce': nonce
    }
  )

  tx_create = w3.eth.account.sign_transaction(mint_NFT_txn, account_from['private_key'])
  tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
  tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

  print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')

################################################

# mint_authenticity_token(metadataUrl)

####################################################

def check(content_name: string, hash_to_check: string):
  url = "https://deep-index.moralis.io/api/v2/nft/search?chain=mumbai&format=decimal&q="+content_name+"&filter=name&addresses=0xcbf1502abc69ba54631a99c4901b652a9e8f4308"

  headers = {
    "accept": "application/json",
    "X-API-Key": "rGG3YKpRbl6DzP8y02ryMG3Eu8TeUScxiYONfXpwiLj2RKitIaNRPL9OuVmHeiVb"
  }

  response = get(url, headers=headers)

  json_response = json.loads(response.text)

  if json_response['total'] == 0:
    print("No content with such name!")
    return
  
  if json.loads(json_response['result'][0]['metadata'])['rootHash'] == hash_to_check:
    print("Hash matches!")

  print("No match!")

# check(metadata_sample['name'], metadata_sample['rootHash'])