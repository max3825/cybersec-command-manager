// Thème sombre/clair
function initTheme() {
    const theme = localStorage.getItem('theme') || 'dark';
    document.body.className = theme + '-theme';
}

// Fonction de copie améliorée avec animation
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const original = button.textContent;
        
        // Add copied class for CSS animation
        button.classList.add('copied');
        button.textContent = '✅ Copié!';
        
        // Create ripple effect
        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(76, 175, 80, 0.6);
            width: 100px;
            height: 100px;
            margin-top: -50px;
            margin-left: -50px;
            top: 50%;
            left: 50%;
            animation: ripple 0.6s;
            pointer-events: none;
        `;
        button.style.position = 'relative';
        button.appendChild(ripple);
        
        // Show success notification
        showNotification('✅ Copié dans le presse-papiers!', 'success');
        
        setTimeout(() => {
            button.classList.remove('copied');
            button.textContent = original;
            if (ripple.parentNode) {
                ripple.remove();
            }
        }, 2000);
    }).catch((err) => {
        console.error('Copy failed:', err);
        showNotification('❌ Erreur: impossible de copier', 'error');
    });
}

// Show notification toast
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
        <span class="notification-message">${message}</span>
    `;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? 'linear-gradient(135deg, rgba(76, 175, 80, 0.95), rgba(56, 142, 60, 0.95))' : type === 'error' ? 'linear-gradient(135deg, rgba(255, 82, 82, 0.95), rgba(244, 67, 54, 0.95))' : 'linear-gradient(135deg, rgba(33, 150, 243, 0.95), rgba(25, 118, 210, 0.95))'};
        color: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 600;
        font-size: 0.95rem;
        z-index: 10000;
        animation: slideInRight 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.4s ease';
        setTimeout(() => notification.remove(), 400);
    }, 3000);
}

// Add keyframe animations for notifications
if (!document.getElementById('notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
        @keyframes ripple {
            from {
                opacity: 1;
                transform: scale(0);
            }
            to {
                opacity: 0;
                transform: scale(2);
            }
        }
    `;
    document.head.appendChild(style);
}

// Favoris avec localStorage
function saveFavorites(favorites) {
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

function loadFavorites() {
    return JSON.parse(localStorage.getItem('favorites') || '[]');
}

// Animations de défilement améliorées
document.addEventListener('DOMContentLoaded', function() {
    initTheme();

    // Animation des cartes au défilement avec effet stagger
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards and animated elements
    document.querySelectorAll('.command-card, .dashboard-card, .stat-mini-card, .quick-link').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s, transform 0.6s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;
        observer.observe(card);
    });

    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add parallax effect on scroll
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                const parallaxElements = document.querySelectorAll('[data-parallax]');
                parallaxElements.forEach(el => {
                    const speed = el.dataset.parallax || 0.5;
                    el.style.transform = `translateY(${scrolled * speed}px)`;
                });
                ticking = false;
            });
            ticking = true;
        }
    });

    // Add hover sound effect (optional, can be muted)
    const addHoverSound = () => {
        document.querySelectorAll('.btn, .command-card, .quick-link').forEach(el => {
            el.addEventListener('mouseenter', () => {
                // Visual feedback on hover
                el.style.transition = 'all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            });
        });
    };
    addHoverSound();

    // Initialize copy buttons
    initCopyButtons();

    // Add loading animation completion
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 100);
});

// Initialize copy buttons
function initCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const text = this.getAttribute('data-copy') || this.closest('.command-example')?.querySelector('code')?.textContent || '';
            if (text) {
                copyToClipboard(text, this);
            }
        });
    });
}

// Add class for animation
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
    
    body.loaded {
        animation: fadeIn 0.5s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);

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
