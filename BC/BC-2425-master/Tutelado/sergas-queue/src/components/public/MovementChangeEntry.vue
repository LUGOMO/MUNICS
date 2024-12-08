<script setup lang="ts">
import type { MovementChange } from '@/models/HistoryEntryType';

defineProps<{
  entry: MovementChange;
}>();
</script>

<template>
  <div
    class="history-item w-full p-4 bg-tertiary text-white rounded-xl shadow-lg transition-transform hover:shadow-xl"
  >
    <h3 class="text-accentlight font-bold text-lg mb-2 text-center">Cambio de posición</h3>
    <p class="text-md mb-2">
      <strong class="text-gray-300">Timestamp:</strong> {{ new Date(entry.timestamp * 1000).toLocaleString() }}
    </p>
    <p class="text-md mb-2 break-all">
      <strong class="text-gray-300">Paciente:</strong> {{ entry.patient.hashed_address }}
    </p>
    <p class="text-md mb-2">
      <strong class="text-gray-300">De posición:</strong> <span class="font-bold">{{ entry.fromPos }}</span>
    </p>
    <p class="text-md mb-2">
      <strong class="text-gray-300">A posición:</strong> <span class="font-bold">{{ entry.toPos }}</span>
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
