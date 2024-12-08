
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.3;

//guardar el hash de los datos enviados por el usuario

contract IpfsStorage {
    
    mapping (address => string) public userFiles;


    function setFilesIPFS(string memory file) external {

        userFiles[msg.sender] = file;
    }
}