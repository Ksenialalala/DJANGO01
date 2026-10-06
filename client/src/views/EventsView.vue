<script setup>
import { ref, onBeforeMount } from "vue";
import axios from "axios";

const events = ref({});
const locations = ref({});
const organizers = ref({});
const loading = ref(false);

const eventToAdd = ref({});
const eventToEdit = ref({});

const eventsPictureRef = ref();
const eventAddImageUrl = ref();
const eventsEditPictureRef = ref();

const selectedImage = ref();

async function fetchEvents() {
  loading.value = true;

  const r = await axios.get("/api/events/");

  console.log(r.data);

  events.value = r.data;
  loading.value = false;
}

async function fetchLocations() {
  const r = await axios.get("/api/locations/");

  console.log(r.data);

  locations.value = r.data;
}

async function fetchOrganizers() {
  const r = await axios.get("/api/organizers/");

  console.log(r.data);

  organizers.value = r.data;
}

async function onEventEditClick(event) {
  eventToEdit.value = { ...event };
}

async function onUpdateEvent() {
  const formData = new FormData();

  formData.append("location", eventToEdit.value.location);
  formData.append("organizer", eventToEdit.value.organizer);
  formData.append("title", eventToEdit.value.title);
  formData.append("description", eventToEdit.value.description);
  formData.append("event_date", eventToEdit.value.event_date);
  formData.append("max_participants", eventToEdit.value.max_participants);
  formData.append("status", eventToEdit.value.status);

  if (eventToEdit.value.image instanceof File) {
    formData.append("image", eventToEdit.value.image);
  }

  await axios.put(`/api/events/${eventToEdit.value.id}/`, formData);

  await fetchEvents();
}

