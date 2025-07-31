document.addEventListener('DOMContentLoaded', async () => {
    const token = getTokenFromCookie();
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    // Récupère user_id depuis le token JWT (payload base64)
    const userId = parseJwt(token)?.sub;
    if (!userId) {
        logout();
        return;
    }

    // Remplit les champs profil avec l’API
    fetchUserProfile(token, userId);

    // Gestion submit modif profil
    document.getElementById('profile-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        await saveProfile(token, userId);
    });

    // Déconnexion
    document.getElementById('logout-btn').onclick = logout;
});


function getTokenFromCookie() {
    const match = document.cookie.match(/(?:^|;\s*)access_token=([^;]+)/);
    return match ? match[1] : null;
}

function logout() {
    document.cookie = "access_token=; Max-Age=0; path=/";
    window.location.href = "login.html";
}

// Décoder JWT
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));
        return JSON.parse(jsonPayload);
    } catch (e) { return null; }
}

// GET profil actuel
async function fetchUserProfile(token, userId) {
    try {
        const res = await fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`, {
            headers: { "Authorization": "Bearer " + token }
        });
        if (res.ok) {
            const user = await res.json();
            document.getElementById('first_name').value = user.first_name || '';
            document.getElementById('last_name').value = user.last_name || '';
            document.getElementById('email').value = user.email || '';
        } else {
            showMsg("Unable to load profile. Please re-login.", true);
            setTimeout(() => logout(), 1500);
        }
    } catch {
        showMsg("Server error. Please try later.", true);
    }
}

// PUT modification profil
async function saveProfile(token, userId) {
    const first_name = document.getElementById('first_name').value.trim();
    const last_name = document.getElementById('last_name').value.trim();
    const data = { first_name, last_name };
    showMsg("Saving...", false);
    try {
        const res = await fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`, {
            method: 'PUT',
            headers: {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        if (res.ok) {
            showMsg("Profile updated!", false, true);
        } else {
            const err = await res.json();
            showMsg(err.error || err.message || "Error updating profile", true);
        }
    } catch {
        showMsg("Server error.", true);
    }
}

function showMsg(msg, error = false, success = false) {
    const box = document.getElementById('profile-message');
    box.innerHTML = msg;
    box.style.color = error ? "#f55" : (success ? "#2cf590" : "#c7f6ff");
    box.style.display = "block";
    setTimeout(() => { box.innerHTML = ""; }, 3500);
}
