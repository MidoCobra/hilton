/**
 * Hilton Dubai JBR - Main JavaScript
 * Handles navigation, mobile menu, and interactive features
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initMobileMenu();
    initSmoothScroll();
    initScrollAnimations();
    initNewsletterForm();
    initReadMore();
});

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navOverlay = document.querySelector('.nav-overlay');
    const navLinks = document.querySelectorAll('.nav-menu a');

    if (!menuToggle || !navMenu) return;

    // Toggle menu on button click
    menuToggle.addEventListener('click', function() {
        toggleMenu();
    });

    // Close menu when clicking overlay
    if (navOverlay) {
        navOverlay.addEventListener('click', function() {
            closeMenu();
        });
    }

    // Close menu when clicking a link
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            closeMenu();
        });
    });

    // Close menu on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            closeMenu();
        }
    });

    function toggleMenu() {
        menuToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        if (navOverlay) {
            navOverlay.classList.toggle('active');
        }
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    }

    function closeMenu() {
        menuToggle.classList.remove('active');
        navMenu.classList.remove('active');
        if (navOverlay) {
            navOverlay.classList.remove('active');
        }
        document.body.style.overflow = '';
    }
}

/**
 * Smooth Scroll for anchor links
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href === '#') return;
            
            const target = document.querySelector(href);
            
            if (target) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Scroll Animations - Fade in elements on scroll
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.info-card, .restaurant-card, .benefit-card, .feature-item');
    
    // Simply add fade-in class to all elements - no hiding/showing
    animatedElements.forEach(function(el) {
        el.classList.add('fade-in');
    });
}

/**
 * Newsletter Form Handling - Using standard form submission as fallback
 */
function initNewsletterForm() {
    const form = document.querySelector('.newsletter-form');
    
    if (!form) {
        return;
    }
    
    // Just do basic validation, let the form submit normally if AJAX fails
    form.addEventListener('submit', function(e) {
        const email = form.querySelector('input[type="email"]');
        const checkbox = form.querySelector('input[type="checkbox"]');
        
        // Basic validation only - don't prevent default
        if (!email || !email.value || !isValidEmail(email.value)) {
            e.preventDefault();
            showNotification('Please enter a valid email address.', 'error');
            return;
        }
        
        if (checkbox && !checkbox.checked) {
            e.preventDefault();
            showNotification('Please agree to subscribe to the mailing list.', 'error');
            return;
        }
        
        // Let the form submit normally - the server will handle it
        // This ensures it works even if there's a JavaScript issue
    });
}

/**
 * Email Validation
 */
function isValidEmail(email) {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return pattern.test(email);
}

/**
 * Show Notification
 */
function showNotification(message, type) {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification notification-' + type;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 9999;
        animation: slideIn 0.3s ease;
        background-color: ${type === 'success' ? '#28a745' : '#dc3545'};
    `;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(function() {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(function() {
            notification.remove();
        }, 300);
    }, 3000);
}

/**
 * Add CSS for notification animations
 */
(function addNotificationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
})();

/**
 * Read more toggles for clamped descriptions
 */
function initReadMore() {
    const descriptions = document.querySelectorAll('.restaurant-content .description');

    descriptions.forEach(function(desc) {
        // create read more button
        const btn = document.createElement('button');
        btn.className = 'read-more-btn';
        btn.type = 'button';
        btn.textContent = 'Read more';
        btn.setAttribute('aria-expanded', 'false');

        // place after the description
        desc.insertAdjacentElement('afterend', btn);

        // check if overflowed (content taller than clamped area)
        function checkOverflow() {
            const isOverflowing = desc.scrollHeight > desc.clientHeight + 1; // small tolerance
            btn.style.display = isOverflowing ? 'inline-block' : 'none';
        }

        // initial check
        checkOverflow();

        // toggle handler
        btn.addEventListener('click', function() {
            const expanded = btn.getAttribute('aria-expanded') === 'true';
            if (expanded) {
                desc.classList.remove('expanded');
                btn.textContent = 'Read more';
                btn.setAttribute('aria-expanded', 'false');
                // after collapse, ensure page doesn't jump
                desc.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                desc.classList.add('expanded');
                btn.textContent = 'Show less';
                btn.setAttribute('aria-expanded', 'true');
            }
        });

        // on window resize, re-check
        window.addEventListener('resize', checkOverflow);
    });
}

/**
 * Header scroll behavior
 */
(function initHeaderScroll() {
    const header = document.querySelector('.header');
    let lastScroll = 0;
    
    if (!header) return;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll <= 0) {
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
            return;
        }
        
        if (currentScroll > lastScroll) {
            // Scrolling down
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
        } else {
            // Scrolling up
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
        
        lastScroll = currentScroll;
    });
})();

/**
 * Lazy Loading Images
 */
(function initLazyLoading() {
    if ('loading' in HTMLImageElement.prototype) {
        // Native lazy loading supported
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(function(img) {
            img.src = img.dataset.src;
        });
    } else {
        // Fallback with Intersection Observer
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver(function(entries) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const image = entry.target;
                        image.src = image.dataset.src;
                        imageObserver.unobserve(image);
                    }
                });
            });
            
            images.forEach(function(img) {
                imageObserver.observe(img);
            });
        } else {
            // Fallback: load all images
            images.forEach(function(img) {
                img.src = img.dataset.src;
            });
        }
    }
})();
