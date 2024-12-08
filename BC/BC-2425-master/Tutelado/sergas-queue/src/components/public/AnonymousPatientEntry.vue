<script setup lang="ts">
import type { AnonymousPatient } from '@/models/patient';

defineProps<{
  patient: AnonymousPatient,
  index: number
}>()
</script>

<template>
  <div
    class="queue-item flex flex-col items-center justify-center p-4 bg-primary text-white rounded-xl shadow-lg transition-transform hover:shadow-xl"
  >
    <h3 class="text-accentlight font-bold text-lg mb-2">#{{ index + 1 }}</h3>
    <p class="text-sm break-words">
      <span class="short-address">{{ patient.short_address }}</span>
      <span class="full-address">{{ patient.hashed_address }}</span>
    </p>
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