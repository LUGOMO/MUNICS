import type { AddRemoveChange, MovedPriority, MovementChange } from "./models/HistoryEntryType";
import type { AnonymousPatient, Patient } from "./models/patient";
import type { Specialist } from "./models/specialist";

/* eslint-disable @typescript-eslint/no-explicit-any */
export function shortenAddress(address: string): string {
  if (address.length <= 8) {
    return address;
  }
  return `${address.slice(0, 4)}...${address.slice(-4)}`;
}

export function mapCalldataToAnonymousPatient(patient: any): AnonymousPatient {
  return {
    short_address: shortenAddress(patient[0]),
    hashed_address: patient[0],
    specialist: patient[1],
    priority: Number(patient[2]),
  }
}

export function mapCalldataToPatient(patient: any): Patient {
  return {
    hashed_address: patient[0],
    address: patient[1],
    short_address: shortenAddress(patient[1]),
    name: patient[2],
    specialist: patient[3],
    priority: Number(patient[4]),
    reason: patient[5],
  }
}

export function mapCalldataToSpecialist(specialist: any): Specialist {
  return {
    address: specialist[0],
    short_address: shortenAddress(specialist[0]),
    name: specialist[1],
  }
}

export function mapCalldataToMovementChange(movementChange: any): MovementChange {
  return {
    patient: mapCalldataToAnonymousPatient(movementChange[0]),
    timestamp: Number(movementChange[1]),
    fromPos: Number(movementChange[2]),
    toPos: Number(movementChange[3]),
    reason: movementChange[4],
  }
}

export function mapCalldataToAddRemoveChange(addRemoveChange: any): AddRemoveChange {
  return {
    actionType: Number(addRemoveChange[0]),
    patient: mapCalldataToAnonymousPatient(addRemoveChange[1]),
    executor: addRemoveChange[2],
    timestamp: Number(addRemoveChange[3]),
    reason: addRemoveChange[4],
  }
}

export function mapCalldataToMovedPriority(movedPriority: any): MovedPriority {
  return {
    patient: mapCalldataToAnonymousPatient(movedPriority[0]),
    timestamp: Number(movedPriority[1]),
    lastPosition: Number(movedPriority[2]),
    toPriority: Number(movedPriority[3]),
    reason: movedPriority[4],
  }
}
