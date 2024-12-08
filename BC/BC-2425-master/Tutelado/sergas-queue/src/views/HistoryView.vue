<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useWeb3Store } from '@/stores/web3';

import MovedPriorityEntry from '@/components/public/MovedPriorityEntry.vue';
import MovementChangeEntry from '@/components/public/MovementChangeEntry.vue';
import AddRemoveChangeEntry from '@/components/public/AddRemoveChangeEntry.vue';

import type { MovedPriority, MovementChange, AddRemoveChange } from '@/models/HistoryEntryType';
import SpinnerButton from '@/components/SpinnerButton.vue';

const web3Store = useWeb3Store();
const loading = ref(true);
const historyEntries = ref<(MovedPriority | MovementChange | AddRemoveChange)[]>([]);

const fetchHistory = async () => {
  loading.value = true;
  try {
    const historyData = await web3Store.getHistories(); // Assumes a method `getHistory(id)`
    historyEntries.value = [
      ...historyData.MovementChangeHistory,
      ...historyData.AddRemoveChangeHistory,
      ...historyData.MovedPriorityHistory,
    ]
    // Sort by timestamp
    historyEntries.value.sort((a, b) => b.timestamp - a.timestamp);
  } catch (error) {
    console.error('Failed to fetch history:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchHistory();
});
</script>

<template>
  <div class="flex flex-col items-center justify-center h-full p-2 lg:p-4">
    <SpinnerButton v-if="loading"/>
    <div
      v-else
      class="w-full max-w-screen-lg p-4 rounded-lg"
    >
      <div v-for="(entry, index) in historyEntries" :key="index" class="my-2">
        <MovedPriorityEntry v-if="'lastPosition' in entry" :entry="entry" />
        <MovementChangeEntry v-else-if="'fromPos' in entry" :entry="entry" />
        <AddRemoveChangeEntry v-else-if="'actionType' in entry" :entry="entry" />
      </div>
      <div v-if="historyEntries.length === 0" class="text-gray-300 text-center">
        No history available for this queue.
      </div>
    </div>
  </div>
</template>
