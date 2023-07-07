// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;
import "./certificate.sol";

contract certificateFactory{
    uint totalCertificates;
    uint revorkedCertificates;

    mapping(address => Certificates.Certificate) certificates;
    mapping(address => bool) revorked;

    function addCertificate(string memory _name, uint _valididty) public {
        Certificates certificate = new Certificates(_name);
        certificate.issueCertificate(_valididty);
        certificates[msg.sender] = certificate.getCertificateInfo();
        totalCertificates += 1;
    }

    function deleteCertificate(Certificates certificate) public {
        certificate.revokeCertificate();
        revorkedCertificates += 1;
        totalCertificates -= 1;

    }

    function verifyCertificate(Certificates certificate) public returns(Certificates.Certificate memory) {
        if (block.timestamp + 1 < certificates[msg.sender].expirationDate) {
            return certificates[msg.sender];
        } else {
            certificate.expiredCertificateNotification();
        }
    }
}