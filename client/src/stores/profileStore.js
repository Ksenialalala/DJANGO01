import { defineStore } from "pinia";
import { ref, onBeforeMount } from "vue";
import axios from "axios";
import Cookies from "js-cookie";

const useProfileStore = defineStore('profileStore', () => {

    const isAuthenticated = ref(false);
    const username = ref(null);
    const role = ref(null);
    const userId = ref(null);

    async function fetchMe() {
        const r = await axios.get("/api/profile/me/");
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        isAuthenticated.value = r.data.is_authenticated;
        username.value = r.data.is_authenticated ? r.data.username : null;
        role.value = r.data.is_authenticated ? r.data.role : null;
        userId.value = r.data.is_authenticated ? r.data.id : null;
    }

    async function login(username, password) {
        const r = await axios.post('/api/profile/login/', {
            username: username,
            password: password
        })
        fetchMe();
    }

    async function logout() {
        await axios.post("/api/profile/logout/")
        fetchMe();
    }

    onBeforeMount(() => {
        fetchMe();
    });

    return {
        isAuthenticated,
        username,
        role,
        userId,

        fetchMe,
        login,
        logout
    }

})

export default useProfileStore;