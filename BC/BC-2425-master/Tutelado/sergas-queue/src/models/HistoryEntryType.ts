import { type AnonymousPatient } from './patient';

export type MovedPriority = {
  patient: AnonymousPatient;
  timestamp: number; // uint in Solidity corresponds to number in TypeScript
  lastPosition: number;
  toPriority: number;
  reason: string;
};

export type MovementChange = {
  patient: AnonymousPatient;
  timestamp: number;
  fromPos: number;
  toPos: number;
  reason: string;
};

export type AddRemoveChange = {
  actionType: number;
  patient: AnonymousPatient;
  executor: string;
  timestamp: number;
  reason: string;
};
