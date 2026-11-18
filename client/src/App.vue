<script setup>
import axios from "axios";
import Cookies from "js-cookie";
import useProfileStore from "@/stores/profileStore";
import { storeToRefs } from 'pinia';

const profileStore = useProfileStore();
const { isAuthenticated, username, role } = storeToRefs(profileStore);

async function onLogoutButtonCLick() {
  profileStore.logout();
}

</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Главная</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div
          class="collapse navbar-collapse"
          justify-content-between
          id="navbarNavDropdown"
        >
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" v-if="!isAuthenticated" to="/login">Логин</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" v-if="isAuthenticated" to="/events"
                >Мероприятия</router-link
              >
            </li>
            <li class="nav-item" v-if="role === 2">
              <router-link class="nav-link" to="/locations">Локации</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" to="/organizers"
                >Организаторы</router-link
              >
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" to="/reviews">Отзывы</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link" to="/registrations"
                >Регистрация</router-link
              >
            </li>
            <li class="nav-item" v-if="role === 2">
              <router-link class="nav-link" to="/event-materials"
                >Материалы</router-link
              >
            </li>
            <li class="nav-item" v-if="role === 2">
              <router-link class="nav-link" to="/participants"
                >Участники</router-link
              >
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Пользователь
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="/admin">Aдминка</a></li>
              </ul>
            </li>
          </ul>
          <div role="search">
            Авторизован:{{ username }}
            <button
              v-if="isAuthenticated"
              class="btn btn-outline-success"
              @click="onLogoutButtonCLick"
            >
              Выйти
            </button>
          </div>
        </div>
      </div>
    </nav>
  </div>

  <div class="container">
    <router-view />
  </div>
</template>

<style scoped>
</style>