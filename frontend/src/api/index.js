import axios from "axios";

const API_URL = process.env.VUE_APP_API_ROOT

export function authenticate (userData) {
    return axios.post(`${API_URL}/login`, userData)
}

export function register (userData) {
    return axios.post(`${API_URL}/register`, userData)
}