<script setup>
import {computed, ref, onBeforeMount} from 'vue';
import axios from 'axios';

const locations = ref({});
const loading = ref(false);
const locationToAdd = ref({});
const locationToEdit = ref({});


async function fetchLocations() {
    loading.value = true;
    const r = await axios.get("/api/locations/");
    console.log(r.data)
    locations.value = r.data;
    loading.value = false;
}

async function onLocationEditClick(location) {
    locationToEdit.value = {...location};
}

async function onUpdateLocation() {
    await axios.put(`/api/locations/${locationToEdit.value.id}/`, {
        ...locationToEdit.value
    })
    await fetchLocations();
}

async function onLocationAdd() {
    console.log(locationToAdd.value);

    await axios.post("/api/locations/", locationToAdd.value);
    await fetchLocations();
}

async function onRemoveClick(location) {
    await axios.delete(`/api/locations/${location.id}/`)
    await fetchLocations();
}

onBeforeMount(async () => {
    await fetchLocations()
})

</script>

<template>
<div class="container-fluid">
    
    <div class="p-2">
        <form @submit.prevent.stop="onLocationAdd">
            <div class="row">
                <div class="col">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="locationToAdd.name" required/>
                        <label for="floatingInput">Название</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="locationToAdd.address" required/>
                        <label for="floatingInput">Адрес</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-floating">
                        <input type="text" class="form-control" v-model="locationToAdd.capacity" required/>
                        <label for="floatingInput">Вместимость</label>
                    </div>
                </div>
                <div class="col-auto">
                    <button class="btn btn-primary">Добавить</button>
                </div>
            </div>
        </form>
    </div>
    
    <div class="modal fade" id="editLocationModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Редактировать</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="locationToEdit.name"/>
                            <label for="floatingInput">Название</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="locationToEdit.address"/>
                            <label for="floatingInput">Адрес</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="locationToEdit.capacity"/>
                            <label for="floatingInput">Вместимость</label>
                        </div>
                    </div>
                </div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click="onUpdateLocation">Сохранить</button>
            </div>
            </div>
        </div>
    </div>

    <div v-if="loading">Гружу...</div>
    <div>
        <div v-for="item in locations" class="location-item">
            <div>{{item.name}}</div>
            <button class="btn btn-success"
            @click="onLocationEditClick(item)"
                data-bs-toggle="modal" 
                data-bs-target="#editLocationModal">
                <i class="bi bi-pencil-fill"></i>
            </button>
            <button class="btn btn-danger" @click="onRemoveClick(item)">
                <i class="bi bi-x-circle"></i>
            </button>
        </div>
    </div>
</div>
</template>

<style lang="scss" scoped>
.location-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr auto auto auto;
    align-content: center;
    align-items: center;
    gap: 16px;
}
</style>
