# import scripts.constants as const
# import sys, inspect

from brownie import (
    network,
    accounts,
    config,
    interface,
    LinkToken,
    MockV3Aggregator,
    MockOracle,
    VRFCoordinatorMock,
    Contract,
)

from web3 import Web3

from scripts import activeNet as activeNet


NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache", "hardhat", ]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]

contract_to_mock = {
    "link_token": LinkToken,
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "oracle": MockOracle,
}



import functools
def printFuncSig(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'\n{func.__name__}:\n\t{args = }\n\t{kwargs = }')
        return func(*args, **kwargs)
    return wrapper



def getAccount(index=None, id=None):
    if index: return accounts[index]
    if id: return accounts.load(id)
    if activeNet in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if activeNet in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])

    return None


def get_contract(contract_name):
    """If you want to use this function, go to the brownie config and add a new entry for
    the contract that you want to be able to 'get'. Then add an entry in the in the variable 'contract_to_mock'.
    You'll see examples like the 'link_token'.
        This script will then either:
            - Get a address from the config
            - Or deploy a mock to use for a network that doesn't have it

        Args:
            contract_name (string): This is the name that is refered to in the
            brownie config and 'contract_to_mock' variable.

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            Contract of the type specificed by the dictonary. This could be either
            a mock or the 'real' contract on a live network.
    """
    contract_type = contract_to_mock[contract_name]
    if activeNet in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        try:
            contract_address = config["networks"][network.show_active()][contract_name]
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
            )
            print(
                f"brownie run scripts/deploy_mocks.py --network {network.show_active()}"
            )
    return contract


def get_breed(breed_number):
    switch = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}
    return switch[breed_number]



def fund_with_link(
        contract_address,
        account=None,
        link_token=None,
        amount=Web3.toWei(1, "ether")
    ):

    if not account: account = getAccount()
    if not link_token: link_token = get_contract("link_token")

    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Contract Funded: {contract_address}")
    return funding_tx


def get_verify_status():
    verify = (
        config["networks"][network.show_active()]["verify"]
        if config["networks"][network.show_active()].get("verify")
        else False
    )
    return verify


def deploy_mocks(decimals=18, initial_value=2000):
    """ Use this script if you want to deploy mocks to a testnet """

    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = getAccount()
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock VRFCoordinator...")
    mock_vrf_coordinator = VRFCoordinatorMock.deploy(
        link_token.address, {"from": account}
    )
    print(f"Deployed to {mock_vrf_coordinator.address}")

    print("Deploying Mock Oracle...")
    mock_oracle = MockOracle.deploy(link_token.address, {"from": account})
    print(f"Deployed to {mock_oracle.address}")
    print("Mocks Deployed!")
