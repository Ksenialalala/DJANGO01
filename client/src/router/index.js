import { createRouter, createWebHistory } from 'vue-router'
import LocationsView from '../views/LocationsView.vue'
import EventsView from '../views/EventsView.vue'
import OrganizersView from '../views/OrganizersView.vue'
import ReviewsView from '../views/ReviewsView.vue'
import RegistrationsView from '../views/RegistrationsView.vue'
import EventMaterialsView from '../views/EventMaterialsView.vue'
import MainPage from '@/pages/MainPage.vue'
import LoginPage from '@/pages/LoginPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
        path: "/",
        name: "MainPage",
        component: MainPage
    },
    {
      path: "/login",
      name: "LoginPage",
      component: LoginPage
    },
    {
      path: "/locations",
      name: "LocationsView",
      component: LocationsView
    },
    {
      path: "/events",
      name: "EventsView",
      component: EventsView
    },
    {
      path: "/organizers",
      name: "OrganizersView",
      component: OrganizersView
    },
    {
      path: "/reviews",
      name: "ReviewsView",
      component: ReviewsView
    },
    {
      path: "/registrations",
      name: "RegistrationsView",
      component: RegistrationsView
    },
    {
      path: "/event-materials",
      name: "EventMaterialsView",
      component: EventMaterialsView
    }
  ],
})

export default router
