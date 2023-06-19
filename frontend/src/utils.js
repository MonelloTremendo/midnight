import settings from './settings.js';

const api = {
    async get(endpoint = '/') {
        return await fetch(settings.api_url + endpoint, {
            method: 'GET',
        });
    },
    async put(endpoint = '/') {
        return await fetch(settings.api_url + endpoint, {
            method: 'PUT',
        });
    },
    async delete(endpoint = '/') {
        return await fetch(settings.api_url + endpoint, {
            method: 'DELETE',
        });
    },
    async post(endpoint = '/', params = {}) {
        return await fetch(settings.api_url + endpoint, {
            method: 'POST',
            body: JSON.stringify(params),
            headers: { 'content-type': 'application/json' },
        });
    },
    async patch(endpoint = '/', params = {}) {
        return await fetch(settings.api_url + endpoint, {
            method: 'PATCH',
            body: JSON.stringify(params),
            headers: { 'content-type': 'application/json' },
        });
    },
};

const colors = {
    white: '#FFFFFF',
    error: '#B00020',
    green1: '#42b983',
    green2: '#03DAC6',
    green3: '#018786',
    purple1: '#6200EE',
    purple2: '#3700B3',
    darkgrey: "#121212",
    black: '#000000',

    surface100: "#121212",
    surface200: "#282828",
    surface300: "#3f3f3f",
    surface400: "#575757",
    surface500: "#717171",
    surface600: "#8b8b8b",
}

export { api, colors };