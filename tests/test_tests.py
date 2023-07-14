import pytest
from brownie import accounts, chain
from web3 import Web3, EthereumTesterProvider
from scripts.deploy import deployFactory as deploy
from scripts.scripts import issueCertificate, revokeCertificate, verifyCertificate, getCertificateInfo

w3 = Web3(EthereumTesterProvider())
pytestmark = pytest.mark.parametrize('_validity', [0, 1, 2])

@pytest.fixture()
def deployedCertificate(autouse=True):
    acc = accounts[0]
    certificateContract = deploy(acc)
    return acc, certificateContract

def test_issueCertificate(deployedCertificate, _validity, _name='First'):
    acc, factoryContract = deployedCertificate
    issueCertificate(acc, _name, _validity)
    timestamp = chain.time()
    certificateInfo = getCertificateInfo(1)
    #допустим, что хэш всегда генерируется правильно
    documentHash = certificateInfo[2]
    validInfo = (acc, _name, documentHash, 1, 1, timestamp, timestamp+(86400*_validity), False, True)
    assert certificateInfo == validInfo
    assert factoryContract.totalCertificates() == certificateInfo[3]

def test_revokeCertificate(deployedCertificate, _validity, _name='Second'):
    acc, factoryContract = deployedCertificate
    issueCertificate(acc, _name, _validity)
    totalCertificates = factoryContract.totalCertificates()
    revokeCertificate(acc, 1)
    revoked = getCertificateInfo(1)[-2]
    assert factoryContract.revorkedCertificates() == 1
    assert factoryContract.totalCertificates() == totalCertificates - 1
    # What the fuck?
    assert revoked == True

def test_verifyCertificate(deployedCertificate, _validity, _id=1, _name='Third',):
    acc, factoryContract = deployedCertificate
    issueCertificate(acc, _name, _validity)
    certificate = factoryContract.getCertificate(_id)
    verifyInfo = verifyCertificate(acc, certificate, _id).return_value
    assert verifyInfo == getCertificateInfo(_id)