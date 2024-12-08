// SPDX-License-Identifier: MIT

pragma solidity ^0.8.20;

import {Priority} from "./Priority.sol";

struct SensitivePatient {
    address _address;
    string name;
    string reason;
}

struct ExtPatient {
    bytes32 hashedId;
    address specialist;
    Priority priority;
}

struct CompletePatient {
    bytes32 hashedId;
    address _address;
    string name;
    address specialist;
    Priority priority;
    string reason;
}