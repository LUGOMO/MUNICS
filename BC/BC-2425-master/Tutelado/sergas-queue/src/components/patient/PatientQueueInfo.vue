<script setup lang="ts">
import type { AnonymousPatient, Patient } from '@/models/patient';
import ColorCodedPriority from '../ColorCodedPriority.vue';
import { computed } from 'vue';

const props = defineProps<{
  queue: AnonymousPatient[],
  patient: Patient | undefined,
  position: number,
}>()
const positionPercentage = computed(() => {
  if (props.queue.length === 0) return 0;
  return (props.position / props.queue.length) * 100;
});
const peopleAhead = computed(() => {
  return props.queue.slice(0, props.position);
});
</script>

<template>
  <div class="lg:mt-28 mx-8 p-4 bg-secondary text-white rounded-lg shadow-lg text-center sticky-top">
    <h2 class="text-xl font-bold inline-block">Prioridad:</h2>
    <ColorCodedPriority :priority="patient?.priority ?? 0" />
    <br />
    <h3 class="text-lg font-semibold inline-block">Total de personas en la cola:</h3>
    <p class="text-lg font-semibold inline-block px-2 rounded-lg">
      {{ queue.length }}
    </p>
    <br />
    <h3 class="text-lg font-semibold inline-block">Tu posición en la cola es:</h3>
    <p class="text-lg font-semibold inline-block px-2 rounded-lg">
      {{ position + 1 }}
    </p>
    <br />
    <h3 class="text-lg font-semibold inline-block">Porcentaje en la cola:</h3>
    <p class="text-lg font-semibold inline-block px-2 rounded-lg">
      {{ positionPercentage.toFixed(2) }}%
    </p>
    <br />
    <h3 class="text-lg font-semibold inline-block">Personas delante de ti:</h3>
    <p class="text-lg font-semibold inline-block px-2 rounded-lg">
      {{ peopleAhead.length }}
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