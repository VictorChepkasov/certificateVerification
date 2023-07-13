from brownie import certificateFactory, accounts
from scripts.deploy import deployFactory as deploy

def issueCertificate(_from, _name, _validity):
    certificateFactory[-1].issueCertificate(
        _name, _validity, {
            'from': _from,
            'priority_fee': '1 wei'
        }
    )
    print('Certificate issued successfully!')

def revokeCertificate(certificate):
    certificateFactory[-1].revokeCertificate(certificate)
    print('Certificate revorked!')

def verifyCertificate(certificate):
    certificateFactory[-1].verifyCertificate(certificate)
    print('Certificate verified!')

def getCertificateInfo(_hash):
    certificateInfo = certificateFactory[-1].getCertificateInfo(_hash)
    print(f'Cartificate info: {certificateInfo}')