async function onEventAdd() {
  console.log(eventToAdd.value);

  const formData = new FormData();

  formData.append("location", eventToAdd.value.location);
  formData.append("organizer", eventToAdd.value.organizer);
  formData.append("title", eventToAdd.value.title);
  formData.append("description", eventToAdd.value.description);
  formData.append("event_date", eventToAdd.value.event_date);
  formData.append("max_participants", eventToAdd.value.max_participants);
  formData.append("status", eventToAdd.value.status);

  formData.append("image", eventsPictureRef.value.files[0]);

  await axios.post("/api/events/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  await fetchEvents();
}

async function eventsAddPictureChange() {
  eventAddImageUrl.value = URL.createObjectURL(eventsPictureRef.value.files[0]);
}

function onImageClick(image) {
  selectedImage.value = image;
}

function eventsEditPictureChange() {
  eventToEdit.value.image = eventsEditPictureRef.value.files[0];
}

function onImageChange(event) {
  eventToAdd.value.image = event.target.files[0];
}

function onEditImageChange(event) {
  eventToEdit.value.image = event.target.files[0];
}

async function onRemoveClick(event) {
  await axios.delete(`/api/events/${event.id}/`);

  await fetchEvents();
}

onBeforeMount(async () => {
  await fetchEvents();
  await fetchLocations();
  await fetchOrganizers();
});
</script>


<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onEventAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="eventToAdd.location"
                required
              >
                <option v-for="location in locations" :value="location.id">
                  {{ location.name }}
                </option>
              </select>
              <label>Место</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="eventToAdd.organizer"
                required
              >
                <option v-for="organizer in organizers" :value="organizer.id">
                  {{ organizer.name }}
                </option>
              </select>
              <label>Организатор</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="eventToAdd.title"
                required
              />
              <label>Название</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="text"
                class="form-control"
                v-model="eventToAdd.description"
                required
              />
              <label>Описание</label>
            </div>
          </div>
        </div>

        <div class="row mt-2">
          <div class="col">
            <div class="form-floating">
              <input
                type="datetime-local"
                class="form-control"
                v-model="eventToAdd.event_date"
                required
              />
              <label>Дата и время</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <input
                type="number"
                class="form-control"
                v-model="eventToAdd.max_participants"
                required
              />
              <label>Максимальное количество участников</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <select class="form-select" v-model="eventToAdd.status" required>
                <option value="PLANNED">Запланировано</option>
                <option value="COMPLETED">Завершено</option>
                <option value="CANCELLED">Отменено</option>
              </select>
              <label>Статус</label>
            </div>
          </div>

          <div class="col">
            <label class="form-label">Изображение</label>
            <input
              type="file"
              class="form-control"
              ref="eventsPictureRef"
              @change="eventsAddPictureChange"
            />
          </div>

          <div class="col-auto">
            <img :src="eventAddImageUrl" style="max-height: 60px" alt="" />
          </div>

          <div class="col-auto d-flex align-items-end">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>
    </div>

    <div class="modal fade" id="editEventModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать</h1>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body">
            <div class="row">
              <div class="col">
                <div class="form-floating">
                  <select class="form-select" v-model="eventToEdit.location">
                    <option v-for="location in locations" :value="location.id">
                      {{ location.name }}
                    </option>
                  </select>
                  <label>Место</label>
                </div>
              </div>

              <div class="col">
                <div class="form-floating">
                  <select class="form-select" v-model="eventToEdit.organizer">
                    <option
                      v-for="organizer in organizers"
                      :value="organizer.id"
                    >
                      {{ organizer.name }}
                    </option>
                  </select>
                  <label>Организатор</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="eventToEdit.title"
                  />
                  <label>Название</label>
                </div>
              </div>

              <div class="col">
                <div class="form-floating">
                  <input
                    type="text"
                    class="form-control"
                    v-model="eventToEdit.description"
                  />
                  <label>Описание</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <div class="form-floating">
                  <input
                    type="datetime-local"
                    class="form-control"
                    v-model="eventToEdit.event_date"
                  />
                  <label>Дата и время</label>
                </div>
              </div>

              <div class="col">
                <div class="form-floating">
                  <input
                    type="number"
                    class="form-control"
                    v-model="eventToEdit.max_participants"
                  />
                  <label>Максимальное количество участников</label>
                </div>
              </div>

              <div class="col">
                <div class="form-floating">
                  <select class="form-select" v-model="eventToEdit.status">
                    <option value="PLANNED">Запланировано</option>
                    <option value="COMPLETED">Завершено</option>
                    <option value="CANCELLED">Отменено</option>
                  </select>
                  <label>Статус</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <label class="form-label">Изображение</label>
                <input
                  type="file"
                  class="form-control"
                  ref="eventsEditPictureRef"
                  @change="eventsEditPictureChange"
                />
              </div>
              <div class="col">
                <label class="form-label">Текущая картинка</label>

                <div v-if="eventToEdit.image">
                  <img
                    :src="eventToEdit.image"
                    style="max-height: 100px"
                    alt=""
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>

            <button
              type="button"
              class="btn btn-primary"
              data-bs-dismiss="modal"
              @click="onUpdateEvent"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="imageModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Просмотр изображения</h1>

            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>

          <div class="modal-body text-center">
            <img :src="selectedImage" class="img-fluid" alt="" />
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Закрыть
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading">Гружу...</div>

    <div>
      <div v-for="item in events" class="event-item">
        <div>
          <b>{{ item.title }}</b>
        </div>

        <div>
          {{ item.description }}
        </div>

        <div>Место: {{ item.location }}</div>

        <div>Организатор: {{ item.organizer }}</div>

        <div>Дата: {{ item.event_date }}</div>

        <div>Участники: {{ item.max_participants }}</div>

        <div>Статус: {{ item.status }}</div>

        <div v-show="item.image">
          <img
            :src="item.image"
            style="max-height: 60px; cursor: pointer"
            @click="onImageClick(item.image)"
            data-bs-toggle="modal"
            data-bs-target="#imageModal"
          />
        </div>

        <button
          class="btn btn-success"
          @click="onEventEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editEventModal"
        >
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
.event-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;

  display: grid;
  grid-template-columns: 1fr auto auto;
  align-content: center;
  align-items: center;
  gap: 16px;
}

.event-image {
  max-width: 200px;
  max-height: 150px;
}
</style>