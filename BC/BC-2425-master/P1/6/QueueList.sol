// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {Patient} from "./models/Patient.sol";
// import {Specialist} from "./models/Specialist.sol";

contract QueueList {
    // In the future a better list method will be implemented, that favors
    // the queue operations
    Patient[] private queueList;

    MovementChange[] private movementHistory;
    AddRemoveChange[] private addRemoveHistory; 
    UpdateSpecialistChange[] private updateSpecialistHistory;

    enum ActionType { Add, Remove }

    struct MovementChange {
        Patient patient;
        uint timestamp;
        uint fromPos;
        uint toPos;
        string reason;
    }

    struct AddRemoveChange {
        ActionType actionType;
        address executor;
        Patient patient;
        uint timestamp;
        uint lastPosition;
        string reason;
    }

    struct UpdateSpecialistChange {
        address executor;
        address patient;
        uint timestamp;
        address prevSpecialist;
        address newSpecialist;
        string reason;
    }

    // event ArrayModified(ActionType action, Patient patient, uint index, uint timestamp);

    function searchPatient(address _patient) internal view returns (Patient memory patient, uint index) {
        uint currentIndex;
        bool patientFound = false;
        for (uint i = 0; i < queueList.length; i++) {
            if (queueList[i]._address == _patient) {
                currentIndex = i;
                patientFound = true;
                break;
            }
        }

        require(patientFound, "Patient not found in queue");
        return (queueList[currentIndex], currentIndex);
    }

    function add(Patient memory _patient, uint queuePos, string memory reason) internal {
        require(queuePos < queueList.length, "Position out of bounds");
        require(queuePos >= 0, "Position out of bounds");

        // Shift every patient from queuePos + 1
        queueList.push(queueList[queueList.length - 1]); // Copy the last patient to expand the array
        for (uint i = queueList.length - 1; i > queuePos; i--) {
            queueList[i] = queueList[i - 1];
        }
        queueList[queuePos] = _patient;

        _recordAddRemoveHistory(ActionType.Add, _patient, queueList.length - 1, reason);
    }

    function add(Patient memory _patient, string memory reason) internal {
        queueList.push(_patient);
        _recordAddRemoveHistory(ActionType.Add, _patient, queueList.length - 1, reason);
    }

    // Moving is a costly operation for now
    function move(address _patient, uint _newPos, string memory reason) internal {
        require(_newPos < queueList.length, "Position out of bounds");
        require(_newPos >= 0, "Position out of bounds");
        // Shift every patient from index _newPos + 1

        (Patient memory patient, uint currentIndex) = searchPatient(_patient);
        
        require(_newPos != currentIndex, "New position is the same as the current position");

        // Remove the patient from the current index and shift elements
        if (currentIndex < _newPos) {
            // Shift left: move elements from currentIndex + 1 to _newPos
            for (uint i = currentIndex; i < _newPos; i++) {
                queueList[i] = queueList[i + 1];
            }
        } else if (currentIndex > _newPos) {
            // Shift right: move elements from _newPos to currentIndex - 1
            for (uint i = currentIndex; i > _newPos; i--) {
                queueList[i] = queueList[i - 1];
            }
        }

        // Place the patient at the new position
        queueList[_newPos] = patient;

        _recordMovementHistory(patient, currentIndex, _newPos, reason);
    }

    // Remove a number by swapping with the last element and popping, then record the action
    function remove(address _patient, string memory reason) internal {

        (Patient memory removedPatient, uint currentIndex) = searchPatient(_patient);

        for (uint i = currentIndex; i < queueList.length - 1; i++) {
            queueList[i] = queueList[i + 1];
        }
        queueList.pop();

        _recordAddRemoveHistory(ActionType.Remove, removedPatient, currentIndex, reason);
    }

    function update(address _patient, address _prevSpecialist, address _newSpecialist, string memory reason) internal {
        (Patient memory patient, uint currentIndex) = searchPatient(_patient);

        require(patient.specialist != _newSpecialist, "The patient already has this specialist assigned");

        patient.specialist = _newSpecialist;
        queueList[currentIndex] = patient;

        _recordUpdateHistory(_patient, _prevSpecialist, _newSpecialist, reason);
    }

    // Internal function to record a change to the history
    function _recordMovementHistory(Patient memory patient, uint fromPos, uint toPos, string memory reason) internal {
        MovementChange memory change = MovementChange({
            patient: patient,
            timestamp: block.timestamp,
            fromPos: fromPos,
            toPos: toPos,
            reason: reason
        });
        movementHistory.push(change);
        // emit ArrayModified(action, patient, fromPos, toPos, block.timestamp);
    }

    function _recordAddRemoveHistory(ActionType action, Patient memory patient, uint lastPos, string memory reason) internal {
        AddRemoveChange memory change = AddRemoveChange({
            executor: msg.sender,
            actionType: action,
            patient: patient,
            timestamp: block.timestamp,
            lastPosition: lastPos,
            reason: reason
        });
        addRemoveHistory.push(change);
        // emit ArrayModified(action, patient, index, block.timestamp);
    }

    function _recordUpdateHistory(address patient, address prevSpecialist, address newSpecialist, string memory reason) internal {
        UpdateSpecialistChange memory change = UpdateSpecialistChange({
            executor: msg.sender,
            patient: patient,
            timestamp: block.timestamp,
            prevSpecialist: prevSpecialist,
            newSpecialist: newSpecialist,
            reason: reason
        });
        updateSpecialistHistory.push(change);
        // emit ArrayModified(action, value, index, block.timestamp);
    }

    // PUBLIC FUNCTIONS
    function getMovementHistory() public view returns(MovementChange[] memory) {
        return movementHistory;
    }
    function getAddRemoveHistory() public view returns(AddRemoveChange[] memory) {
        return addRemoveHistory;
    }
    function getUpdateHistory() public view returns(UpdateSpecialistChange[] memory) {
        return updateSpecialistHistory;
    }
    function getPatientsQueue() public view returns (Patient[] memory patients) {
        return queueList;
    }
    function getQueueLength() public view returns(uint) {
        return queueList.length;
    }
}