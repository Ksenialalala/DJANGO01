
<script setup>
import { onBeforeMount, ref, computed, watch } from 'vue';
import axios from 'axios';

const participants = ref([]);

const page = ref(1);
const pageItemsCount = ref(10);
const totalCount = ref(0);
const loading = ref(false);

async function fetchParticipants() {
    loading.value = true;

    try {
        let r = await axios.get('/api/participants/', {
            params: {
                page: page.value
            }
        });

        participants.value = r.data.results || r.data;
        totalCount.value = r.data.count || participants.value.length;
    }
    finally {
        loading.value = false;
    }
}

const pagesCount = computed(() => {
    return Math.ceil(totalCount.value / pageItemsCount.value);
});

watch(page, () => {
    fetchParticipants();
});

onBeforeMount(() => {
    fetchParticipants();
});
</script>

<template>
    <div class="container mt-3">
        <h3>Участники библиотеки</h3>

        <div v-if="loading">Загружаю данные...</div>

        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">Фамилия</th>
                    <th scope="col">Имя</th>
                    <th scope="col">Логин</th>
                    <th scope="col">Электронная почта</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="p in participants" :key="p.id">
                    <th scope="row">{{ p.id }}</th>
                    <td>{{ p.last_name }}</td>
                    <td>{{ p.first_name }}</td>
                    <td>{{ p.username }}</td>
                    <td>{{ p.email }}</td>
                </tr>
            </tbody>
        </table>

        <div v-if="!loading && (!participants || participants.length === 0)">
            Участники не найдены.
        </div>

        <nav aria-label="Навигация по страницам">
            <ul class="pagination justify-content-center">
                <li class="page-item" :class="{ disabled: page <= 1 }">
                    <button
                        class="page-link"
                        :disabled="page <= 1"
                        @click="page--"
                    >
                        Previous
                    </button>
                </li>

                <li class="page-item active">
                    <span class="page-link">
                        {{ page }} из {{ pagesCount }}
                    </span>
                </li>

                <li class="page-item" :class="{ disabled: page >= pagesCount }">
                    <button
                        class="page-link"
                        :disabled="page >= pagesCount"
                        @click="page++"
                    >
                        Next
                    </button>
                </li>
            </ul>
        </nav>
    </div>
</template>

<style>
</style>
