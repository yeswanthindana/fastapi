const API_BASE = 'http://127.0.0.1:8000';

const api = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        };

        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401 && !endpoint.includes('/login')) {
            alert('Session expired. Please login again.');
            localStorage.removeItem('token');
            window.location.href = 'index.html';
            return;
        }

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || 'Something went wrong');
        }
        return data;
    },

    get(endpoint) { return this.request(endpoint); },
    post(endpoint, body) { return this.request(endpoint, { method: 'POST', body: JSON.stringify(body) }); },
    put(endpoint, body) { return this.request(endpoint, { method: 'PUT', body: JSON.stringify(body) }); },
    delete(endpoint) { return this.request(endpoint, { method: 'DELETE' }); }
};

// UI Utils
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast glass animate-fade`;
    toast.style.display = 'block';
    toast.style.background = type === 'success' ? 'rgba(34, 197, 94, 0.9)' : 'rgba(239, 68, 68, 0.9)';
    toast.style.color = 'white';
    toast.innerText = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function checkAuth() {
    const token = localStorage.getItem('token');
    const isLoginPage = window.location.pathname.endsWith('index.html') || window.location.pathname === '/';

    if (!token && !isLoginPage) {
        window.location.href = 'index.html';
    } else if (token && isLoginPage) {
        window.location.href = 'dashboard.html';
    }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = 'index.html';
}

// Navigation injection
function injectNav() {
    const nav = `
        <nav class="navbar glass">
            <div class="nav-brand">OctopiX Cloud</div>
            <div class="nav-links">
                <a href="dashboard.html">Dashboard</a>
                <a href="users.html">Users</a>
                <a href="roles.html">Roles</a>
                <a href="organizations.html">Organizations</a>
                <a href="#" onclick="logout()">Logout</a>
            </div>
        </nav>
    `;
    const container = document.getElementById('nav-container');
    if (container) container.innerHTML = nav;
}
