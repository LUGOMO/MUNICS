export type AnonymousPatient = {
  hashed_address: string;
  short_address: string;
  priority: number;
  specialist: string;
}

export type Patient = {
  hashed_address: string;
  address: string;
  name: string;
  specialist: string;
  priority: number;
  short_address: string;
  reason: string;
}