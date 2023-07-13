import pytest
from brownie import accounts
from scripts.deploy import deployFactory as deploy
from scripts.scripts import issueCertificate, revokeCertificate, verifyCertificate

@pytest.fixture()
def deployedCertificate():
    acc = accounts[0]
    certificateContract = deploy(acc)
    return acc, certificateContract


def test_issueCertificate(deployedCertificate):
    