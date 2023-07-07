// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;
import "./certificate.sol";

contract certificateFactory{
    uint totalCertificates;
    uint revorkedCertificates;

    /*
        адрес => владельца хэш сертификата => данные сертификата
        Вопрос: Как второй ключ лучше использовать хэш или имя сертификата(name)?
    */
    mapping(address => mapping(bytes32 => Certificate.CertificateInfo)) certificates;
    mapping(address => bool) revorked;

    function issueCertificate(string memory _name, uint _valididty) public {
        Certificate certificate = new Certificate(_name);
        certificate.issueCertificate(_valididty);
        Certificate.CertificateInfo memory certificateInfo = certificate.getCertificateInfo();
        certificates[msg.sender][certificateInfo.documentHash] = certificateInfo;
        totalCertificates += 1;
    }

    function revokeCertificate(Certificate certificate) public {
        certificate.revokeCertificate();
        revorkedCertificates += 1;
        totalCertificates -= 1;

    }

    function verifyCertificate(Certificate certificate) public returns(Certificate.CertificateInfo memory) {
        bytes32 documentHash = certificate.getCertificateInfo().documentHash;
        if (block.timestamp + 1 < certificates[msg.sender][documentHash].expirationDate) {
            return certificates[msg.sender][documentHash];
        } else {
            certificate.expiredCertificateNotification();
        }
    }
}