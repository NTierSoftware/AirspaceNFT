from brownie import AirspaceNFT
from scripts.localUtils import getAccount
import logging


logger = logging.getLogger(__name__)
logger.info('\n')

def burnTokens(tokenId = None) -> int:
    NFTcontract = AirspaceNFT[-1]
    logger.info(f'{NFTcontract = }')

    numTokens = NFTcontract.tokenCounter()
    if numTokens < 1:
        logger.warning(f'No tokens to burn: {numTokens = }')
        return -1

    tokensBurned = 0
    acct = getAccount()

    if tokenId:
        tx = NFTcontract.burn(tokenId, {"from": acct})
    else: # BURN ALL TOKENS!
        for tokenId in range(1, numTokens + 1):
            tx = NFTcontract.burn(tokenId, {"from": acct})
            # logger.info(f'{tokenId}:{tx.return_value}' )
            logger.info(f'burned {tokenId = }' )
            tokensBurned += 1


        tx.wait(2)

            # try:
            #     tx = NFTcontract.burn(tokenId, {"from": acct})
            #     tx.wait(2)
            # except ValueError as err:
            #     logger.warning(f'{tokenId =}:\t{err})' )



    logger.info(f'tokens burned: {tokensBurned}')



def main():
    burnTokens()

