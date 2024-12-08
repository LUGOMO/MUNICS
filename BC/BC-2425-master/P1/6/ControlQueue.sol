// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {AccessControl} from "./roles/AccessControl.sol";
import {QueueList, Patient} from "./QueueList.sol";
import {Specialist} from "./models/Specialist.sol";

contract ControlQueue is AccessControl, QueueList {
    // Creates role identifiers
    bytes32 public constant OWNER_ENTITY = keccak256("OWNER_ENTITY_ROLE");
    bytes32 public constant SPECIALIST_ROLE = keccak256("SPECIALIST_ROLE");
    bytes32 public constant PATIENT_ROLE = keccak256("PATIENT_ROLE");
    bytes32 public constant EXTERNAL_ROLE = keccak256("EXTERNAL_ROLE");

    string private _name;

    // Auxiliary structures
    mapping (address patient => address specialist) private patientToSpecialist;
    mapping (address patient => uint) private specialistPatients;

    // Come up with a better way of storing specialists
    Specialist[] private specialists;

    // List array
    // Change history (timestamp, patient, motive, from position, to position...)

    constructor(string memory name) {
        // Define los roles del contrato
        _grantRole(OWNER_ENTITY, msg.sender);
        _setRoleAdmin(OWNER_ENTITY, OWNER_ENTITY);
        _setRoleAdmin(SPECIALIST_ROLE, OWNER_ENTITY);
        // !!! Implementar que el OWNER_ENTITY también pueda modificar el paciente
        _setRoleAdmin(PATIENT_ROLE, SPECIALIST_ROLE);
        _name = name;
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // OWNER_ENTITY_FUNCTIONS

    function addSpecialist(address _specialist, string memory name) onlyRole(OWNER_ENTITY) public {
        if (hasRole(SPECIALIST_ROLE, _specialist)) {
            revert("Patient already exists");
        }
        _grantRole(SPECIALIST_ROLE, _specialist);
        specialists.push(Specialist(_specialist, name));
    }

    function removeSpecialist(address _specialist) onlyRole(OWNER_ENTITY) public {
        if (!hasRole(SPECIALIST_ROLE, _specialist)) {
            revert("Specialist does not exist");
        }
        // check if it has patients
        if (specialistPatients[_specialist] > 0) {
            revert("Cannot delete a specialist who still has patients");
        }
        _revokeRole(SPECIALIST_ROLE, _specialist);

        // Remove specialist from list
        uint current_index;

        for (uint i = 0; i < specialists.length; i++) {
            if (_specialist == specialists[i]._address) {
                current_index = i;
                break;
            }
        }

        for (uint i = current_index; i < specialists.length - 1; i++) {
            specialists[i] = specialists[i+1];
        }
        specialists.pop();
    }

    function movePatientInQueue(address _patient, uint newPos, string memory reason) public onlyRole(OWNER_ENTITY) {
        move(_patient, newPos, reason);
    }

    function transferAllPatientsFromSpecialist(address _oldSpecialist, address _newSpecialist, string memory reason) public onlyRole(OWNER_ENTITY) {
        require(specialistPatients[_oldSpecialist] > 0, "No hay pacientes para transferir ");

        Patient[] memory _specialistPatients = getPatientsFromSpecialist(_oldSpecialist);

        for (uint i = 0; i < _specialistPatients.length; i++) {
            transferPatient(_specialistPatients[i]._address, _newSpecialist, reason);
        }
    }


    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // SPECIALIST FUNCTIONS

    // Add patient in certain position of the queue
    function addPatient(address _patient, string memory name, uint pos, string memory reason) onlyRole(SPECIALIST_ROLE) public onlyRole(SPECIALIST_ROLE) {
        if (hasRole(PATIENT_ROLE, _patient)) {
            revert("Patient already exists");
        }
        if (!patientBelongsToSpecialist(_patient, msg.sender)) {
            revert("Patient doesn't belong to Specialist");
        }
        Patient memory patient = Patient(_patient, msg.sender, name);

        _grantRole(PATIENT_ROLE, _patient);
        patientToSpecialist[_patient] = msg.sender;
        specialistPatients[msg.sender]++;

        // Add to queue
        if (pos == getQueueLength()) {
            add(patient, reason);
        } else {
            add(patient, pos, reason);
        }

        emit PatientCreated(_patient, msg.sender);
    }

    // Add patient to the end of the queue
    function addPatient(address _patient, string memory name, string memory reason) onlyRole(SPECIALIST_ROLE) public onlyRole(SPECIALIST_ROLE) {
        addPatient(_patient, name, getQueueLength(), reason);
    }

    function transferPatient(address _patient, address _newSpecialist, string memory reason) public onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY) {
        address oldSpecialist = patientToSpecialist[_patient];

        if (!hasRole(OWNER_ENTITY, msg.sender)) {
            require(oldSpecialist == msg.sender, "El paciente no pertenece a este especialista");
        }

        specialistPatients[oldSpecialist]--;
        patientToSpecialist[_patient] = _newSpecialist;
        specialistPatients[_newSpecialist]++;

        update(_patient, oldSpecialist, _newSpecialist, reason);
    }

    function transferAllPatients(address _newSpecialist, string memory reason) public onlyRole(SPECIALIST_ROLE) {
        require(specialistPatients[msg.sender] > 0, "No hay pacientes para transferir ");

        Patient[] memory _specialistPatients = getPatientsFromSpecialist(msg.sender);

        for (uint i = 0; i < _specialistPatients.length; i++) {
            transferPatient(_specialistPatients[i]._address, _newSpecialist, reason);
        }
    }

    function removePatient(address _patient, string memory reason) public onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY) {
        if (!hasRole(OWNER_ENTITY, msg.sender)) {
            if (!hasRole(PATIENT_ROLE, _patient)) {
                revert("Patient doesn't exist");
            }
            if (!patientBelongsToSpecialist(_patient, msg.sender)) {
                revert("Patient doesn't belong to Specialist");
            }
        }

        address specialist = patientToSpecialist[_patient];

        if (specialistPatients[specialist] == 0) {
            revert("Specialist does not have any patients");
        }

        _revokeRole(PATIENT_ROLE, _patient);
        specialistPatients[specialist]--;
        delete patientToSpecialist[_patient];
        remove(_patient, reason);
        emit PatientRemoved(_patient);
    }

    function getPositionInQueue(address _patient) public view onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY) returns (Patient memory patient, uint position) {
        return searchPatient(_patient);
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // PATIENT_ROLE FUNCTIONS

    function getPositionInQueue() onlyRole(PATIENT_ROLE) public view returns (Patient memory patient, uint position) {
        return searchPatient(msg.sender);
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // PUBLIC EXTERNAL_ROLE FUNCTIONS

    function getQueueType() public view returns(string memory) {
        return _name;
    }

    function patientBelongsToSpecialist(address _patient, address _specialist) public view returns(bool) {
        return ((patientToSpecialist[_patient] == _specialist) || (patientToSpecialist[_patient] == address(0)));
    }

    function getSpecialists() public view returns(Specialist[] memory) {
        return specialists;
    }

    function getPatientsFromSpecialist(address _specialist) public view returns(Patient[] memory) {
        uint counter = 0;
        uint queueLength = getQueueLength();
        Patient[] memory queue = getPatientsQueue();
        Patient[] memory result = new Patient[](specialistPatients[_specialist]);

        for (uint i = 0; i < queueLength; i++) {
            if (queue[i].specialist == _specialist) {
                result[counter++] = queue[i];
            }
        }

        return result;
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // Events (not used yet, may be changed in the future)
    event PatientCreated(address patient, address specialist);
    event PatientRemoved(address patient);
}