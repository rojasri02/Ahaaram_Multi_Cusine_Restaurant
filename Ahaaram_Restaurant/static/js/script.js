/**
 * Ahaaram Multi Cuisine Restaurant
 * Client-side interactivity, AJAX Cart, Favorites, Gallery Lightbox, and Scroll Animations
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initScrollAnimations();
  initGallery();
  initDateConstraints();
});

/* ==========================================================================
   Toast Notifications
   ========================================================================== */
function showToast(message, type = 'gold') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">✨</span>
    <span class="toast-msg">${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

/* ==========================================================================
   Mobile Navigation
   ========================================================================== */
function initMobileNav() {
  const toggleBtn = document.querySelector('.nav-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('nav-menu-open');
      const isOpen = navMenu.classList.contains('nav-menu-open');
      toggleBtn.setAttribute('aria-expanded', isOpen);
    });
  }
}

/* ==========================================================================
   AJAX Cart Management
   ========================================================================== */
async function addToCart(foodId, quantity = 1) {
  try {
    const response = await fetch('/api/cart/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ food_id: foodId, quantity: parseInt(quantity) })
    });

    const data = await response.json();
    if (data.success) {
      updateCartBadge(data.cart_count);
      showToast(data.message || 'Added to cart!');
    } else {
      showToast(data.message || 'Could not add to cart', 'error');
    }
  } catch (err) {
    console.error('Cart add error:', err);
    showToast('Something went wrong with the cart', 'error');
  }
}

async function updateCartItem(foodId, action) {
  try {
    const response = await fetch('/api/cart/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ food_id: foodId, action: action })
    });

    const data = await response.json();
    if (data.success) {
      updateCartBadge(data.cart_count);

      // If on cart page, update quantities and totals in DOM
      const row = document.getElementById(`cart-row-${foodId}`);
      if (row) {
        if (!data.cart[foodId]) {
          row.remove();
        } else {
          const qtyElem = row.querySelector('.qty-val');
          if (qtyElem) qtyElem.textContent = data.cart[foodId].quantity;
          const itemTotalElem = row.querySelector('.item-total-price');
          if (itemTotalElem) {
            itemTotalElem.textContent = `₹${(data.cart[foodId].price * data.cart[foodId].quantity).toFixed(2)}`;
          }
        }
      }

      // Update Summary box if exists
      const subtotalElem = document.getElementById('summary-subtotal');
      const taxElem = document.getElementById('summary-tax');
      const deliveryElem = document.getElementById('summary-delivery');
      const grandTotalElem = document.getElementById('summary-grand-total');

      if (subtotalElem) subtotalElem.textContent = `₹${data.totals.subtotal.toFixed(2)}`;
      if (taxElem) taxElem.textContent = `₹${data.totals.tax.toFixed(2)}`;
      if (deliveryElem) {
        deliveryElem.textContent = data.totals.delivery_fee === 0 ? 'FREE' : `₹${data.totals.delivery_fee.toFixed(2)}`;
      }
      if (grandTotalElem) grandTotalElem.textContent = `₹${data.totals.grand_total.toFixed(2)}`;

      // If cart empty
      if (data.cart_count === 0) {
        const cartWrap = document.querySelector('.cart-layout');
        if (cartWrap) {
          cartWrap.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px;">
              <h3 style="font-size: 1.6rem; margin-bottom: 12px;">Your Cart is Empty</h3>
              <p style="color: var(--color-text-muted); margin-bottom: 24px;">Explore our multi-cuisine menu to add your favourite dishes.</p>
              <a href="/menu" class="btn btn-primary">Explore Menu</a>
            </div>
          `;
        }
      }
    }
  } catch (err) {
    console.error('Update cart error:', err);
  }
}

async function clearCart() {
  if (!confirm('Are you sure you want to clear your cart?')) return;
  try {
    const res = await fetch('/api/cart/clear', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      updateCartBadge(0);
      window.location.reload();
    }
  } catch (e) {
    console.error(e);
  }
}

function updateCartBadge(count) {
  const badge = document.querySelector('.cart-badge');
  if (badge) {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';
  }
}

/* ==========================================================================
   Favorites Toggle
   ========================================================================== */
async function toggleFavorite(foodId, btn) {
  try {
    const response = await fetch('/api/favorites/toggle', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ food_id: foodId })
    });

    if (response.status === 401) {
      showToast('Please sign in to save dishes to favorites.', 'info');
      setTimeout(() => {
        window.location.href = `/login?next=${encodeURIComponent(window.location.pathname)}`;
      }, 1500);
      return;
    }

    const data = await response.json();
    if (data.success) {
      if (data.favorited) {
        btn.classList.add('active');
        btn.innerHTML = '♥';
        showToast('Added to your favorites');
      } else {
        btn.classList.remove('active');
        btn.innerHTML = '♡';
        showToast('Removed from favorites');
      }
    }
  } catch (err) {
    console.error('Toggle favorite error:', err);
  }
}

/* ==========================================================================
   Gallery & Lightbox
   ========================================================================== */
function initGallery() {
  const filterBtns = document.querySelectorAll('.gallery-filter-btn');
  const items = document.querySelectorAll('.gallery-item');
  const lightbox = document.getElementById('gallery-lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxCaption = document.getElementById('lightbox-caption');
  const lightboxClose = document.getElementById('lightbox-close');

  // Filtering
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.getAttribute('data-filter');

      items.forEach(item => {
        if (cat === 'all' || item.getAttribute('data-category') === cat) {
          item.style.display = 'block';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  // Lightbox open
  items.forEach(item => {
    item.addEventListener('click', () => {
      if (!lightbox || !lightboxImg) return;
      const img = item.querySelector('img');
      const title = item.querySelector('h4')?.textContent || '';
      lightboxImg.src = img.src;
      if (lightboxCaption) lightboxCaption.textContent = title;
      lightbox.classList.add('active');
    });
  });

  // Lightbox close
  if (lightboxClose && lightbox) {
    lightboxClose.addEventListener('click', () => lightbox.classList.remove('active'));
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) lightbox.classList.remove('active');
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') lightbox.classList.remove('active');
    });
  }
}

/* ==========================================================================
   Date Constraints (Table Reservation)
   ========================================================================== */
function initDateConstraints() {
  const dateInput = document.getElementById('res-date');
  if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;
  }
}

/* ==========================================================================
   Scroll Reveal Animations (IntersectionObserver)
   ========================================================================== */
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in-up').forEach(el => observer.observe(el));
}
