import axios from "axios"

const SERVER_HOST = "127.0.0.1"
const SERVER_PORT = "5000"

const server = axios.create({
    baseURL: `http://${SERVER_HOST}:${SERVER_PORT}`
});

export default server;