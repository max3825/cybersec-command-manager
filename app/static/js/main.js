// Thème sombre/clair
function initTheme() {
    const theme = localStorage.getItem('theme') || 'dark';
    document.body.className = theme + '-theme';
}

// Fonction de copie améliorée
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const original = button.textContent;
        button.textContent = '✅ Copié!';
        button.style.background = 'rgba(76, 175, 80, 0.4)';
        button.style.borderColor = '#4caf50';

        setTimeout(() => {
            button.textContent = original;
            button.style.background = '';
            button.style.borderColor = '';
        }, 2000);
    }).catch(() => {
        alert('❌ Erreur: impossible de copier');
    });
}

// Favoris avec localStorage
function saveFavorites(favorites) {
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

function loadFavorites() {
    return JSON.parse(localStorage.getItem('favorites') || '[]');
}

// Animations de défilement
document.addEventListener('DOMContentLoaded', function() {
    initTheme();

    // Animation des cartes au défilement
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.command-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});

// Raccourcis clavier
document.addEventListener('keydown', (e) => {
    // Ctrl+F pour focus sur recherche
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const search = document.getElementById('searchInput');
        if (search) search.focus();
    }

    // Escape pour fermer les modals
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal.active');
        if (modal) modal.classList.remove('active');
    }
});

// Tri des résultats
function sortResults(sortBy) {
    const cards = Array.from(document.querySelectorAll('.command-card:not([style*="display: none"])'));
    const container = document.getElementById('commandsGrid');

    cards.sort((a, b) => {
        let aVal = a.querySelector('.command-name').textContent;
        let bVal = b.querySelector('.command-name').textContent;

        if (sortBy === 'alpha') return aVal.localeCompare(bVal);
        if (sortBy === 'reverse') return bVal.localeCompare(aVal);
        return 0;
    });

    cards.forEach(card => container.appendChild(card));
}

// Export des données
function exportAsJSON() {
    fetch('/api/export')
    .then(r => r.json())
    .then(data => {
        const dataStr = JSON.stringify(data, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `commands_${new Date().toISOString().split('T')[0]}.json`;
        link.click();
    });
}
