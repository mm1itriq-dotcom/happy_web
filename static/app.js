const API_URL = 'http://localhost:5000';

function getToken() {
    return localStorage.getItem('happy_token');
}

function setAuth(token, name) {
    localStorage.setItem('happy_token', token);
    localStorage.setItem('happy_name', name);
}

function logout() {
    localStorage.removeItem('happy_token');
    localStorage.removeItem('happy_name');
    window.location.href = 'login.html';
}

function checkAuth(redirectIfNotLoggedIn = true) {
    const token = getToken();
    if (!token && redirectIfNotLoggedIn) {
        window.location.href = 'login.html';
    }
    return token;
}

// Utility to handle API calls
async function fetchApi(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
    }
    return data;
}

function showError(msgId, message) {
    const el = document.getElementById(msgId);
    if(el) {
        el.textContent = message;
        el.style.display = 'block';
    }
}

function hideError(msgId) {
    const el = document.getElementById(msgId);
    if(el) {
        el.style.display = 'none';
    }
}
