// SPDX-License-Identifier: Unlicensed
pragma solidity ^0.8.18;

contract TokenContract {

    address public owner;
    uint256 public tokenPrice = 5 ether; // 1 token = 5 Ether
 
    struct Receivers 
    {
        string name;
        uint256 tokens;
    }
    mapping(address => Receivers) public users;

      modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor()
    {
    owner = msg.sender;
    users[owner].tokens = 100;
    }

    function double(uint _value) public pure returns (uint)
    {
    return _value*2;
    }

    function register(string memory _name) public
    {
    users[msg.sender].name = _name;
    }

    function giveToken(address _receiver, uint256 _amount) onlyOwner public
    {
    require(users[owner].tokens >= _amount);
    users[owner].tokens -= _amount;
    users[_receiver].tokens += _amount;
    }
    //Comprar Tokens con Ether
    function buyToken(uint256 _amount) public payable 
    {
        uint256 totalPrice = _amount * tokenPrice;
        require(msg.value >= totalPrice, "No envio suficiente Ether");
        require(users[owner].tokens >= _amount, "No tienes suficientes Tokens");

        users[owner].tokens -= _amount;
        users[msg.sender].tokens += _amount;

        if(msg.value > totalPrice) 
        {
            payable(msg.sender).transfer(msg.value - totalPrice);

        }
    }
    function getContractBalance() public view 
    returns(uint256)
    {
        return address(this).balance;
          } 
}