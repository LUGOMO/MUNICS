<script setup lang="ts">
import type { AddRemoveChange } from '@/models/HistoryEntryType';

defineProps<{
  entry: AddRemoveChange;
}>();

const actionTypeToText = (actionType: number) => {
  switch (actionType) {
    case 0:
      return 'Añadido';
    case 1:
      return 'Quitado';
    case 2:
      return 'Derivado';
    case 3:
      return 'Atendido';
    default:
      return 'Desconocido';
  }
};

const actionTypeToColor = (actionType: number) => {
  switch (actionType) {
    case 0:
      return 'bg-green-600';
    case 1:
      return 'bg-red-500';
    case 2:
      return 'bg-purple-500';
    case 3:
      return 'bg-blue-500';
    default:
      return 'bg-gray-500';
  }
};

</script>

<template>
  <div
    class="history-item w-full p-4 bg-primary text-white rounded-xl shadow-lg transition-transform hover:shadow-xl"
  >
    <h3 class="text-accentlight font-bold text-lg mb-2 text-center">Añadido/Quitado de cola</h3>
    <p class="text-md mb-2">
      <strong class="text-gray-300">Timestamp:</strong> {{ new Date(entry.timestamp * 1000).toLocaleString() }}
    </p>
    <p class="text-md mb-2">
      <strong class="text-gray-300">Paciente:</strong> {{ entry.patient.hashed_address }}
    </p>
    <p class="text-md mb-2">
      <strong class="text-gray-300">Tipo de acción:</strong> <span class="font-bold"
        :class="actionTypeToColor(entry.actionType) + ' text-white px-2 py-1 rounded-md'"
      >{{ actionTypeToText(entry.actionType) }}</span>
    </p>
    <p class="text-md mb-2 break-all">
      <strong class="text-gray-300">Dirección ejecutora:</strong> {{ entry.executor }}
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
