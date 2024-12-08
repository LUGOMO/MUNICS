// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import {SensitivePatient, ExtPatient, CompletePatient} from "./models/Patient.sol";
import {Priority} from "./models/Priority.sol";

enum ActionType { Add, Remove, Derived, Attended }

struct MovementChange {
    ExtPatient patient;
    uint timestamp;
    uint fromPos;
    uint toPos;
    string reason;
}

struct AddRemoveChange {
    ActionType actionType;
    ExtPatient patient;
    address executor;
    uint timestamp;
    string reason;
}

struct UpdateSpecialistChange {
    address executor;
    ExtPatient patient;
    uint timestamp;
    address prevSpecialist;
    address newSpecialist;
    string reason;
}

struct MovedPriority {
    ExtPatient patient;
    uint timestamp;
    uint lastPosition;
    Priority toPriority;
    string reason;
}

contract QueueList {
    mapping(Priority => ExtPatient[]) private PriorityQueueMapping;

    struct QueueIndex {
        uint index;
        Priority prio;
    }

    mapping(address => QueueIndex) private addressToIndex;
    mapping(bytes32 => SensitivePatient) private hashedToPatient;

    MovementChange[] private movementHistory;
    AddRemoveChange[] private addRemoveHistory;
    UpdateSpecialistChange[] private updateSpecialistHistory;
    MovedPriority[] private movedPriorityHistory;

    bytes32 private salt;

    constructor() {
        salt = keccak256(abi.encodePacked(block.timestamp, block.difficulty, address(this)));
    }

    function calculateHashedId(address _address) public view returns (bytes32) {
        return keccak256(abi.encodePacked(_address, salt));
    }

    function retrieveAddress(bytes32 _hashedId) public view returns (SensitivePatient memory patient) {
        return hashedToPatient[_hashedId];
    }

    function anonymizePatient(SensitivePatient memory patient, address specialist, Priority priority) public view returns (ExtPatient memory) {
        bytes32 hashedId = calculateHashedId(patient._address);
        return ExtPatient({ hashedId: hashedId, priority: priority, specialist: specialist });
    }

    function deanonimizePatient(ExtPatient memory externalPatient) public view returns (CompletePatient memory) {
        SensitivePatient memory sensitivePatient = hashedToPatient[externalPatient.hashedId];
        return CompletePatient({
            hashedId: externalPatient.hashedId,
            _address: sensitivePatient._address,
            name: sensitivePatient.name,
            specialist: externalPatient.specialist,
            priority: externalPatient.priority,
            reason: sensitivePatient.reason
        });
    }

    function searchPatientIndex(address _patient) public view returns (ExtPatient memory, uint index) {
        QueueIndex memory qi = addressToIndex[_patient];
        if (qi.prio == Priority.None) revert("Patient not found");
        return (PriorityQueueMapping[qi.prio][qi.index], qi.index);
    }

    function searchPatient(address _patient) public view returns (CompletePatient memory) {
        (ExtPatient memory extPatient, ) = searchPatientIndex(_patient);
        return deanonimizePatient(extPatient);
    }

    function add(address _patient, address specialist, string memory name, Priority priority, string memory reason) public returns(ExtPatient memory, uint) {
        SensitivePatient memory patient = SensitivePatient(_patient, name, reason);
        ExtPatient memory extPatient = anonymizePatient(patient, specialist, priority);
        PriorityQueueMapping[priority].push(extPatient);
        addressToIndex[_patient] = QueueIndex(PriorityQueueMapping[priority].length - 1, priority);
        hashedToPatient[extPatient.hashedId] = patient;

        _recordAddRemoveHistory(ActionType.Add, extPatient, reason);
        return (extPatient, PriorityQueueMapping[priority].length - 1);
    }

    function move(address _patient, uint _newPos, string memory reason) public {
        (ExtPatient memory patient, uint currentIndex) = searchPatientIndex(_patient);
        require(_newPos < PriorityQueueMapping[patient.priority].length, "Position out of bounds");
        require(_newPos != currentIndex, "New position is the same as the current position");

        _shiftQueue(PriorityQueueMapping[patient.priority], currentIndex, _newPos);
        PriorityQueueMapping[patient.priority][_newPos] = patient;

        addressToIndex[_patient].index = _newPos;
        _recordMovementHistory(patient, currentIndex, _newPos, reason);
    }

    function changePriority(address _patient, Priority newPriority, string memory reason) public {
        (ExtPatient memory patient, uint currentIndex) = searchPatientIndex(_patient);

        _recordMovedPriorityHistory(patient, currentIndex, newPriority, reason);
        _removeAtIndex(patient.priority, currentIndex);

        // Add to the new priority queue
        add(_patient, patient.specialist, hashedToPatient[patient.hashedId].name, newPriority, reason);
    }

    function remove(address _patient, string memory reason) public {
        (ExtPatient memory patient, uint index) = searchPatientIndex(_patient);
        _removeAtIndex(patient.priority, index);
        _recordAddRemoveHistory(ActionType.Remove, patient, reason);
    }

    function attend(address _patient, string memory comments) public {
        (ExtPatient memory patient, uint pos) = searchPatientIndex(_patient);
        _removeAtIndex(patient.priority, pos);
        _recordAddRemoveHistory(ActionType.Attended, patient, comments);
    }

    function attend(Priority priority, uint index, string memory comments) public {
        ExtPatient memory patient = PriorityQueueMapping[priority][index];
        _removeAtIndex(priority, index);
        _recordAddRemoveHistory(ActionType.Attended, patient, comments);
    }

    function derive(address _patient, string memory comments) public {
        (ExtPatient memory patient, uint pos) = searchPatientIndex(_patient);
        _removeAtIndex(patient.priority, pos);
        _recordAddRemoveHistory(ActionType.Derived, patient, comments);
    }

    function update(ExtPatient memory _patient, address _prevSpecialist, address _newSpecialist, string memory reason) public {
        require(_patient.specialist != _newSpecialist, "Already assigned to this specialist");
        PriorityQueueMapping[_patient.priority][
            addressToIndex[hashedToPatient[_patient.hashedId]._address].index
        ].specialist = _newSpecialist;

        _recordUpdateHistory(_patient, _prevSpecialist, _newSpecialist, reason);
    }

    function _removeAtIndex(Priority priority, uint index) internal {
        ExtPatient[] storage queue = PriorityQueueMapping[priority];
        uint lastIndex = queue.length - 1;
        address removedAddress = hashedToPatient[queue[index].hashedId]._address;

        if (index != lastIndex) {
            queue[index] = queue[lastIndex];
            addressToIndex[hashedToPatient[queue[index].hashedId]._address].index = index;
        }

        queue.pop();
        delete addressToIndex[removedAddress];
    }

    function _shiftQueue(ExtPatient[] storage queue, uint from, uint to) internal {
        if (from < to) {
            for (uint i = from; i < to; i++) {
                queue[i] = queue[i + 1];
                addressToIndex[hashedToPatient[queue[i].hashedId]._address].index = i;
            }
        } else {
            for (uint i = from; i > to; i--) {
                queue[i] = queue[i - 1];
                addressToIndex[hashedToPatient[queue[i].hashedId]._address].index = i;
            }
        }
    }

    // History Records
    function _recordMovementHistory(ExtPatient memory patient, uint fromPos, uint toPos, string memory reason) internal {
        movementHistory.push(MovementChange(patient, block.timestamp, fromPos, toPos, reason));
    }

    function _recordAddRemoveHistory(ActionType action, ExtPatient memory patient, string memory reason) internal {
        addRemoveHistory.push(AddRemoveChange(action, patient, msg.sender, block.timestamp, reason));
    }

    function _recordUpdateHistory(ExtPatient memory patient, address prevSpecialist, address newSpecialist, string memory reason) internal {
        updateSpecialistHistory.push(UpdateSpecialistChange(msg.sender, patient, block.timestamp, prevSpecialist, newSpecialist, reason));
    }

    function _recordMovedPriorityHistory(ExtPatient memory patient, uint lastPosition, Priority newPriority, string memory reason) internal {
        movedPriorityHistory.push(MovedPriority(patient, block.timestamp, lastPosition, newPriority, reason));
    }

    // Public Getters
    function getMovementHistory() public view returns (MovementChange[] memory) {
        return movementHistory;
    }

    function getAddRemoveHistory() public view returns (AddRemoveChange[] memory) {
        return addRemoveHistory;
    }

    function getUpdateHistory() public view returns (UpdateSpecialistChange[] memory) {
        return updateSpecialistHistory;
    }

    function getMovedPriorityHistory() public view returns (MovedPriority[] memory) {
        return movedPriorityHistory;
    }

    function getQueue(Priority priority) public view returns (ExtPatient[] memory) {
        return PriorityQueueMapping[priority];
    }

    function getQueueLength(Priority priority) public view returns (uint) {
        return PriorityQueueMapping[priority].length;
    }
}
