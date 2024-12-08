<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useWeb3Store } from '@/stores/web3'
import SpinnerButton from '@/components/SpinnerButton.vue'
import PatientQueueInfo from '@/components/patient/PatientQueueInfo.vue'
import type { AnonymousPatient, Patient } from '@/models/patient'
import AnonymousPatientEntry from '@/components/public/AnonymousPatientEntry.vue'
import PatientHighlight from '@/components/patient/PatientHighlight.vue'
const web3Store = useWeb3Store()

const loading = ref(true)
const queue = ref<AnonymousPatient[]>([])
const patient = ref<Patient>()
const position = ref(0)
const priority = computed(() => patient.value?.priority ?? 0)

const fetchPatientQueue = async () => {
  loading.value = true
  await web3Store
    .getPosInQueue()
    .then((res) => ((patient.value = res.patient), (position.value = res.position)))
    .finally(() => (loading.value = false))
  if (priority.value) {
    await web3Store
      .getQueue(priority.value)
      .then((res) => (queue.value = res))
      .finally(() => (loading.value = false))
  } else {
    loading.value = false
  }
}

onMounted(() => {
  fetchPatientQueue()
})
</script>

<template>
  <div v-if="loading" class="text-center p-4">
    <SpinnerButton />
  </div>
  <div v-else>
    <PatientQueueInfo :queue="queue" :priority="priority" :patient="patient" :position="position" />
    <div class="grid gap-4 p-8 grid-cols-1 md:grid-cols-[repeat(auto-fit,_minmax(66ch,_1fr))]">
    <div 
        v-for="(queuePatient, index) in queue"
        :key="queuePatient.hashed_address"
    >
      <!-- Queue Items -->
      <PatientHighlight v-if="index == position && patient" :patient="patient" :index="index" />
      <AnonymousPatientEntry v-else :patient="queuePatient" :index="index" />
      </div>
    </div>
  </div>
</template>
