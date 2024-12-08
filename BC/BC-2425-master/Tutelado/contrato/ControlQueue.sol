// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {AccessControl} from "./roles/AccessControl.sol";
import {QueueList, SensitivePatient, ExtPatient, CompletePatient, ActionType, MovementChange, AddRemoveChange, UpdateSpecialistChange, MovedPriority} from "./QueueList.sol";
import {Specialist} from "./models/Specialist.sol";
import {Priority} from "./models/Priority.sol";

contract ControlQueue is AccessControl {
    // Role Identifiers
    bytes32 public constant OWNER_ENTITY_ROLE = keccak256("OWNER_ENTITY_ROLE");
    bytes32 public constant SPECIALIST_ROLE = keccak256("SPECIALIST_ROLE");
    bytes32 public constant PATIENT_ROLE = keccak256("PATIENT_ROLE");

    address private OWNER_ENTITY;
    string private _name;

    QueueList private priorityQueue;
    mapping(address => uint24) private specialistPatients;
    Specialist[] private specialists;

    string private conveniosIPFSHash;

    constructor(string memory name) {
        OWNER_ENTITY = msg.sender;
        _grantRole(OWNER_ENTITY_ROLE, msg.sender);

        _setRoleAdmin(OWNER_ENTITY_ROLE, OWNER_ENTITY_ROLE);
        _setRoleAdmin(SPECIALIST_ROLE, OWNER_ENTITY_ROLE);
        _setRoleAdmin(PATIENT_ROLE, SPECIALIST_ROLE);

        _name = name;
        priorityQueue = new QueueList();
    }

    // Role Utilities
    function getRole() public view returns (int8 rolecode) {
        int8 roleBits = int8(1); // Default PUBLIC_ROLE
        if (hasRole(OWNER_ENTITY_ROLE, msg.sender)) roleBits |= int8(1 << 3);
        if (hasRole(SPECIALIST_ROLE, msg.sender)) roleBits |= int8(1 << 2);
        if (hasRole(PATIENT_ROLE, msg.sender)) roleBits |= int8(1 << 1);
        return roleBits;
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // OWNER_ENTITY_ROLE Functions
    function addSpecialist(address _specialist, string memory name) public onlyRole(OWNER_ENTITY_ROLE) {
        if (hasRole(SPECIALIST_ROLE, _specialist)) revert("Specialist already exists");
        _grantRole(SPECIALIST_ROLE, _specialist);
        specialists.push(Specialist(_specialist, name));
    }

    function removeSpecialist(address _specialist) public onlyRole(OWNER_ENTITY_ROLE) {
        if (!hasRole(SPECIALIST_ROLE, _specialist)) revert("Specialist does not exist");
        if (specialistPatients[_specialist] > 0) revert("Cannot delete a specialist with patients");

        _revokeRole(SPECIALIST_ROLE, _specialist);
        _removeSpecialistFromList(_specialist);
    }

    function changePriority(address _patient, Priority newPriority, string memory reason) public onlyRole(OWNER_ENTITY_ROLE) {
        priorityQueue.changePriority(_patient, newPriority, reason);
    }

    function movePatientInQueue(address _patient, uint newPos, string memory reason) public onlyRole(OWNER_ENTITY_ROLE) {
        priorityQueue.move(_patient, newPos, reason);
    }

    function attendPatient(address _patient, string memory reason) public onlyRole(OWNER_ENTITY_ROLE) {
        priorityQueue.attend(_patient, reason);
    }

    function attendPatientAtPosition(Priority priority, uint index, string memory reason) public onlyRole(OWNER_ENTITY_ROLE) {
        priorityQueue.attend(priority, index, reason);
    }

    function derivePatient(address _patient, string memory reason) public onlyRole(OWNER_ENTITY_ROLE) {
        priorityQueue.derive(_patient, reason);
    }

    function transferAllPatientsFromSpecialist(address _oldSpecialist, address _newSpecialist, string memory reason) public onlyRole(OWNER_ENTITY_ROLE) {
        require(specialistPatients[_oldSpecialist] > 0, "No patients to transfer");
        CompletePatient[] memory _patients = _getPatientsFromSpecialist(_oldSpecialist);

        for (uint i = 0; i < _patients.length; i++) {
            transferPatient(_patients[i]._address, _newSpecialist, reason);
        }
    }

    function setConveniosIPFSHash(string memory _ipfsHash) public onlyRole(OWNER_ENTITY_ROLE) {
        conveniosIPFSHash = _ipfsHash;
    }

    function getConveniosIPFSHash() public view returns (string memory) {
        return conveniosIPFSHash;
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // SPECIALIST_ROLE Functions
    function addPatient(address _patient, string memory name, Priority priority, string memory reason) public onlyRole(SPECIALIST_ROLE) returns (CompletePatient memory, uint) {
        if (hasRole(PATIENT_ROLE, _patient)) revert("Patient already exists");
        _grantRole(PATIENT_ROLE, _patient);

        specialistPatients[msg.sender]++;
        (ExtPatient memory extPatient, uint pos) = priorityQueue.add(_patient, msg.sender, name, priority, reason);
        return (CompletePatient(extPatient.hashedId, _patient, name, msg.sender, priority, reason), pos);
    }

    function transferPatient(address _patient, address _newSpecialist, string memory reason) public onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY_ROLE) {
        CompletePatient memory patient = priorityQueue.searchPatient(_patient);
        if (!hasRole(OWNER_ENTITY_ROLE, msg.sender)) {
            require(patient.specialist == msg.sender, "Patient doesn't belong to this specialist");
        }

        specialistPatients[patient.specialist]--;
        specialistPatients[_newSpecialist]++;

        priorityQueue.update(
            priorityQueue.anonymizePatient(SensitivePatient({ _address: patient._address, name: patient.name, reason: patient.reason }), _newSpecialist, patient.priority),
            patient.specialist,
            _newSpecialist,
            reason
        );
    }

    function transferAllPatients(address _newSpecialist, string memory reason) public onlyRole(SPECIALIST_ROLE) {
        require(specialistPatients[msg.sender] > 0, "No patients to transfer");
        CompletePatient[] memory _patients = _getPatientsFromSpecialist(msg.sender);

        for (uint i = 0; i < _patients.length; i++) {
            transferPatient(_patients[i]._address, _newSpecialist, reason);
        }
    }

    function removePatient(address _patient, string memory reason) public onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY_ROLE) {
        if (!hasRole(OWNER_ENTITY_ROLE, msg.sender)) {
            if (!hasRole(PATIENT_ROLE, _patient)) revert("Patient doesn't exist");
            if (!patientBelongsToSpecialist(_patient, msg.sender)) revert("Patient doesn't belong to specialist");
        }

        CompletePatient memory patient = priorityQueue.searchPatient(_patient);
        if (specialistPatients[patient.specialist] == 0) revert("Specialist has no patients");

        _revokeRole(PATIENT_ROLE, _patient);
        specialistPatients[patient.specialist]--;
        priorityQueue.remove(_patient, reason);
    }

    function getPositionInQueue(address _patient) public view onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY_ROLE) returns (ExtPatient memory, uint) {
        return priorityQueue.searchPatientIndex(_patient);
    }

    function getCompletePatientData(bytes32[] memory patientHashId) public view onlyRoles(OWNER_ENTITY_ROLE, SPECIALIST_ROLE) returns (CompletePatient[] memory) {
        uint totalPatients = patientHashId.length; 
        CompletePatient[] memory patients = new CompletePatient[](totalPatients);

        for (uint i = 0; i < totalPatients; i++) {
            CompletePatient memory patient = priorityQueue.searchPatient(priorityQueue.retrieveAddress(patientHashId[i])._address);
            patients[i] = patient;
        }

        return patients;
    }

    function getPatientHashId(address patientAddress) public view onlyRoles(OWNER_ENTITY_ROLE, SPECIALIST_ROLE) returns (bytes32) {
        return priorityQueue.calculateHashedId(patientAddress);
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // PATIENT_ROLE Functions
    function getPositionInQueue() public view onlyRole(PATIENT_ROLE) returns (CompletePatient memory, uint) {
        (ExtPatient memory patient, uint index) = priorityQueue.searchPatientIndex(msg.sender);
        return (priorityQueue.deanonimizePatient(patient), index);
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // External Public Functions
    function getQueueType() public view returns (string memory) {
        return _name;
    }

    function patientBelongsToSpecialist(address _patient, address _specialist) public view returns (bool) {
        return priorityQueue.searchPatient(_patient).specialist == _specialist;
    }

    function getSpecialists() public view returns (Specialist[] memory) {
        return specialists;
    }

    function getOwnerEntityAddress() public view returns (address) {
        return OWNER_ENTITY;
    }

    function getMovementHistory() public view returns (MovementChange[] memory) {
        return priorityQueue.getMovementHistory();
    }

    function getAddRemoveHistory() public view returns (AddRemoveChange[] memory) {
        return priorityQueue.getAddRemoveHistory();
    }

    function getUpdateHistory() public view returns (UpdateSpecialistChange[] memory) {
        return priorityQueue.getUpdateHistory();
    }

    function getMovedPriorityHistory() public view returns (MovedPriority[] memory) {
        return priorityQueue.getMovedPriorityHistory();
    }

    function getQueue(Priority priority) public view returns (ExtPatient[] memory) {
        return priorityQueue.getQueue(priority);
    }

    function getQueueLength(Priority priority) public view returns (uint) {
        return priorityQueue.getQueueLength(priority);
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // Internal Helpers
    function _removeSpecialistFromList(address _specialist) internal {
        for (uint i = 0; i < specialists.length; i++) {
            if (specialists[i]._address == _specialist) {
                specialists[i] = specialists[specialists.length - 1];
                specialists.pop();
                return;
            }
        }
    }

    function _getPatientsFromSpecialist(address _specialist) internal view returns (CompletePatient[] memory) {
        uint24 patientsCount = specialistPatients[_specialist];
        CompletePatient[] memory patients = new CompletePatient[](patientsCount);
        uint index = 0;

        // Iterate over priorities numerically
        for (uint priorityValue = uint(Priority.Priority1); priorityValue <= uint(Priority.Priority3); priorityValue++) {
            Priority priority = Priority(priorityValue); // Cast the numeric value back to Priority enum
            ExtPatient[] memory queue = priorityQueue.getQueue(priority);

            for (uint i = 0; i < queue.length; i++) {
                if (queue[i].specialist == _specialist) {
                    patients[index++] = priorityQueue.deanonimizePatient(queue[i]);
                    if (index == patientsCount) return patients; // Return early if all patients are collected
                }
            }
        }
        return patients;
    }

    function getPatientsFromSpecialist(address _specialist) public view returns (ExtPatient[] memory) {
        uint24 patientsCount = specialistPatients[_specialist];
        ExtPatient[] memory patients = new ExtPatient[](patientsCount);
        uint index = 0;

        // Iterate over priorities numerically
        for (uint priorityValue = uint(Priority.Priority1); priorityValue <= uint(Priority.Priority3); priorityValue++) {
            Priority priority = Priority(priorityValue); // Cast the numeric value back to Priority enum
            ExtPatient[] memory queue = priorityQueue.getQueue(priority);

            for (uint i = 0; i < queue.length; i++) {
                if (queue[i].specialist == _specialist) {
                    patients[index++] = queue[i];
                    if (index == patientsCount) return patients; // Return early if all patients are collected
                }
            }
        }
        return patients;
    }
}
