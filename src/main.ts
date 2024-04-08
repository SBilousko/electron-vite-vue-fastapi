import { createApp } from "vue";
import App from "./App.vue";
import WaveUI from "wave-ui";
import 'wave-ui/dist/wave-ui.css'

const app = createApp(App);
app.use(WaveUI, { theme: "auto" }).mount("#app").$nextTick(() => {
    postMessage({ payload: "removeLoading" }, "*");
});
