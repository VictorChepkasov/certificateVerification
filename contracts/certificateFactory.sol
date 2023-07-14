// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;
import "./certificate.sol";

contract certificateFactory{
    uint totalCertificates;
    uint revorkedCertificates;
    /*
        адрес => владельца id сертификата => данные сертификата
        Вопрос: Как второй ключ лучше использовать хэш или id сертификата?
    */
    mapping(uint => Certificate) certificates; 
    mapping(uint => Certificate.CertificateInfo) certificatesInfo;
    mapping(address => bool) revorked;

    function issueCertificate(string memory _name, uint _valididty) public {
        address owner = msg.sender;
        Certificate certificate = new Certificate(owner, _name, totalCertificates+1);
        certificate.issueCertificate(_valididty);
        Certificate.CertificateInfo memory certificateInfo = certificate.getCertificateInfo();
        certificatesInfo[certificateInfo.id] = certificateInfo;
        certificates[totalCertificates+1] = certificate;
        totalCertificates += 1;
    }

    function revokeCertificate(Certificate certificate) public {
        certificate.revokeCertificate();
        revorkedCertificates += 1;
        totalCertificates -= 1;
    }

    function verifyCertificate(Certificate certificate, uint id) public returns(Certificate.CertificateInfo memory) {
        // bytes32 documentHash = certificate.getCertificateInfo().documentHash;
        if (block.timestamp + 1 < certificatesInfo[id].expirationDate) {
            return certificatesInfo[id];
        } else {
            certificate.expiredCertificateNotification();
        }
    }

    function getCertificateInfo(uint id) public view returns(Certificate.CertificateInfo memory) {
        return certificatesInfo[id];
    }

    function getTotalCertificates() public view returns(uint) {
        return totalCertificates;
    }

    function getRevorkedCertificates() public view returns(uint) {
        return revorkedCertificates;
    }

    function getCertificate(uint id) public view returns(Certificate) {
        return certificates[id];
    }
}