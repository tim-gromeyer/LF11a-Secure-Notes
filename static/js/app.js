// Zentrales API-Modul
const API = {
    getToken: () => localStorage.getItem('sessionToken'),
    getUser: () => localStorage.getItem('currentUser'),
    
    async request(path, options = {}) {
        const token = this.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'X-Session-Token': token }),
            ...options.headers
        };

        const res = await fetch(path, { ...options, headers });
        
        if (res.status === 401 && !path.includes('/login')) {
            this.logout();
            return;
        }
        
        return res;
    },

    logout() {
        if (this.getToken()) {
            this.request('/logout', { method: 'POST' });
        }
        localStorage.clear();
        window.location.href = '/login.html';
    }
};

// Check for Auth on restricted pages
if (!API.getToken() && !window.location.pathname.includes('login.html')) {
    window.location.href = '/login.html';
}
