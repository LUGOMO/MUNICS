<script setup lang="ts">
import type { MovedPriority } from '@/models/HistoryEntryType';
import ColorCodedPriority from '@/components/ColorCodedPriority.vue';

defineProps<{
  entry: MovedPriority;
}>();
</script>

<template>
  <div
    class="history-item w-full p-4 bg-secondary text-white rounded-xl shadow-lg transition-transform hover:shadow-xl"
  >
    <h3 class="text-accentlight font-bold text-lg mb-2 text-center">Cambio de Prioridad</h3>
    <p class="text-md mb-2">
      <strong class="text-gray-300">Timestamp:</strong> {{ new Date(entry.timestamp * 1000).toLocaleString() }}
    </p>
    <p class="text-md mb-2 break-all">
      <strong class="text-gray-300">Paciente:</strong> {{ entry.patient.hashed_address }}
    </p>
    <p class="text-md mb-2">
      <strong class="text-gray-300">Última posición:</strong> {{ entry.lastPosition + 1 }}
    </p>
    <p class="text-md mb-2">
      <strong class="text-gray-300">De prioridad:</strong> <ColorCodedPriority :priority="entry.patient.priority" />
    </p>
    <p class="text-md mb-2">
      <strong class="text-gray-300">Para prioridad:</strong> <ColorCodedPriority :priority="entry.toPriority" />
    </p>
    <p class="text-md mb-2 break-words">
      <strong class="text-gray-300">Razón:</strong> {{ entry.reason }}
    </p>
  </div>
</template>

<style scoped>
.history-item {
  position: relative;
  overflow: hidden;
  margin-bottom: 1rem;
}

.history-item:last-child {
  margin-bottom: 0;
}
</style>
