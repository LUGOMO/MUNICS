<script setup lang="ts">
import type { AnonymousPatient } from '@/models/patient';
import ColorCodedPriority from './ColorCodedPriority.vue';

defineProps<{
  queue: AnonymousPatient[]
}>()
const queueId = defineModel<number>('queueId', { required: true })
</script>

<template>
  <div class="lg:mt-28 mx-8 p-4 bg-secondary text-white rounded-lg shadow-lg text-center sticky-top">
    <h2 class="text-xl font-bold inline-block">Prioridad:</h2>
    <ColorCodedPriority :priority="queueId" />
    <br />
    <h3 class="text-lg font-semibold inline-block">Total de personas en la cola:</h3>
    <p class="text-lg font-semibold inline-block px-2 rounded-lg">
      {{ queue.length }}
    </p>
  </div>
</template>

<style scoped>
.sticky-top {
  position: sticky;
  top: 10px;
  z-index: 30;
}
</style>