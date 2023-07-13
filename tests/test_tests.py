import pytest
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
    acc, _ = deployedCertificate
    issueCertificate(acc, _name, _validity)
    certificateInfo = getCertificateInfo(1)
    #допустим, что хэш всегда генерируется правильно
    documentHash = certificateInfo[2]
    validInfo = (acc, _name, documentHash, 1, 1, chain.time(), chain.time()+(86400*_validity), False, True)
    assert certificateInfo == validInfo