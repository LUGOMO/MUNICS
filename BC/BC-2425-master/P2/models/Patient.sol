// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

import {Priority} from "./Priority.sol";

struct Patient {
    address _address;
    address specialist;
    string name;
    Priority priority;
}