<template>
  <div
    v-if="errorMessage"
    class="px-4 py-3 bg-red-100 text-red-800 border border-red-300 rounded-lg w-full"
  >
    {{ errorMessage }}
  </div>
</template>

<script setup lang="ts">
import { defineProps } from "vue";

// Define props
defineProps<{
  errorMessage: string;
}>();
</script>
