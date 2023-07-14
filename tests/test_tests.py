import pytest
from brownie import accounts, chain
from scripts.deploy import deployFactory as deploy
from scripts.scripts import issueCertificate, revokeCertificate, verifyCertificate, getCertificateInfo

from web3 import Web3, EthereumTesterProvider
w3 = Web3(EthereumTesterProvider())

@pytest.fixture()
def deployedCertificate(autouse=True):
    acc = accounts[0]
    certificateContract = deploy(acc)
    return acc, certificateContract

def test_issueCertificate(deployedCertificate, _name='First', _validity=0):
    acc, factoryContract = deployedCertificate
    issueCertificate(acc, _name, _validity)
    timestamp = chain.time()+(86400*_validity)
    certificateInfo = getCertificateInfo(1)
    #допустим, что хэш всегда генерируется правильно
    documentHash = certificateInfo[2]
    validInfo = (acc, _name, documentHash, 1, 1, chain.time(), timestamp, False, True)
    assert certificateInfo == validInfo
    print(f'Factory: {factoryContract}')
    assert factoryContract.getTotalCertificates() == certificateInfo[3]

def test_revokeCertificate(deployedCertificate, _name='Second', _validity=0):
    acc, factoryContract = deployedCertificate
    issueCertificate(acc, _name, _validity)
    totalCertificates = factoryContract.getTotalCertificates()
    certificate = factoryContract.getCertificate(1)
    print(f'Certificate: {certificate}')
    revokeCertificate(acc, 1)
    revoked = getCertificateInfo(1)[-2]
    assert factoryContract.getRevorkedCertificates() == 1
    assert factoryContract.getTotalCertificates() == totalCertificates - 1
    # What the fuck?
    assert revoked == True

def test_verifyCertificate(deployedCertificate, _id=1, _name='Third', _validity=0):
    acc, factoryContract = deployedCertificate
    issueCertificate(acc, _name, _validity)

    certificate = factoryContract.getCertificate(_id)
    verifyInfo = verifyCertificate(acc, certificate, _id).return_value
    print(f'Verify info: {verifyInfo}')

    assert verifyInfo == getCertificateInfo(_id)