<script setup lang="ts">
import { ref } from 'vue';
import type { Patient } from '@/models/patient';

// Props
defineProps<{
  patient: Patient;
  index: number;
}>();

// State
const isHovered = ref(false);
</script>

<template>
  <div
    class="queue-item flex flex-col items-center justify-center p-4 bg-accent text-white rounded-xl shadow-lg transition-all duration-300 hover:shadow-2xl"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div class="inline-flex items-center space-x-4">
      <h3 class="text-white font-bold text-lg">#{{ index + 1 }}</h3>
      <h3 v-if="isHovered" class="text-lg">{{ patient.name }}</h3>
    </div>
    <p class="text-sm break-all">
      <span class="short-address">{{ patient.short_address }}</span>
      <span v-if="isHovered" class="text-black"> Dirección: </span> <span class="full-address">{{ patient.address }}</span>
    </p>
    <!-- Additional Info -->
    <div v-if="isHovered" class="additional-info mt-2 break-all">
      <span v-if="isHovered" class="text-black"> Dirección anónima: </span> <span class="text-xs hashed-address">{{ patient.hashed_address }}</span>
    </div>
  </div>
</template>

<style scoped>
.queue-item {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease-in-out;
}

.expanded {
  padding-bottom: 1.5rem; /* Adjust padding for expanded state */
}

.short-address {
  display: inline;
}

.full-address {
  display: none;
}

/* Expand the component and reveal the full address */
.queue-item:hover .short-address {
  display: none;
}

.queue-item:hover .full-address {
  display: inline;
}

</style>
