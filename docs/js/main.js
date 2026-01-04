// =====================================================
// selectbreakcoint Documentation JavaScript
// =====================================================

// Initialize syntax highlighting
document.addEventListener('DOMContentLoaded', function() {
    hljs.highlightAll();
    initNavigation();
    initCodeTabs();
});

// Copy install command
function copyInstall() {
    const code = document.getElementById('install-code');
    navigator.clipboard.writeText(code.textContent).then(() => {
        const btn = document.querySelector('.copy-btn');
        btn.innerHTML = `
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
        `;
        setTimeout(() => {
            btn.innerHTML = `
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2"/>
                    <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
                </svg>
            `;
        }, 2000);
    });
}

// Navigation toggle for mobile
function initNavigation() {
    const toggle = document.querySelector('.nav-toggle');
    const menu = document.querySelector('.nav-menu');
    
    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            menu.classList.toggle('active');
            toggle.classList.toggle('active');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!toggle.contains(e.target) && !menu.contains(e.target)) {
                menu.classList.remove('active');
                toggle.classList.remove('active');
            }
        });
        
        // Close menu when clicking a link
        menu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                menu.classList.remove('active');
                toggle.classList.remove('active');
            });
        });
    }
    
    // Navbar scroll effect
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.08)';
        } else {
            navbar.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
}

// Code tabs functionality
function initCodeTabs() {
    const tabs = document.querySelectorAll('.code-tab');
    const panels = document.querySelectorAll('.code-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.dataset.tab;
            
            // Update active tab
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Update active panel
            panels.forEach(panel => {
                panel.classList.remove('active');
                if (panel.id === targetId) {
                    panel.classList.add('active');
                }
            });
            
            // Re-highlight code
            hljs.highlightAll();
        });
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const navHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 20;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Copy code blocks functionality
function copyCode(button) {
    const codeBlock = button.closest('pre').querySelector('code');
    navigator.clipboard.writeText(codeBlock.textContent).then(() => {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    });
}

// Add copy buttons to all code blocks
document.querySelectorAll('.content-section pre').forEach(pre => {
    const btn = document.createElement('button');
    btn.className = 'code-copy-btn';
    btn.textContent = 'Copy';
    btn.onclick = () => copyCode(btn);
    pre.style.position = 'relative';
    pre.appendChild(btn);
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
        }
    });
}, observerOptions);

document.querySelectorAll('.feature-card, .step, .api-method').forEach(el => {
    observer.observe(el);
});
