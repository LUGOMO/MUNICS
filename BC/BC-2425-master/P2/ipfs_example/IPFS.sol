// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileStorage {
    // Mapping from address to file content (string)
    mapping(address => string) public userFiles;
    
    // Array to store addresses of users who have uploaded a file
    address[] public users;
    
    // Function to upload a file (for simplicity, a string as a file)
    function uploadFile(string memory fileContent) public {
        // Ensure the user hasn't uploaded a file already
        require(bytes(userFiles[msg.sender]).length == 0, "File already uploaded.");
        
        // Store the file for the sender
        userFiles[msg.sender] = fileContent;
        
        // Add the sender's address to the users array if not already present
        users.push(msg.sender);
    }

    // Function to show all files for all users
    function showFiles() external view returns (string memory) {
        uint256 userCount = users.length;
        
        // Prepare a dynamic string to store the concatenated files
        string memory allFiles = "";
        
        // Iterate over all users and concatenate their file content
        for (uint256 i = 0; i < userCount; i++) {
            allFiles = string(abi.encodePacked(allFiles, "Address: ", toString(users[i]), " File: ", userFiles[users[i]], "\n"));
        }
        
        return allFiles;
    }

    // Helper function to convert address to string (for concatenation)
    function toString(address _address) private pure returns (string memory) {
        bytes32 value = bytes32(uint256(uint160(_address)));
        bytes memory alphabet = "0123456789abcdef";
        bytes memory str = new bytes(42);
        str[0] = '0';
        str[1] = 'x';
        for (uint256 i = 0; i < 20; i++) {
            str[2 + i * 2] = alphabet[uint8(value[i + 12] >> 4)];
            str[3 + i * 2] = alphabet[uint8(value[i + 12] & 0x0f)];
        }
        return string(str);
    }
}
