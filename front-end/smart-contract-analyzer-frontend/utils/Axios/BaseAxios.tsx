import axios from "axios"

const instance = axios.create({
    baseURL: 'http://localhost:88/',
});

export default instance;
