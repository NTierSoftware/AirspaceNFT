from brownie import AirspaceNFT, config, accounts
from pathlib import Path
import requests, json, os, logging
# from scripts.localUtils import printFuncSig
from scripts.localUtils import getAccount

imageStagingDir = 'Z:\\workspace3\\NFTPOC1\\imageStaging\\'
imagesDir   = f'{imageStagingDir}images\\' #images to upload to IPFS...
metadataDir = f'{imageStagingDir}JSON\\'   #...and their metadata files

logger = logging.getLogger(__name__)

NFTcontract = AirspaceNFT[-1]

def main():
    # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    _, _, images = next(os.walk(imagesDir), (None, None, []))
    logger.debug(f'{len(images) = }\t{images = }')

    _, _, JSONs = next(os.walk(metadataDir), (None, None, []))
    logger.debug(f'{len(JSONs) = }\t{JSONs = }')

    if len(images) != len(JSONs): logger.warning(f'{len(images) = } != {len(JSONs) = }')

    for img in images:
        JSONfname =  img[0:img.index('.')] +'.json' #strip off the .jpg or .png from img filename and add .json

        if JSONfname in JSONs:
            imgURI = upload_to_ipfs(imagesDir, img)

            with open(metadataDir + JSONfname, "r+") as JSONfile:
                JSON = json.load(JSONfile)
                JSON["image"] = imgURI
                JSONfile.seek(0)
                json.dump(JSON, JSONfile, indent=2) #, sort_keys=True)
                # JSONfile.write( json.dumps(JSON, indent=4, sort_keys=True) )
                JSONfile.truncate()


            tokenURI = upload_to_ipfs(metadataDir, JSONfname)
            createCollectible(tokenURI)

        else: logger.warning(f'no metadata JSON file found for: {img}.  Upload failed for this image!')


    # NFTcontract = AirspaceNFT[-1]
    logger.info(f'{NFTcontract = }')
    number_of_NFTcontracts = NFTcontract.tokenCounter()
    print(f"You have created {number_of_NFTcontracts} collectibles!")

    logger.info('\n')


# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


IPFS = 'http://127.0.0.1:5001'
IPFSadd = f'{IPFS}/api/v0/add'

# @printFuncSig
def upload_to_ipfs(filepath:str, fname:str) -> str:
# http://docs.ipfs.io.ipns.localhost:8080/how-to/address-ipfs-on-web/
#     https://ipfs.io/ipfs/<CID>   e.g.  https://ipfs.io/ipfs/Qme7ss3ARVgxv6rXqVPiikMJ8u2NLgmgszg13pYrDKEoiu
# https://stackoverflow.com/questions/70806644/ipfs-uri-format-https-ipfs-io-ipfs-cid-vs-ipfs-cid
    with Path(filepath + fname).open("rb") as fp:
        imgBinary = fp.read()

    response = requests.post(IPFSadd, files={"file": imgBinary})
    CID = response.json()["Hash"]
    # return f"https://ipfs.io/ipfs/{CID}?filename={fname}"

    # https://stackoverflow.com/questions/70806644/ipfs-uri-format-https-ipfs-io-ipfs-cid-vs-ipfs-cid
    # http://docs.ipfs.io.ipns.localhost:8080/how-to/mint-nfts-with-ipfs/#how-minty-works
    return f"ipfs://{CID}?filename={fname}"


OPENSEA_FORMAT = "https://testnets.opensea.io/assets/"
acct = getAccount()

def createCollectible(tokenURI: str):
    logger.info(f'{tokenURI= }')

    tx = NFTcontract.createCollectible(tokenURI, {"from": acct})
    tx.wait(1)
    tokenId = NFTcontract.tokenCounter()

    logger.info(f'{OPENSEA_FORMAT}{NFTcontract.address}/{tokenId}')

    # print('Please give up to 20 minutes, and hit the "refresh metadata" button')
