<template>
  <div class="flex flex-col items-center">
    <!-- Remove Button -->
    <button
      v-if="!showDeletionReason"
      class="bg-red-700 text-white py-2 px-4 rounded-lg shadow-lg hover:bg-red-800 transition"
      @click="handleRemoveClick"
    >
      <WalletSpinner v-if="loading" />
      <span v-else>Remove</span>
    </button>

    <!-- Reason Input & Confirm Button -->
    <div v-else class="mt-4 w-full">
      <input
        v-model="deletionReason"
        type="text"
        placeholder="Reason for deletion"
        class="w-full p-2 border border-gray-300 rounded-lg text-gray-800"
      />
      <div class="flex justify-center mt-2">
        <button
          class="bg-red-700 text-white py-2 px-4 rounded-lg shadow-lg hover:bg-red-800 transition"
          @click="confirmRemove"
        >
          Confirm Remove
        </button>
      </div>
    </div>

    <div class="w-full mb-4">
    <!-- Error Message -->
      <ErrorContainer v-if="errorMessage" :errorMessage="errorMessage" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import WalletSpinner from '@/components/WalletSpinner.vue';
import ErrorContainer from '@/components/ErrorContainer.vue';

defineProps<{
  loading?: boolean; // Loading state for spinner
  reason?: string; // Reason for deletion
}>();

const emit = defineEmits(['remove']); // Emits 'remove' with the reason for deletion

const showDeletionReason = ref(false);
const deletionReason = ref('');
const errorMessage = ref<string | null>(null);

// Methods
const handleRemoveClick = () => {
  showDeletionReason.value = true;
};

const confirmRemove = () => {
  if (deletionReason.value.trim()) {
    emit('remove', deletionReason.value);
  } else {
    errorMessage.value = 'Please provide a reason for deletion';
  }
};
</script>
