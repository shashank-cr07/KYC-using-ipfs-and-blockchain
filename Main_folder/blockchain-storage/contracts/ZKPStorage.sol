// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ZKPStorage {
    struct ZKPData {
        string verificationKey;
        string publicData;
        string proof;
    }

    mapping(uint256 => ZKPData) private userBlocks;
    event BlockStored(uint256 indexed userId);

    constructor(string memory _verificationKey, string memory _publicData, string memory _proof) {
        userBlocks[1] = ZKPData(_verificationKey, _publicData, _proof);
        emit BlockStored(1);
    }

    function getBlockData(uint256 userId) public view returns (string memory, string memory, string memory) {
        ZKPData memory data = userBlocks[userId];
        return (data.verificationKey, data.publicData, data.proof);
    }
}
