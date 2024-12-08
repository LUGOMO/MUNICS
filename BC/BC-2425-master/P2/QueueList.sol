// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {Patient} from "./models/Patient.sol";
// import {Specialist} from "./models/Specialist.sol";
import {Priority} from "./models/Priority.sol";

enum ActionType { Add, Remove, Derived, Attended }

struct MovementChange {
    Patient patient;
    uint timestamp;
    uint fromPos;
    uint toPos;
    string reason;
}

struct AddRemoveChange {
    ActionType actionType;
    Patient patient;
    address executor;
    uint timestamp;
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

struct MovedPriority {
    Patient patient;
    uint timestamp;
    uint lastPosition;
    Priority toPriority;
    string reason;
}

contract QueueList {
    Patient[] private priorityQueueList1;
    Patient[] private priorityQueueList2;
    Patient[] private priorityQueueList3;

    struct queueIndex {
        uint index;
        Priority prio;
    }

    mapping (address patient => queueIndex index) private addressToIndex;
    mapping (Priority priority => Patient[]) private PriorityQueueMapping;

    MovementChange[] private movementHistory;
    AddRemoveChange[] private addRemoveHistory; 
    UpdateSpecialistChange[] private updateSpecialistHistory;
    MovedPriority[] private movedPriorityHistory;

    constructor() {
        PriorityQueueMapping[Priority.Priority1] = priorityQueueList1;
        PriorityQueueMapping[Priority.Priority2] = priorityQueueList2;
        PriorityQueueMapping[Priority.Priority3] = priorityQueueList3;
    }

    function searchPatientIndex(address _patient) public view returns (Patient memory, uint index) {
        queueIndex memory qi = addressToIndex[_patient];
        if (qi.prio == Priority.None) {
            revert("Patient not found");
        }
        Patient memory patient = PriorityQueueMapping[qi.prio][qi.index];
        return (patient, qi.index);
    }

    function searchPatient(address _patient) public view returns (Patient memory) {
        (Patient memory patient,) = searchPatientIndex(_patient);
        return patient;
    }

    function retrievePatientQueue(address _patient) internal view returns(Patient memory, Patient[] memory queue, uint index) {
        (Patient memory patient, uint i) = searchPatientIndex(_patient);
        return (patient, PriorityQueueMapping[patient.priority], i);
    }

    function add(address _patient, address specialist, string memory name, Priority priority, string memory reason) public {
        Patient[] storage queue = PriorityQueueMapping[priority];
        Patient memory patient = Patient(_patient, specialist, name, priority);
        queue.push(patient);
        addressToIndex[_patient] = queueIndex(queue.length - 1, priority);
        _recordAddRemoveHistory(ActionType.Add, patient, reason);
    }
    

    // Moving patient in the same queue
    function move(address _patient, uint _newPos, string memory reason) public {
        (Patient memory patient, Patient[] memory queue, uint currentIndex) = retrievePatientQueue(_patient);
        
        require(_newPos < queue.length, "Position out of bounds");
        require(_newPos >= 0, "Position out of bounds");
        // Shift every patient from index _newPos + 1

        require(_newPos != currentIndex, "New position is the same as the current position");

        // Remove the patient from the current index and shift elements
        if (currentIndex < _newPos) {
            // Shift left: move elements from currentIndex + 1 to _newPos
            for (uint i = currentIndex; i < _newPos; i++) {
                queue[i] = queue[i + 1];
                addressToIndex[queue[i]._address].index--;
            }
        } else if (currentIndex > _newPos) {
            // Shift right: move elements from _newPos to currentIndex - 1
            for (uint i = currentIndex; i > _newPos; i--) {
                queue[i] = queue[i - 1];
                addressToIndex[queue[i]._address].index++;
            }
        }

        // Place the patient at the new position
        queue[_newPos] = patient;

        _recordMovementHistory(patient, currentIndex, _newPos, reason);
    }

    function changePriority(address _patient, Priority priority, Priority newPriority, string memory reason) public {
        (Patient memory patient, uint currentIndex) = searchPatientIndex(_patient);
        patient.priority = priority;
        add(_patient, patient.specialist, patient.name, newPriority, reason);
        _removeAtIndex(patient.priority, currentIndex);
        _recordMovedPriorityHistory(patient, currentIndex, newPriority, reason);
    }

    // Remove a number by swapping with the last element and popping, then record the action
    function remove(address _patient, string memory reason) public {
        (Patient memory patient, uint index) = searchPatientIndex(_patient);

        _removeAtIndex(patient.priority, index);

        _recordAddRemoveHistory(ActionType.Remove, patient, reason);
    }

    function attend(address _patient, string memory comments) public {
        (Patient memory patient, uint pos) = searchPatientIndex(_patient);

        _removeAtIndex(patient.priority, pos);

        _recordAddRemoveHistory(ActionType.Attended, patient, comments);
    }

    function attend(Priority priority, uint index, string memory comments) public {
        Patient memory patient = PriorityQueueMapping[priority][index];
        _removeAtIndex(priority, index);

        _recordAddRemoveHistory(ActionType.Attended, patient, comments);
    }

    function derive(address _patient, string memory comments) public {
        (Patient memory patient, uint pos) = searchPatientIndex(_patient);

        _removeAtIndex(patient.priority, pos);

        _recordAddRemoveHistory(ActionType.Derived, patient, comments);
    }

    function _removeAtIndex(Priority priority, uint index) internal {
        Patient[] memory queue = PriorityQueueMapping[priority];
        delete(addressToIndex[queue[index]._address]);
        for (uint i = index; i < queue.length - 1; i++) {
            queue[i] = queue[i + 1];
            addressToIndex[queue[i]._address].index--;
        }
        PriorityQueueMapping[priority].pop();
    }

    function update(address _patient, address _prevSpecialist, address _newSpecialist, string memory reason) public {
        (Patient memory patient, Patient[] memory queue, uint pos) = retrievePatientQueue(_patient);

        require(patient.specialist != _newSpecialist, "The patient already has this specialist assigned");

        patient.specialist = _newSpecialist;
        queue[pos] = patient;

        _recordUpdateHistory(_patient, _prevSpecialist, _newSpecialist, reason);
    }

    // public function to record a change to the history
    function _recordMovementHistory(Patient memory patient, uint fromPos, uint toPos, string memory reason) public {
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

    function _recordAddRemoveHistory(ActionType action, Patient memory patient, string memory reason) public {
        AddRemoveChange memory change = AddRemoveChange({
            executor: msg.sender,
            actionType: action,
            patient: patient,
            timestamp: block.timestamp,
            reason: reason
        });
        addRemoveHistory.push(change);
        // emit ArrayModified(action, patient, index, block.timestamp);
    }

    function _recordUpdateHistory(address patient, address prevSpecialist, address newSpecialist, string memory reason) public {
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

    function _recordMovedPriorityHistory(Patient memory patient, uint lastPosition, Priority newPriority, string memory reason) public {
        MovedPriority memory change = MovedPriority({
            patient: patient,
            timestamp: block.timestamp,
            lastPosition: lastPosition,
            toPriority: newPriority,
            reason: reason
        });
        movedPriorityHistory.push(change);
        // emit
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
    function getMovedPriorityHistory() public view returns(MovedPriority[] memory) {
        return movedPriorityHistory;
    }
    function getQueue(Priority priority) public view returns (Patient[] memory patients) {
        return PriorityQueueMapping[priority];
    }
    function getQueueLength(Priority priority) public view returns(uint) {
        return PriorityQueueMapping[priority].length;
    }
}