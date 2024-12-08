<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed, onMounted, ref, watch } from 'vue'
import { useWeb3Store } from '@/stores/web3'
import SpinnerButton from '@/components/SpinnerButton.vue'
import QueueInfo from '@/components/QueueInfo.vue'
import type { AnonymousPatient } from '@/models/patient'
import AnonymousPatientEntry from '@/components/public/AnonymousPatientEntry.vue'
const web3Store = useWeb3Store()

const loading = ref(true)
const route = useRoute()
const queueId = computed(() => Number(route.params.id))
const queue = ref<AnonymousPatient[]>([])

const fetchQueue = async () => {
  loading.value = true
  await web3Store
    .getQueue(queueId.value)
    .then((res) => (queue.value = res))
    .finally(() => (loading.value = false))
}

onMounted(fetchQueue)

watch(queueId, fetchQueue)
</script>

<template>
  <div v-if="loading" class="text-center p-4">
    <SpinnerButton />
  </div>
  <div v-else>
    <QueueInfo :queue="queue" v-model:queueId="queueId" />
    <div class="grid gap-4 p-8 grid-cols-1 md:grid-cols-[repeat(auto-fit,_minmax(66ch,_1fr))]">
      <!-- Queue Items -->
      <div
        v-for="(patient, index) in queue"
        :key="patient.hashed_address"
      >
      <AnonymousPatientEntry :patient="patient" :index="index" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Styling for Queue Items */
.queue-item {
  position: relative;
  overflow: hidden;
}

.short-address {
  display: inline;
  transition: opacity 0.3s ease-in-out;
}

.full-address {
  display: none;
  transition: opacity 0.3s ease-in-out;
}

/* Hover Effect */
.queue-item:hover .short-address {
  display: none;
}

.queue-item:hover .full-address {
  display: inline;
}
</style>
