
<script setup>
import { onBeforeMount, ref, computed, watch } from 'vue';
import axios from 'axios';

const participants = ref([]);

const events = ref([]);
const selectedEvent = ref('');
const loading = ref(false);

async function fetchEvents() {
    let r = await axios.get('/api/events/');
    events.value = r.data;
}

async function fetchParticipants() {

    console.log('Выбранное мероприятие:', selectedEvent.value);
    loading.value = true;

    let r = await axios.get('/api/participants/', {
        params: {
            event: selectedEvent.value
        }
    });

     console.log('URL запроса:', r.config.url, r.config.params);
    console.log('Количество участников:', r.data.length);

    participants.value = r.data;  
    loading.value = false;
    

}

const participantsFiltered = computed(() => {
    return participants.value;
})

watch(selectedEvent, () => {
    fetchParticipants();
});

onBeforeMount(() => {
    fetchEvents();
    fetchParticipants();
});
</script>

<template>
    <div>
        <div class="mb-3">
            <label for="eventSelect" class="form-label">
                Фильтр по мероприятию:
            </label>

            <select
                id="eventSelect"
                class="form-select"
                v-model="selectedEvent"
            >
                <option value="">Все участники</option>

                <option
                    v-for="event in events"
                    :key="event.id"
                    :value="event.id"
                >
                    {{ event.title }}
                </option>
            </select>
        </div>
        <div class="container mt-3">

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
                    <tr v-for="p in participantsFiltered">
                        <th scope="row">{{ p.id }}</th>
                        <td>{{ p.last_name }}</td>
                        <td>{{ p.first_name }}</td>
                        <td>{{ p.username }}</td>
                        <td>{{ p.email }}</td>
                    </tr>
                </tbody>
            </table>

            <nav aria-label="Навигация по страницам">
                <ul class="pagination justify-content-center">
                    <li class="page-item" @click="page -= 1">
                        <a class="page-link" href="#">Previous</a>
                    </li>

                    <li @click="page = page - 1" class="page-item" v-if="page - 1 > 0"><a class="page-link" >{{ page - 1 }}</a></li>
                    <li  class="page-item" v-if="page > 0"><span href="" class="page-link">{{ page  }}</span></li>
                    <li @click="page = page + 1" class="page-item" v-if="page + 1 < pagesCount"><a class="page-link" >{{ page + 1 }}</a></li>
                    <li @click="page = page + 2" class="page-item" v-if="page + 2 < pagesCount"><a class="page-link" >{{ page + 2 }}</a></li>
                    <li @click="page = page + 3" class="page-item" v-if="page + 3 < pagesCount"><a class="page-link" >{{ page + 3 }}</a></li>


                    <li class="page-item">
                        <a class="page-link" href="#" @click="page += 1">Next</a>
                    </li>
                </ul>
            </nav>
        </div>
    </div>
</template>

<style>
</style>
