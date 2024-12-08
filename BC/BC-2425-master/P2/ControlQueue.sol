// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {AccessControl} from "./roles/AccessControl.sol";
import {QueueList, Patient, ActionType, MovementChange, AddRemoveChange, UpdateSpecialistChange, MovedPriority} from "./QueueList.sol";
import {Specialist} from "./models/Specialist.sol";
import {Priority} from "./models/Priority.sol";

contract ControlQueue is AccessControl {
    // Crea identificadores de roles
    bytes32 public constant OWNER_ENTITY_ROLE = keccak256("OWNER_ENTITY_ROLE");
    bytes32 public constant SPECIALIST_ROLE = keccak256("SPECIALIST_ROLE");
    bytes32 public constant PATIENT_ROLE = keccak256("PATIENT_ROLE");
    bytes32 public constant PUBLIC_ROLE = keccak256("PUBLIC_ROLE");
    address private OWNER_ENTITY;

    QueueList priorityQueue = new QueueList();

    string private _name;

    // Estructuras auxiliares
    mapping (address specialist => uint24) private specialistPatients;

    Specialist[] private specialists;

    // Hash de IPFS para los convenios
    string private conveniosIPFSHash;

    constructor(string memory name) {
        // Define los roles del contrato
        OWNER_ENTITY = msg.sender;
        _grantRole(OWNER_ENTITY_ROLE, msg.sender);
        _setRoleAdmin(OWNER_ENTITY_ROLE, OWNER_ENTITY_ROLE);
        _setRoleAdmin(SPECIALIST_ROLE, OWNER_ENTITY_ROLE);
        _setRoleAdmin(PATIENT_ROLE, SPECIALIST_ROLE);
        _name = name;
    }

    function getRole() public view returns (int8 rolecode) {
        int8 roleBits = int8(1);
        if (hasRole(OWNER_ENTITY_ROLE, msg.sender)) roleBits = roleBits | int8(1 << 3);
        if (hasRole(SPECIALIST_ROLE, msg.sender)) roleBits = roleBits | int8(1 << 2);
        if (hasRole(PATIENT_ROLE, msg.sender)) roleBits = roleBits | int8(1 << 1);
        return roleBits;
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // FUNCIONES DEL ROL OWNER_ENTITY_ROLE

    function addSpecialist(address _specialist, string memory name) public onlyRole(OWNER_ENTITY_ROLE) {
        if (hasRole(SPECIALIST_ROLE, _specialist)) {
            revert("Specialist already exists");
        }
        _grantRole(SPECIALIST_ROLE, _specialist);
        specialists.push(Specialist(_specialist, name));
    }

    function removeSpecialist(address _specialist) public onlyRole(OWNER_ENTITY_ROLE) {
        if (!hasRole(SPECIALIST_ROLE, _specialist)) {
            revert("Specialist does not exist");
        }
        // Verifica si tiene pacientes
        if (specialistPatients[_specialist] > 0) {
            revert("Cannot delete a specialist who still has patients");
        }
        _revokeRole(SPECIALIST_ROLE, _specialist);

        // Elimina el especialista de la lista
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

    function changePriority(address _patient, Priority priority, Priority newPriority, string memory reason) public onlyRole(OWNER_ENTITY_ROLE) {
        priorityQueue.changePriority(_patient, priority, newPriority, reason);
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
        require(specialistPatients[_oldSpecialist] > 0, "No patient to transfer");

        Patient[] memory _specialistPatients = getPatientsFromSpecialist(_oldSpecialist);

        for (uint i = 0; i < _specialistPatients.length; i++) {
            transferPatient(_specialistPatients[i]._address, _newSpecialist, reason);
        }
    }

    // Nuevas funciones para los convenios en IPFS
    
    function setConveniosIPFSHash(string memory _ipfsHash) public onlyRole(OWNER_ENTITY_ROLE) {
        conveniosIPFSHash = _ipfsHash;
    }

    function getConveniosIPFSHash() public view returns (string memory) {
        return conveniosIPFSHash;
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // FUNCIONES DEL ROL SPECIALIST

    // Agrega un paciente al final de la cola
    function addPatient(address _patient, string memory name, Priority priority, string memory reason) public onlyRole(SPECIALIST_ROLE) {
        if (hasRole(PATIENT_ROLE, _patient)) {
            revert("Patient already exists");
        }
        _grantRole(PATIENT_ROLE, _patient);
        specialistPatients[msg.sender]++;

        // Añade al paciente a la cola
        priorityQueue.add(_patient, msg.sender, name, priority, reason);
    }

    function transferPatient(address _patient, address _newSpecialist, string memory reason) public onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY_ROLE) {
        Patient memory patient = priorityQueue.searchPatient(_patient);

        if (!hasRole(OWNER_ENTITY_ROLE, msg.sender)) {
            require(patient.specialist == msg.sender, "El paciente no pertenece a este especialista");
        }

        specialistPatients[patient.specialist]--;
        specialistPatients[_newSpecialist]++;

        priorityQueue.update(_patient, patient.specialist, _newSpecialist, reason);
    }

    function transferAllPatients(address _newSpecialist, string memory reason) public onlyRole(SPECIALIST_ROLE) {
        require(specialistPatients[msg.sender] > 0, "No hay pacientes para transferir ");

        Patient[] memory _specialistPatients = getPatientsFromSpecialist(msg.sender);

        for (uint i = 0; i < _specialistPatients.length; i++) {
            transferPatient(_specialistPatients[i]._address, _newSpecialist, reason);
        }
    }

    function removePatient(address _patient, string memory reason) public onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY_ROLE) {
        if (!hasRole(OWNER_ENTITY_ROLE, msg.sender)) {
            if (!hasRole(PATIENT_ROLE, _patient)) {
                revert("Patient doesn't exist");
            }
            if (!patientBelongsToSpecialist(_patient, msg.sender)) {
                revert("Patient doesn't belong to Specialist");
            }
        }

        Patient memory patient = priorityQueue.searchPatient(_patient);

        if (specialistPatients[patient.specialist] == 0) {
            revert("Specialist does not have any patients");
        }

        _revokeRole(PATIENT_ROLE, _patient);
        specialistPatients[patient.specialist]--;
        priorityQueue.remove(_patient, reason);
    }

    function getPositionInQueue(address _patient) public view onlyRoles(SPECIALIST_ROLE, OWNER_ENTITY_ROLE) returns (Patient memory patient, uint pos) {
        return priorityQueue.searchPatientIndex(_patient);
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // FUNCIONES DEL ROL PATIENT

    function getPositionInQueue() public view onlyRole(PATIENT_ROLE) returns (Patient memory patient, uint pos) {
        return priorityQueue.searchPatientIndex(msg.sender);
    }

    // // // // // // // // // // // // // // // // // // // // // // // // // // // // 
    // FUNCIONES PÚBLICAS EXTERNAS

    function getQueueType() public view returns(string memory) {
        return _name;
    }

    function patientBelongsToSpecialist(address _patient, address _specialist) public view returns(bool) {
        return (priorityQueue.searchPatient(_patient).specialist == _specialist);
    }

    function getSpecialists() public view returns(Specialist[] memory) {
        return specialists;
    }

    function getPatientsFromSpecialist(address _specialist) private view returns(Patient[] memory) {
        uint24 counter = 0;
        uint24 patients = specialistPatients[_specialist];
        Patient[] memory result = new Patient[](patients);

        // Cola de prioridad 1
        Patient[] memory queue = priorityQueue.getQueue(Priority.Priority1);
        uint queueLength = priorityQueue.getQueueLength(Priority.Priority1);

        for (uint i = 0; i < queueLength && counter < patients; i++) {
            if (queue[i].specialist == _specialist) {
                result[counter++] = queue[i];
            }
        }

        if (counter == patients) {
            return result;
        }

        // Cola de prioridad 2
        queue = priorityQueue.getQueue(Priority.Priority2);
        queueLength = priorityQueue.getQueueLength(Priority.Priority2);

        for (uint i = 0; i < queueLength && counter < patients; i++) {
            if (queue[i].specialist == _specialist) {
                result[counter++] = queue[i];
            }
        }

        if (counter == patients) {
            return result;
        }

        // Cola de prioridad 3
        queue = priorityQueue.getQueue(Priority.Priority3);
        queueLength = priorityQueue.getQueueLength(Priority.Priority3);

        for (uint i = 0; i < queueLength && counter < patients; i++) {
            if (queue[i].specialist == _specialist) {
                result[counter++] = queue[i];
            }
        }

        return result;
    }

    function getOwnerEntityAddress() public view returns(address) {
        return OWNER_ENTITY;
    }

    function getMovementHistory() public view returns(MovementChange[] memory) {
        return priorityQueue.getMovementHistory();
    }

    function getAddRemoveHistory() public view returns(AddRemoveChange[] memory) {
        return priorityQueue.getAddRemoveHistory();
    }

    function getUpdateHistory() public view returns(UpdateSpecialistChange[] memory) {
        return priorityQueue.getUpdateHistory();
    }

    function getMovedPriorityHistory() public view returns(MovedPriority[] memory) {
        return priorityQueue.getMovedPriorityHistory();
    }

    function getQueue(Priority priority) public view returns (Patient[] memory patients) {
        return priorityQueue.getQueue(priority);
    }

    function getQueueLength(Priority priority) public view returns(uint) {
        return priorityQueue.getQueueLength(priority);
    }

    // Eventos (no utilizados aún, pueden cambiar en el futuro)
    // event PatientCreated(address patient, address specialist);
    // event PatientRemoved(address patient);
}
