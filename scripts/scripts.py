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

def revokeCertificate(_from, certificate):
    certificateFactory[-1].revokeCertificate(certificate, {
        'from': _from,
        'priority_fee': '1 wei'
    })
    print('Certificate revorked!')

def verifyCertificate(certificate):
    certificateFactory[-1].verifyCertificate(certificate)
    print('Certificate verified!')

def getCertificateInfo(_id):
    certificateInfo = certificateFactory[-1].getCertificateInfo(_id)
    print(f'Cartificate info: {certificateInfo}')
    return certificateInfo