// SPDX-License-Identifier: Unlicenced
pragma solidity ^0.8.18;

contract TokenContract {
    address payable public owner;
    uint256 public constant tokenPrice = 5 ether;
    uint256 private contractBalance = 0 ether;

    struct Receivers {
        string name;
        uint256 tokens;
    }
    mapping(address => Receivers) public users;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor() {
        owner = payable(msg.sender);
        users[owner].tokens = 100;
    }

    function double(uint256 _value) public pure returns (uint256) {
        return _value * 2;
    }

    function register(string memory _name) public {
        users[msg.sender].name = _name;
    }

    function giveToken(address _receiver, uint256 _amount) public onlyOwner {
        require(users[owner].tokens >= _amount);
        users[owner].tokens -= _amount;
        users[_receiver].tokens += _amount;
    }
    
    
    function buyTokens(uint256 _amount) public payable {
        uint256 totalCost = _amount * tokenPrice;

        require(msg.sender.balance >= totalCost, "Not enough balance to buy tokens");
        require(users[owner].tokens >= _amount, "Not enough tokens");

        (bool success,) = owner.call{value: msg.value}("Buying tokens");
        require(success, "Payment failed");

        users[owner].tokens -= _amount;
        users[msg.sender].tokens += _amount;

        contractBalance += msg.sender.balance;
    }

    function getContractBalance() public view returns (uint256) {
        return contractBalance;
    }
}
