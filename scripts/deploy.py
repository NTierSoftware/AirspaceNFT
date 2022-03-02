#!/usr/bin/python3
import logging
from brownie import AirspaceNFT, accounts, network, config

activeNet = network.show_active()

logger = logging.getLogger(__name__)

def deploy():
    myAcct = accounts.add(config["wallets"]["from_key"])

    tx = AirspaceNFT.deploy(
        {"from": myAcct},
        publish_source = config["networks"][activeNet].get("verify", False)
    )

    logger.info(f'{AirspaceNFT[-1] = }')



def main():
    print(f'deploy():\t{activeNet = }')

    deploy()
    logger.info('\n')
