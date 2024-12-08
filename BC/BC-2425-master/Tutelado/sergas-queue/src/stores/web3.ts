/* eslint-disable @typescript-eslint/no-explicit-any */
import { defineStore } from "pinia";
import { ref } from "vue";
import Web3 from "web3";
import abi from '@/models/abi.json'
import { type Specialist } from "@/models/specialist";
import { mapCalldataToAddRemoveChange, mapCalldataToAnonymousPatient, mapCalldataToMovedPriority, mapCalldataToMovementChange, mapCalldataToPatient, mapCalldataToSpecialist } from "@/utils";
import type { AnonymousPatient, Patient } from "@/models/patient";
import type { MovedPriority, MovementChange, AddRemoveChange } from "@/models/HistoryEntryType";

export const useWeb3Store = defineStore('web3', () => {
  const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS
  const verbose = true

  // State
  const web3 = ref(new Web3(window.ethereum));
  const contract = ref(new web3.value.eth.Contract(abi, contractAddress));
  // compute this when setDefaultAccount is called
  const roleCode = ref(0);
  // retrieve from the session storage
  const cachedRoleCode = ref(Number(sessionStorage.getItem('roleCode')) || 1);

  // Use .call for read-only functions, which don't change the state of the blockchain
  // Use .send for functions that change the state of the blockchain and need user check

  // Actions
  const setDefaultAccount = async (acc: string) => {
    web3.value.defaultAccount = acc;
    if (verbose) {
      console.log('Default account:', acc)
    }
  }
  const getRole = async () => {
    try {
      roleCode.value = Number(await contract.value.methods.getRole().call({ from: web3.value.defaultAccount }))
      sessionStorage.setItem('roleCode', roleCode.value.toString())
      cachedRoleCode.value = roleCode.value
      if (verbose) {
        console.log('Role code:', roleCode.value)
      }
    } catch (error) {
      console.error('Error fetching role:', error)
      throw error
    }
  }
  const getQueueName = async () => {
    try {
      const queueName = await contract.value.methods.getQueueType().call({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Queue name:', queueName);
      }
      return queueName;
    } catch (error) {
      if (verbose) {
        console.error('Error fetching queue name:', error);
      }
      throw error;
    }
  }

  // Patient methods
  const getPosInQueue = async (): Promise<{ patient: Patient, position: number }> => {
    try {
      const patientPos: any = await contract.value.methods.getPositionInQueue().call({ from: web3.value.defaultAccount });
      const patient = patientPos[0];
      const position = patientPos[1];
      if (verbose) {
        console.log('Position in queue:', patient, position);
      }
      return {
        patient: mapCalldataToPatient(patient),
        position: Number(position),
      }
    } catch (error) {
      if (verbose) {
        console.error('Error fetching position in queue:', error);
      }
      throw error;
    }
  }

  // public methods
  const getQueue = async (priority: number): Promise<AnonymousPatient[]> => {
    try {
      const queue: any = await contract.value.methods.getQueue(priority).call({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Queue priority:', priority, queue);
      }
      return queue.map((patient: any) => (mapCalldataToAnonymousPatient(patient)));
    } catch (error) {
      if (verbose) {
        console.error('Error fetching queue priority:', priority, error);
      }
      throw error;
    }
  }

  const getQueueLength = async (priority: number): Promise<number> => {
    try {
      const queueLength: number = await contract.value.methods.getQueueLength(priority).call({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Queue length:', priority, queueLength);
      }
      return queueLength;
    } catch (error) {
      if (verbose) {
        console.error('Error fetching queue length:', priority, error);
      }
      throw error;
    }
  }

  const getHistories = async (): Promise<{ MovementChangeHistory: MovementChange[], AddRemoveChangeHistory: AddRemoveChange[], MovedPriorityHistory: MovedPriority[] }> => {
    try {
      const MovementChangeCalldata: any[] = await contract.value.methods.getMovementHistory().call({ from: web3.value.defaultAccount });
      const MovementChangeHistory = MovementChangeCalldata.map((data: any) => {
        return mapCalldataToMovementChange(data)
      });
      const AddRemoveChangeCalldata: any[] = await contract.value.methods.getAddRemoveHistory().call({ from: web3.value.defaultAccount });
      const AddRemoveChangeHistory = AddRemoveChangeCalldata.map((data: any) => {
        return mapCalldataToAddRemoveChange(data)
      });
      const MovedPriorityCalldata: any[] = await contract.value.methods.getMovedPriorityHistory().call({ from: web3.value.defaultAccount });
      const MovedPriorityHistory = MovedPriorityCalldata.map((data: any) => {
        return mapCalldataToMovedPriority(data)
      });
      if (verbose) {
        console.log('Histories:', MovedPriorityHistory, MovementChangeHistory, AddRemoveChangeHistory);
      }
      return {
        MovementChangeHistory,
        AddRemoveChangeHistory,
        MovedPriorityHistory
      };
    } catch (error) {
      if (verbose) {
        console.error('Error fetching histories:', error);
      }
      throw error;
    }
  }

  const getConveniosIPFSHash = async (): Promise<string> => {
    try {
      const hash: string = await contract.value.methods.getConveniosIPFSHash().call({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Convenios IPFS hash:', hash);
      }
      return hash;
    } catch (error) {
      if (verbose) {
        console.error('Error fetching convenios IPFS hash:', error);
      }
      throw error;
    }
  }

  // Specialists management
  const getSpecialists = async (): Promise<Specialist[]> => {
    try {
      const specialistsData = await contract.value.methods.getSpecialists().call({ from: web3.value.defaultAccount });
      if (!Array.isArray(specialistsData)) {
        throw new Error('Invalid specialists data');
      }
      const specialists: Specialist[] = specialistsData.map((data: any) => (
        mapCalldataToSpecialist(data)
      ));
      if (verbose) {
        console.log('Specialists:', specialists);
      }
      return specialists;
    } catch (error) {
      if (verbose) {
        console.error('Error fetching specialists:', error);
      }
      throw error;
    }
  }
  const addSpecialist = async (sp: Specialist) => {
    try {
      const specialist: any = await contract.value.methods.addSpecialist(sp.address, sp.name).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Specialist added:', sp.address, sp.name);
      }
      return mapCalldataToSpecialist(specialist);
    } catch (error) {
      if (verbose) {
        console.error('Error adding specialist:', error);
      }
      throw error;
    }
  }
  const removeSpecialist = async (sp: Specialist) => {
    try {
      await contract.value.methods.removeSpecialist(sp.address).call({ from: web3.value.defaultAccount });
      await contract.value.methods.removeSpecialist(sp.address).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Specialist removed:', sp.address);
      }
    } catch (error) {
      if (verbose) {
        console.error('Error removing specialist:', error);
      }
      throw error;
    }
  }

  // Patients management
  const getPatients = async (account: string | undefined): Promise<Patient[]> => {
    if (!account) {
      throw new Error('No account provided');
    }
    try {
      const patientsData = await contract.value.methods.getPatientsFromSpecialist(account).call({ from: web3.value.defaultAccount });
      if (!Array.isArray(patientsData)) {
        throw new Error('Invalid patients data');
      }
      // call await contract.value.methods.deanonymizePatient
      const hashArray: any = patientsData.map((data: any) => data[0]);
      const deanonPatients: any = await contract.value.methods.getCompletePatientData(hashArray).call({ from: web3.value.defaultAccount });
      const patients: Patient[] = deanonPatients.map((data: any) => {
        return mapCalldataToPatient(data);
      });
      if (verbose) {
        console.log('Patients:', patients);
      }
      return patients;
    } catch (error) {
      if (verbose) {
        console.error('Error fetching patients:', error);
      }
      throw error;
    }
  }
  const addPatient = async (pt: Patient, reason: string) => {
    try {
      const addedPatientData: any = await contract.value.methods.addPatient(pt.address, pt.name, pt.priority, reason).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Patient added:', pt.address, pt.name, pt.priority);
      }
      console.log(addedPatientData)
      const addedPatient: Patient = mapCalldataToPatient(addedPatientData);
      return addedPatient;
    } catch (error) {
      if (verbose) {
        console.error('Error adding patient:', error);
      }
      throw error;
    }
  }

  const removePatient = async (pt: Patient, reason: string) => {
    try {
      await contract.value.methods.removePatient(pt.address, reason).call({ from: web3.value.defaultAccount });
      await contract.value.methods.removePatient(pt.address, reason).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Patient removed:', pt.hashed_address);
      }
    } catch (error) {
      if (verbose) {
        console.error('Error removing patient:', error);
      }
      throw error;
    }
  }

  const getDeanonQueue = async (priority: number): Promise<Patient[]> => {
    try {
      const anonQueue: AnonymousPatient[] = await getQueue(priority);
      const hashArray: string[] = anonQueue.map((patient) => patient.hashed_address);
      const deanonPatients: any = await contract.value.methods.getCompletePatientData(hashArray).call({ from: web3.value.defaultAccount });
      const patients: Patient[] = deanonPatients.map((data: any) => {
        return mapCalldataToPatient(data);
      });
      if (verbose) {
        console.log('Deanon queue:', patients);
      }
      return patients;
    } catch (error) {
      if (verbose) {
        console.error('Error fetching deanon queue:', error);
      }
      throw error;
    }
  }

  const movePatientInQueue = async (pt: Patient, newPos: number, reason: string) => {
    try {
      await contract.value.methods.movePatientInQueue(pt.address, newPos, reason).call({ from: web3.value.defaultAccount });
      await contract.value.methods.movePatientInQueue(pt.address, newPos, reason).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Patient moved:', pt.address, newPos);
      }
    } catch (error) {
      if (verbose) {
        console.error('Error moving patient:', error);
      }
      throw error;
    }
  }

  const changePatientPriority = async (pt: Patient, newPriority: number, reason: string) => {
    try {
      await contract.value.methods.changePriority(pt.address, newPriority, reason).call({ from: web3.value.defaultAccount });
      await contract.value.methods.changePriority(pt.address, newPriority, reason).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Patient priority changed:', pt.address, newPriority);
      }
    } catch (error) {
      if (verbose) {
        console.error('Error changing patient priority:', error);
      }
      throw error;
    }
  }

  const attendPatient = async (pt: Patient, reason: string) => {
    try {
      await contract.value.methods.attendPatient(pt.address, reason).call({ from: web3.value.defaultAccount });
      await contract.value.methods.attendPatient(pt.address, reason).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Patient attended:', pt.address);
      }
    } catch (error) {
      if (verbose) {
        console.error('Error attending patient:', error);
      }
      throw error;
    }
  }

  const derivePatient = async (pt: Patient, reason: string) => {
    try {
      await contract.value.methods.derivePatient(pt.address, reason).call({ from: web3.value.defaultAccount });
      await contract.value.methods.derivePatient(pt.address, reason).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Patient derived:', pt.address);
      }
    } catch (error) {
      if (verbose) {
        console.error('Error deriving patient:', error);
      }
      throw error;
    }
  }

  const updateConveniosIPFSHash = async (hash: string) => {
    try {
      await contract.value.methods.setConveniosIPFSHash(hash).call({ from: web3.value.defaultAccount });
      await contract.value.methods.setConveniosIPFSHash(hash).send({ from: web3.value.defaultAccount });
      if (verbose) {
        console.log('Convenios IPFS hash updated:', hash);
      }
    } catch (error) {
      if (verbose) {
        console.error('Error updating convenios IPFS hash:', error);
      }
      throw error;
    }
  }

  const method = contract.value.methods;

  // Expose state and actions
  return {
    web3,
    method,
    roleCode,
    cachedRoleCode,
    setDefaultAccount,
    getRole,
    getQueueName,
    // OWNER METHODS
    getSpecialists,
    addSpecialist,
    removeSpecialist,
    getDeanonQueue,
    movePatientInQueue,
    changePatientPriority,
    attendPatient,
    derivePatient,
    updateConveniosIPFSHash,
    // SPECIALIST METHODS
    getPatients,
    addPatient,
    removePatient,
    // PATIENT METHODS
    getPosInQueue,
    // PUBLIC METHODS
    getQueue,
    getQueueLength,
    getHistories,
    getConveniosIPFSHash,
  };
});
