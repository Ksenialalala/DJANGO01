<script setup>
import { ref, onBeforeMount } from "vue";
import axios from "axios";

const registrations = ref({});
const events = ref({});
const users = ref({});
const loading = ref(false);

const registrationToAdd = ref({});
const registrationToEdit = ref({});

async function fetchRegistrations() {
  loading.value = true;
  const r = await axios.get("/api/registrations/");
  console.log(r.data);
  registrations.value = r.data;
  loading.value = false;
}

async function fetchEvents() {
  const r = await axios.get("/api/events/");
  console.log(r.data);
  events.value = r.data;
}

async function fetchUsers() {
  const r = await axios.get("/api/users/");
  console.log(r.data);
  users.value = r.data;
}

async function onRegistrationEditClick(registration) {
  registrationToEdit.value = { ...registration };
}

async function onUpdateRegistration() {
  await axios.put(`/api/registrations/${registrationToEdit.value.id}/`, {
    ...registrationToEdit.value,
  });
  await fetchRegistrations();
}

async function onRegistrationAdd() {
  console.log(registrationToAdd.value);
  await axios.post("/api/registrations/", registrationToAdd.value);
  await fetchRegistrations();
}

async function onRemoveClick(registration) {
  await axios.delete(`/api/registrations/${registration.id}/`);
  await fetchRegistrations();
}

onBeforeMount(async () => {
  await fetchRegistrations();
  await fetchEvents();
  await fetchUsers();
});
</script>

<template>
  <div class="container-fluid">
    <!-- Форма добавления -->
    <div class="p-2">
      <form @submit.prevent.stop="onRegistrationAdd">
        <div class="row">
          <div class="col">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="registrationToAdd.user"
                required
              >
                <option value="" disabled>Выберите пользователя</option>

                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.username }}
                </option>
              </select>

              <label>Пользователь</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="registrationToAdd.event"
                required
              >
                <option value="" disabled>Выберите мероприятие</option>

                <option
                  v-for="event in events"
                  :key="event.id"
                  :value="event.id"
                >
                  {{ event.title }}
                </option>
              </select>

              <label>Мероприятие</label>
            </div>
          </div>

          <div class="col">
            <div class="form-floating">
              <select
                class="form-select"
                v-model="registrationToAdd.status"
                required
              >
                <option value="" disabled>Выберите статус</option>

                <option value="CREATED">Создана</option>

                <option value="CONFIRMED">Подтверждена</option>

                <option value="CANCELLED">Отменена</option>

                <option value="COMPLETED">Завершена</option>
              </select>

              <label>Статус</label>
            </div>
          </div>

          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </form>
    </div>

    <!-- Модальное окно редактирования -->
    <div class="modal fade" id="editRegistrationModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Редактировать регистрацию</h1>

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
                  <select class="form-select" v-model="registrationToEdit.user">
                    <option
                      v-for="user in users"
                      :key="user.id"
                      :value="user.id"
                    >
                      {{ user.username }}
                    </option>
                  </select>

                  <label>Пользователь</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <div class="form-floating">
                  <select
                    class="form-select"
                    v-model="registrationToEdit.event"
                  >
                    <option
                      v-for="event in events"
                      :key="event.id"
                      :value="event.id"
                    >
                      {{ event.title }}
                    </option>
                  </select>

                  <label>Мероприятие</label>
                </div>
              </div>
            </div>

            <div class="row mt-2">
              <div class="col">
                <div class="form-floating">
                  <select
                    class="form-select"
                    v-model="registrationToEdit.status"
                  >
                    <option value="CREATED">Создана</option>

                    <option value="CONFIRMED">Подтверждена</option>

                    <option value="CANCELLED">Отменена</option>

                    <option value="COMPLETED">Завершена</option>
                  </select>

                  <label>Статус</label>
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
              @click="onUpdateRegistration"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Список регистраций -->
    <div v-if="loading">Гружу...</div>

    <div>
      <div
        v-for="item in registrations"
        :key="item.id"
        class="registration-item"
      >
        <div>Пользователь: {{ item.user }}</div>

        <div>Мероприятие: {{ item.event }}</div>

        <div>Статус: {{ item.status }}</div>

        <div>Дата регистрации: {{ item.registration_date }}</div>

        <button
          class="btn btn-success"
          @click="onRegistrationEditClick(item)"
          data-bs-toggle="modal"
          data-bs-target="#editRegistrationModal"
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
.registration-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;

  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr auto auto;

  align-content: center;
  align-items: center;

  gap: 16px;
}
</style>