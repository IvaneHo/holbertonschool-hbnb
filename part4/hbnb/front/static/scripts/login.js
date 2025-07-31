// Récupérer le token depuis le cookie
function getTokenFromCookie() {
    const match = document.cookie.match(/(?:^|; )access_token=([^;]+)/);
    return match ? match[1] : null;
}

// Décode le payload du JWT pour extraire l'expiration (exp) 
function getTokenExpiration(token) {
    try {
        const payload = token.split('.')[1];
        const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
        const payloadObj = JSON.parse(decoded);
        return payloadObj.exp; // timestamp en secondes
    } catch (e) {
        return null;
    }
}

// Déconnexion forcée avec message (token expiré) 
function forceLogoutWithMessage(message) {
    // Efface le cookie
    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    alert(message || "Votre session a expiré, veuillez vous reconnecter.");
    window.location.replace("login.html");
}

// Affichage du compte à rebours d'expiration du token 
function startTokenCountdown(exp) {
    const nav = document.getElementById("user-nav");
    if (!nav) return;
    // Ajoute ou trouve le span du timer
    let timerSpan = document.getElementById('token-timer');
    if (!timerSpan) {
        timerSpan = document.createElement('span');
        timerSpan.id = 'token-timer';
        timerSpan.style.marginLeft = '12px';
        nav.appendChild(timerSpan);
    }

    function updateCountdown() {
        const now = Math.floor(Date.now() / 1000);
        let diff = exp - now;
        if (diff <= 0) {
            forceLogoutWithMessage("Session expirée. Merci de vous reconnecter.");
            return;
        }
        // Format mm:ss
        const min = Math.floor(diff / 60).toString().padStart(2, '0');
        const sec = (diff % 60).toString().padStart(2, '0');
        timerSpan.textContent = `⏳ ${min}:${sec}`;
        setTimeout(updateCountdown, 1000);
    }
    updateCountdown();
}

// Récupère le nom/prénom de l'utilisateur connecté via /auth/me 
async function fetchUserName() {
    const token = getTokenFromCookie();
    if (!token) return null;
    try {
        const res = await fetch("http://127.0.0.1:5000/api/v1/auth/me", {
            headers: { Authorization: "Bearer " + token }
        });
        if (res.status === 401) {
            // Token expiré ou invalide
            forceLogoutWithMessage("Session expirée. Merci de vous reconnecter.");
            return null;
        }
        if (res.ok) {
            const data = await res.json();
            if (data.first_name && data.last_name)
                return `${data.first_name} ${data.last_name}`;
            return data.email || null;
        }
    } catch (e) {}
    return null;
}

// Affiche la navigation utilisateur (login/logout et nom) + countdown 
async function updateUserNav() {
    const nav = document.getElementById("user-nav");
    if (!nav) return;
    const token = getTokenFromCookie();

    if (token) {
        // Affiche nom utilisateur
        let name = await fetchUserName();
        if (!name) name = "Utilisateur";
        nav.innerHTML = `
            Bienvenue <b>${name}</b> !
            <a href="profile.html" class="user-link"><i>(Mon compte)</i></a>
            <a href="#" id="logout-link" class="user-link">Déconnexion</a>
        `;

        // Timer d'expiration
        const exp = getTokenExpiration(token);
        if (exp) startTokenCountdown(exp);

        // Gestion du logout
        document.getElementById("logout-link").onclick = function(e) {
            e.preventDefault();
            document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            window.location.replace("login.html");
        };
    } else {
        // UNIQUEMENT la classe login-link pour Login (jamais neon-button)
        nav.innerHTML = `<a href="login.html" class="login-link">Login</a>`;
    }
}

// LOGIN : Gestion du formulaire de connexion + Validation email live
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('email-error');
    const errorDiv = document.getElementById('login-error');

    // Regex pour email
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$/;

    // Affiche/masque le message d'erreur en tapant
    if (emailInput && emailError) {
        emailInput.addEventListener('input', () => {
            const emailVal = emailInput.value.trim();
            if (emailVal === "") {
                emailError.textContent = "L'email est requis.";
                emailInput.classList.add('input-error');
            } else if (!emailRegex.test(emailVal)) {
                emailError.textContent = "Veuillez saisir une adresse e-mail valide.";
                emailInput.classList.add('input-error');
            } else {
                emailError.textContent = "";
                emailInput.classList.remove('input-error');
            }
        });
    }

    // Validation au submit du formulaire
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            errorDiv && (errorDiv.textContent = "");
            let valid = true;

            if (emailInput && emailError) {
                const emailVal = emailInput.value.trim();
                if (emailVal === "") {
                    emailError.textContent = "L'email est requis.";
                    emailInput.classList.add('input-error');
                    valid = false;
                } else if (!emailRegex.test(emailVal)) {
                    emailError.textContent = "Veuillez saisir une adresse e-mail valide.";
                    emailInput.classList.add('input-error');
                    valid = false;
                } else {
                    emailError.textContent = "";
                    emailInput.classList.remove('input-error');
                }
            }

            if (!valid) {
                event.preventDefault();
                return;
            }

            event.preventDefault(); // Si l'email est OK, alors on continue le login AJAX

            const email = emailInput ? emailInput.value.trim() : "";
            const password = loginForm.password.value;
            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `access_token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    let message = 'Login failed.';
                    try {
                        const errorData = await response.json();
                        if (errorData.message) message = errorData.message;
                        else if (errorData.error) message = errorData.error;
                    } catch (e) {}
                    errorDiv && (errorDiv.textContent = message);
                }
            } catch (error) {
                errorDiv && (errorDiv.textContent = 'Connexion impossible. Vérifier la connexion au serveur.');
            }
        });
    }

    // Affichage utilisateur dans la barre de navigation (user-nav)
    updateUserNav && updateUserNav();
});
