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

    function revokeCertificate(uint id) public {
        // certificate.revokeCertificate();
        // What the fuck?
        certificatesInfo[id].revoked = true;
        revorkedCertificates += 1;
        totalCertificates -= 1;
    }

    function verifyCertificate(Certificate certificate, uint id) public returns(Certificate.CertificateInfo memory) {
        if (block.timestamp > certificatesInfo[id].expirationDate) {
            certificate.expiredCertificateNotification();
        }
        return certificatesInfo[id];
    }

    function getCertificateInfo(uint id) public view returns(Certificate.CertificateInfo memory) {
        return certificatesInfo[id];
    }

    function getCertificate(uint id) public view returns(Certificate) {
        return certificates[id];
    }

    function getTotalCertificates() public view returns(uint) {
        return totalCertificates;
    }

    function getRevorkedCertificates() public view returns(uint) {
        return revorkedCertificates;
    }
}