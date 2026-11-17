<script setup>
import { ref, onBeforeMount } from "vue";
import axios from "axios";
import useProfileStore from "@/stores/profileStore";
import { storeToRefs } from "pinia";

const profileStore = useProfileStore();
const { role } = storeToRefs(profileStore);

const events = ref({});
const locations = ref({});
const organizers = ref({});
const loading = ref(false);

const eventToAdd = ref({});
const eventToEdit = ref({});

const eventsPictureRef = ref();
const eventsEditPictureRef = ref();

const eventAddImages = ref([]);
const eventEditImages = ref([]);

const selectedImages = ref([]);
const selectedImageIndex = ref(0);
const pictures = ref([]);

async function fetchPictures() {
  const r = await axios.get("/api/pictures/");
  pictures.value = r.data;
}

async function fetchEvents() {
  loading.value = true;

  try {
    await fetchPictures();

    const r = await axios.get("/api/events/");

    events.value = r.data.map((event) => {
      const images = (event.images || [])
        .map((image) => {
          if (typeof image === "object") {
            return image;
          }

          return pictures.value.find((picture) => picture.id === image);
        })
        .filter((image) => image);

      if (event.image) {
        images.unshift({
          id: "old",
          image: event.image,
          old: true,
        });
      }

      return {
        ...event,
        images: images,
      };
    });
  } finally {
    loading.value = false;
  }
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

function onEventEditClick(event) {
  eventToEdit.value = {
    ...event,
    images: [...(event.images || [])],
    originalImages: [...(event.images || [])],
    removeOldImage: false,
  };

  eventEditImages.value = [];
}

function eventsAddPictureChange() {
  const files = Array.from(eventsPictureRef.value.files);

  for (const file of files) {
    eventAddImages.value.push({
      file: file,
      url: URL.createObjectURL(file),
    });
  }

  eventsPictureRef.value.value = "";
}

function removeAddImage(index) {
  URL.revokeObjectURL(eventAddImages.value[index].url);
  eventAddImages.value.splice(index, 1);
}

function eventsEditPictureChange() {
  const files = Array.from(eventsEditPictureRef.value.files);

  for (const file of files) {
    eventEditImages.value.push({
      file: file,
      url: URL.createObjectURL(file),
    });
  }

  eventsEditPictureRef.value.value = "";
}

function removeEditImage(index) {
  URL.revokeObjectURL(eventEditImages.value[index].url);
  eventEditImages.value.splice(index, 1);
}

function removeSavedImage(index) {
  const image = eventToEdit.value.images[index];

  if (image.old) {
    eventToEdit.value.removeOldImage = true;
  }

  eventToEdit.value.images.splice(index, 1);
}

async function uploadImages(images) {
  const ids = [];

  for (const item of images) {
    const formData = new FormData();
    formData.append("image", item.file);

    const r = await axios.post("/api/pictures/", formData);
    ids.push(r.data.id);
  }

  return ids;
}

async function onEventAdd() {
  const data = {
    location: eventToAdd.value.location,
    organizer: eventToAdd.value.organizer,
    title: eventToAdd.value.title,
    description: eventToAdd.value.description,
    event_date: eventToAdd.value.event_date,
    max_participants: eventToAdd.value.max_participants,
    status: eventToAdd.value.status,
  };

  const r = await axios.post("/api/events/", data);

  const ids = await uploadImages(eventAddImages.value);

  if (ids.length > 0) {
    await axios.patch(`/api/events/${r.data.id}/`, {
      images: ids,
    });
  }

  for (const image of eventAddImages.value) {
    URL.revokeObjectURL(image.url);
  }

  eventAddImages.value = [];
  eventToAdd.value = {};

  await fetchEvents();
}

async function onUpdateEvent() {
  const event = eventToEdit.value;

  const data = {
    location: event.location,
    organizer: event.organizer,
    title: event.title,
    description: event.description,
    event_date: event.event_date,
    max_participants: event.max_participants,
    status: event.status,
  };

  if (event.removeOldImage) {
    data.image = null;
  }

  await axios.patch(`/api/events/${event.id}/`, data);

  const newIds = await uploadImages(eventEditImages.value);

  const ids = event.images
    .filter((image) => !image.old)
    .map((image) => image.id);

  ids.push(...newIds);

  await axios.patch(`/api/events/${event.id}/`, {
    images: ids,
  });

  const currentIds = event.images
    .filter((image) => !image.old)
    .map((image) => image.id);

  for (const image of event.originalImages) {
    if (!image.old && !currentIds.includes(image.id)) {
      await axios.delete(`/api/pictures/${image.id}/`);
    }
  }

  for (const image of eventEditImages.value) {
    URL.revokeObjectURL(image.url);
  }

  eventEditImages.value = [];

  await fetchEvents();
}

function onImageClick(images, index) {
  selectedImages.value = images;
  selectedImageIndex.value = index;
}

function previousImage() {
  if (selectedImages.value.length === 0) return;

  selectedImageIndex.value =
    (selectedImageIndex.value - 1 + selectedImages.value.length) %
    selectedImages.value.length;
}

function nextImage() {
  if (selectedImages.value.length === 0) return;

  selectedImageIndex.value =
    (selectedImageIndex.value + 1) % selectedImages.value.length;
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

async function onRegisterOnEventClick(event) {
  await axios.post(`/api/events/${event.id}/register/`)
}

onBeforeMount(async () => {
  await fetchEvents();
  await fetchLocations();
  await fetchOrganizers();
});
</script>


<template>
  <div class="container-fluid">
    <div class="p-2" v-if="role === 2">
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
            <label class="form-label">Фотографии</label>
            <input
              type="file"
              class="form-control"
              ref="eventsPictureRef"
              accept="image/*"
              multiple
              @change="eventsAddPictureChange"
            />
          </div>

          <div class="d-flex flex-wrap gap-2 mt-2">
            <div
              v-for="(image, index) in eventAddImages"
              :key="image.url"
              class="photo-item"
            >
              <img :src="image.url" alt="" />
              <button
                type="button"
                class="btn btn-danger btn-sm"
                @click="removeAddImage(index)"
              >
                Удалить
              </button>
            </div>
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

    <div class="modal fade" id="editEventModal" tabindex="-1" v-if="role === 2">
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

            <div class="mt-3">
              <label class="form-label">Фотографии мероприятия</label>

              <div class="d-flex flex-wrap gap-2">
                <div
                  v-for="(image, index) in eventToEdit.images"
                  :key="image.id"
                  class="photo-item"
                >
                  <img
                    :src="image.image"
                    alt=""
                    @click="onImageClick(eventToEdit.images, index)"
                    data-bs-toggle="modal"
                    data-bs-target="#imageModal"
                  />

                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="removeSavedImage(index)"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            </div>

            <div class="mt-3">
              <label class="form-label">Добавить фотографии</label>

              <input
                type="file"
                class="form-control"
                ref="eventsEditPictureRef"
                accept="image/*"
                multiple
                @change="eventsEditPictureChange"
              />
            </div>

            <div class="d-flex flex-wrap gap-2 mt-2">
              <div
                v-for="(image, index) in eventEditImages"
                :key="image.url"
                class="photo-item"
              >
                <img :src="image.url" alt="" />

                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="removeEditImage(index)"
                >
                  Удалить
                </button>
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
            <img
              v-if="selectedImages.length"
              :src="selectedImages[selectedImageIndex].image"
              class="img-fluid"
              alt=""
            />
          </div>

          <div class="modal-footer">
            <button
              v-if="selectedImages.length > 1"
              type="button"
              class="btn btn-secondary"
              @click="previousImage"
            >
              Предыдущая
            </button>

            <span v-if="selectedImages.length > 1">
              {{ selectedImageIndex + 1 }} из {{ selectedImages.length }}
            </span>

            <button
              v-if="selectedImages.length > 1"
              type="button"
              class="btn btn-primary"
              @click="nextImage"
            >
              Следующая
            </button>

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

        <div class="d-flex flex-wrap gap-2">
          <img
            v-for="(image, index) in item.images"
            :key="image.id"
            :src="image.image"
            class="event-image"
            alt=""
            @click="onImageClick(item.images, index)"
            data-bs-toggle="modal"
            data-bs-target="#imageModal"
          />
        </div>

        <button
          v-if="role === 2"
          class="btn btn-success"
          @click="onEventEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editEventModal"
        >
          <i class="bi bi-pencil-fill"></i>
        </button>

        <button v-if="role === 2" class="btn btn-danger" @click="onRemoveClick(item)">
          <i class="bi bi-x-circle"></i>
        </button>
        <button class="btn btn-danger" @click="onRegisterOnEventClick(item)">
          Зарегаться
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
  object-fit: contain;
  cursor: pointer;
}

.photo-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.photo-item img {
  width: 120px;
  height: 90px;
  object-fit: cover;
  cursor: pointer;
}
</style>
