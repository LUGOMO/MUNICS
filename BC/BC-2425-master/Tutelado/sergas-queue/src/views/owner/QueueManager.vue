<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed, onMounted, ref, watch } from 'vue'
import { useWeb3Store } from '@/stores/web3'
import PatientQueueModal from '@/components/owner/PatientQueueModal.vue'
import SpinnerButton from '@/components/SpinnerButton.vue'
import type { Patient } from '@/models/patient'
import QueueInfo from '@/components/QueueInfo.vue'
const web3Store = useWeb3Store()

const loading = ref(true)
const route = useRoute()
const queueId = computed(() => Number(route.params.id))
const queue = ref<Patient[]>([])

const fetchQueue = async () => {
  loading.value = true;
  await web3Store
    .getDeanonQueue(queueId.value)
    .then((res) => (queue.value = res))
    .finally(() => (loading.value = false));
};

onMounted(fetchQueue)

watch(queueId, fetchQueue)

const showModal = ref(false)
const selectedPatient = ref<Patient | null>(null)

const selectPatient = (patient: Patient) => {
  selectedPatient.value = patient
  showModal.value = true
  console.log('Selected Patient:', patient)
}

const removePatient = (patient: Patient) => {
  queue.value = queue.value.filter(p => p.address !== patient.address)
}

const updatePatient = (patient: Patient) => {
  const index = queue.value.findIndex(p => p.address === patient.address)
  if (index !== -1) {
    queue.value[index] = patient
  }
}
</script>

<template>
  <div v-if="loading" class="text-center p-4">
    <SpinnerButton />
  </div>
  <div v-else>
    <QueueInfo :queue="queue" v-model:queueId="queueId" />
    <div class="grid gap-4 p-8 grid-cols-1 md:grid-cols-[repeat(auto-fit,_minmax(26ch,_1fr))]">
      <!-- Queue Items -->
      <div
        v-for="(patient, index) in queue"
        :key="patient.address"
        class="queue-item flex flex-col items-center justify-center p-4 bg-primary text-white rounded-xl shadow-lg transition-transform hover:translate-y-[-5px] hover:shadow-xl cursor-pointer"
        @click="selectPatient(patient)"
      >
        <h3 class="text-accentlight font-bold text-lg mb-2">#{{ index + 1 }}</h3>
        <h3 class="text-white font-bold text-lg mb-2">{{ patient.name }}</h3>
        <p class="text-sm break-words">{{ patient.short_address }}</p>
        <p class="text-sm text-gray-300 break-words">{{ patient.reason }}</p>
      </div>
    <!-- Patient Modal -->
    <PatientQueueModal
      v-if="showModal"
      :patient="selectedPatient"
      @close="showModal = false"
      @remove="removePatient"
      @update="updatePatient"
    />

    </div>
  </div>
</template>
