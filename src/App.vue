<script>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
// import HelloWorld from "./components/HelloWorld.vue";
import FileInput from "./components/FileInput.vue";
import Button from "./components/Button.vue";
import FilesList from "./components/FilesList.vue";
import PID from "./components/PID.vue";
import axios, { AxiosResponse } from "axios";

export default {
    components: {
        FilesList,
        PID,
        FileInput,
        Button,
    },
    data: () => ({
        items: [],
        files: null,
    }),
    methods: {
        async getFiles() {
            try {
                const response = await axios.get("http://127.0.0.1:4242/");
                if (response.status == 200) {
                    let listItems = [];
                    for (let i = 0; i < response.data.length; i++) {
                        let listItem = { label: response.data[i].name };
                        listItems.push(listItem);
                    }
                    this.items = listItems;
                }
            } catch (error) {
                console.error(error);
            }
        },
        async onFormSuccess() {
            this.loading = true;
            let headers = new Headers();
            headers.append("Content-Type", "application/json");
            headers.append("Accept", "application/json");
            headers.append("GET", "POST", "OPTIONS");

            console.log("files: ", this.files);
            const URL = "http://localhost:4242/upload/";
            let req_data = {
                filename: this.files.name,
            };
            console.log("file: ", req_data.filename);
            console.log("req_data: ", req_data);

            await axios
                .post(URL, req_data, headers)
                .then((response) => {
                    if (response.status == 200) {
                        this.getFiles();
                        console.log("data: ", response.data);
                        this.loading = false;
                    }
                })
                .catch((error) => console.log(error));
        },
        async deleteFiles() {
            let headers = new Headers();
            headers.append("Content-Type", "application/json");
            const URL = "http://localhost:4242/delete/";
            await axios.delete(URL, headers).then((response) => {
                console.log(response);
            });
        },
    },
    mounted() {
        this.getFiles();
    },
};
</script>

<template>
    <div class="logo-box">
        <img class="logo vite" src="./assets/vite.svg" />
        <img class="logo electron" src="./assets/electron.svg" />
        <img class="logo vue" src="./assets/vue.svg" />
        <img class="logo fastapi" src="./assets/fastapi.svg" />
    </div>
    <w-flex wrap class="text-center pa10">
        <div class="lg3 md3 sm3 xs12 pa1">
            <w-form @success="onFormSuccess" class="d-flex mb4" wrap>
                <FileInput v-model="files" class="lg9 md9 sm9 xs12 pa1" />
                <w-button
                    type="submit"
                    :loading="loading"
                    class="mla mt4 lg3 md3 sm3 xs12 pa1"
                    bg-color="primary"
                    >Add</w-button
                >
            </w-form>
            <f3>Files</f3>
            <Button
                :type="button"
                @click="deleteFiles"
                class="d-flex mla"
                bg-color="error"
                >Delete Files</Button
            >
            <FilesList :items="items" />
        </div>
        <div class="lg9 md9 sm9 xs12 pa1">
            <div class="primary-light1--bg white py3">xs9</div>
        </div>
    </w-flex>
    <PID />
</template>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}

.logo-box {
    display: flex;
    width: 100%;
    justify-content: center;
}

.static-public {
    display: flex;
    align-items: center;
    justify-content: center;
}

.static-public code {
    background-color: #eee;
    padding: 2px 4px;
    margin: 0 4px;
    border-radius: 4px;
    color: #304455;
}

.logo {
    height: 4em;
    padding: 1.5em;
    will-change: filter;
    transition: 0.75s;
}

.logo.vite:hover {
    filter: drop-shadow(0 0 2em #747bff);
}

.logo.electron:hover {
    filter: drop-shadow(0 0 2em #9feaf9);
}

.logo.vue:hover {
    filter: drop-shadow(0 0 2em #249b73);
}
</style>
