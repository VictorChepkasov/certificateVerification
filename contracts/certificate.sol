// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Certificate {
    struct CertificateInfo {
        address owner;
        string nameCertificate;
        bytes32 documentHash;
        uint lvlQualification;
        uint dateOfIssue;
        uint expirationDate;
        bool revoked;
        bool verified;
    }

    CertificateInfo public certificate;
    
    constructor(string memory _name) {
        certificate.owner = msg.sender;
        certificate.nameCertificate = _name;
    }

    function issueCertificate(uint validity) external onlyRecipient {
        certificate.documentHash = keccak256(abi.encode(certificate.owner, certificate.nameCertificate));
        certificate.lvlQualification = 1;
        certificate.dateOfIssue = block.timestamp;
        certificate.expirationDate = certificate.dateOfIssue + (86400 * validity);
        certificate.revoked = false;
        certificate.verified = true;
        emit IssueCertificate(msg.sender, certificate.dateOfIssue, certificate.expirationDate, certificate.documentHash);
    }

    function revokeCertificate() external {
        certificate.revoked = true;
        emit RevokeCertificate(msg.sender, block.timestamp, certificate.revoked);
    }

    function expiredCertificateNotification() external {
        require(block.timestamp > certificate.expirationDate, "Certificate has not expired!");
        certificate.verified = false;
        emit ExpiredCertificate(msg.sender, certificate.expirationDate, !certificate.verified);
    }

    function getCertificateInfo() public view returns(CertificateInfo memory) {
        return certificate;
    }

    modifier onlyRecipient() {
        require(msg.sender == certificate.owner, "Only Recipient!");
        _;
    }

    event RevokeCertificate(
        address indexed owner,
        uint dateOfRevorked,
        bool revorked
    );
    event ExpiredCertificate(
        address indexed owner,
        uint dateOfExpiration,
        bool expired
    );
    event IssueCertificate(
        address indexed owner,
        uint dateOfIssue,
        uint expirationDate,
        bytes32 documentHash
    );
}