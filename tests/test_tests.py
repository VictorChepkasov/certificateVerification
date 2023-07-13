import pytest
from Crypto.Hash import keccak
from brownie import accounts, chain
from scripts.deploy import deployFactory as deploy
from scripts.scripts import issueCertificate, revokeCertificate, verifyCertificate, getCertificateInfo

from web3 import Web3, EthereumTesterProvider
w3 = Web3(EthereumTesterProvider())

@pytest.fixture()
def deployedCertificate():
    acc = accounts[0]
    certificateContract = deploy(acc)
    return acc, certificateContract


def test_issueCertificate(deployedCertificate, _name='First', _validity=0):
    acc, certificateContract = deployedCertificate
    keccak256 = keccak.new(digest_bits=256)
    # documentHash = keccak256.update(bytes(_name, 'utf-8'))
    documentHash = w3.solidityKeccak(['string'], [_name])
    # documentHash = hash(_name)
    print(f'HASH: {documentHash}')
    issueCertificate(acc, _name, _validity)
    certificateInfo = getCertificateInfo(documentHash)
    print(f'Certificate info: {certificateInfo}')

    validInfo = (acc, _name, documentHash, 1, 1, chain.time(), chain.time()+(86400*_validity), False, True)

    assert certificateInfo == validInfo