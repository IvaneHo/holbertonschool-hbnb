document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById('theme-toggle');
    // Si le bouton n’existe pas sur la page, on ne fait rien
    if (!btn) return;

    function updateThemeIcon() {
        if (document.documentElement.classList.contains('light')) {
            btn.textContent = "☀️";
            btn.title = "Passer en mode sombre";
        } else {
            btn.textContent = "🌙";
            btn.title = "Passer en mode clair";
        }
    }

    // Appliquer le thème au chargement de la page
    if (localStorage.getItem("theme") === "light") {
        document.documentElement.classList.add('light');
    } else {
        document.documentElement.classList.remove('light');
    }
    updateThemeIcon();

    // FONDU OVERLAY
    function fadeOverlay() {
        let overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.left = 0;
        overlay.style.top = 0;
        overlay.style.width = '100vw';
        overlay.style.height = '100vh';
        overlay.style.zIndex = 99999;
        overlay.style.pointerEvents = 'none';
        overlay.style.background = document.documentElement.classList.contains('light')
            ? 'rgba(255,255,255,0.65)' : 'rgba(15,32,39,0.75)';
        overlay.style.transition = 'opacity 0.45s cubic-bezier(0.39,0.58,0.57,1)';
        overlay.style.opacity = 1;
        document.body.appendChild(overlay);
        setTimeout(() => { overlay.style.opacity = 0; }, 35);
        setTimeout(() => { overlay.remove(); }, 550);
    }

    // Switch au clic
    btn.onclick = () => {
        document.documentElement.classList.toggle('light');
        localStorage.setItem(
            "theme",
            document.documentElement.classList.contains('light') ? "light" : "dark"
        );
        updateThemeIcon();
        fadeOverlay();
    };
});
