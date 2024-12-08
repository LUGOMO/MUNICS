<template>
  <div v-if="loading" class="text-center p-4">
    <WalletSpinner />
  </div>
  <div v-else class="grid gap-4 p-8 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
    <!-- Add Patient Button -->
    <div
      class="flex flex-col items-center justify-center p-4 bg-accent text-white font-bold text-3xl rounded-xl shadow-lg cursor-pointer transition-transform hover:translate-y-[-5px] hover:shadow-xl"
      @click="showAddModal = true"
    >
      <span>+</span>
    </div>

    <!-- Patient Items -->
    <div
      v-for="patient in patients"
      :key="patient.address"
      class="relative flex flex-col items-center justify-center p-4 bg-primary text-white rounded-xl shadow-lg transition-transform hover:translate-y-[-5px] hover:shadow-xl cursor-pointer"
      @click="selectPatient(patient)"
    >
      <h3 class="text-white font-bold text-lg mb-2">{{ patient.name }}</h3>
      <p class="text-md text-gray-100 break-words">{{ patient.short_address }}</p>
      <p class="text-md text-gray-300 break-words">{{ patient.reason }}</p>
      <ColorCodedPriority :priority="patient.priority" 
      :class="`absolute top-0 right-0 m-2`"
      />
    </div>

    <!-- Patient Modal -->
    <PatientModal
      v-if="showModal"
      :visible="showModal"
      :patient="selectedPatient"
      @close="closeModal"
      @remove="removePatient"
    />

    <!-- Add Patient Modal -->
    <AddPatientModal :visible="showAddModal" @close="closeAddModal" @add="addPatient" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import PatientModal from '@/components/specialist/PatientModal.vue'
import AddPatientModal from '@/components/specialist/AddPatientModal.vue'
import { type Patient } from '@/models/patient'
import WalletSpinner from '@/components/WalletSpinner.vue'
import { useWeb3Store } from '@/stores/web3'
import ColorCodedPriority from '@/components/ColorCodedPriority.vue'
const web3Store = useWeb3Store()

const patients = ref<Patient[]>([])

const showModal = ref(false)
const showAddModal = ref(false)
const selectedPatient = ref<Patient | null>(null)
const loading = ref(true)

const addPatient = (patient: Patient) => {
  patients.value = [...patients.value, patient]
}

const closeAddModal = () => {
  showAddModal.value = false
}

const selectPatient = (patient: Patient) => {
  selectedPatient.value = patient
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedPatient.value = null
}

const removePatient = () => {
  patients.value = patients.value.filter(
    (patient) => patient.hashed_address !== selectedPatient.value?.hashed_address,
  )
  closeModal()
}

onMounted(() => {
  web3Store
    .getPatients(web3Store.web3.defaultAccount)
    .then((patientsList: Patient[]) => (patients.value = patientsList))
    .finally(() => (loading.value = false))
})
</script>
