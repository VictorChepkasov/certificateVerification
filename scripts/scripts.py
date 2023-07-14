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

def revokeCertificate(_from, _id):
    certificateFactory[-1].revokeCertificate(_id, {
        'from': _from,
        'priority_fee': '1 wei'
    })
    print('Certificate revorked!')

def verifyCertificate(_from, _certificate, _id):
    verifyInfo = certificateFactory[-1].verifyCertificate(_certificate, _id, {
        'from': _from,
        'priority_fee': '1 wei'
    })
    print('Certificate verified!')
    return verifyInfo

def getCertificateInfo(_id):
    certificateInfo = certificateFactory[-1].getCertificateInfo(_id)
    print(f'Cartificate info: {certificateInfo}')
    return certificateInfo