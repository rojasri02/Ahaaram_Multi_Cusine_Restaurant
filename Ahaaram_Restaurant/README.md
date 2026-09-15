# Ahaaram Multi Cuisine Restaurant – Madakulam, Madurai

> **Luxury, Warm & Elegant Full-Stack Restaurant Web Application & Platform**  
> Associated with **Regency Madurai by GRT Hotels**  
> Location: *Madakulam Main Road, Madurai, Tamil Nadu, India*

---

## 🌟 Executive Summary

**Ahaaram Multi Cuisine Restaurant** is a production-grade, full-stack restaurant platform combining a **luxurious public website** with a **comprehensive digital web application**. Designed around the hospitality heritage of Madurai and GRT Hotels, the application features an authentic warm luxury aesthetic (rich gold, deep charcoal, warm ivory, and subtle cream) with rich interactivity, complete ordering workflows, table booking lifecycle management, customer accounts, and an executive administration portal.

> **Data Integrity Notice:**  
> In adherence to verification guidelines, official hotel claims, awards, and reviews are strictly kept to verified facts. Where third-party or proprietary specifics cannot be verified, clearly marked **demo/sample data** is provided for full functional demonstration.

---

## 🏆 Key Features

### 1. Public Restaurant Website
- **Grand Hero Presentation:** Immersive welcome with Madurai cultural motifs, opening hours, direct reservation booking, and menu exploration.
- **Our Story ("Where Madurai Meets the World"):** The culinary philosophy combining temple city heritage, Chettinad spice mastery, and international cuisine.
- **Dining Experiences:** Curated dining formats including the *Grand Breakfast Buffet*, *Royal Afternoon Feasts*, and *Evening Dining & Sizzlers*.
- **Interactive Menu:** 50 multi-cuisine dishes across 10 categories with real-time text search, vegetarian/non-vegetarian filter pills, category tabs, and price sorting.
- **Signature Dish Showcases:** Highlighting iconic culinary gems such as *Madurai Kari Dosa*, *Seeraga Samba Mutton Dum Biryani*, and *Royal Madurai Jigarthanda*.
- **Interactive Lightbox Photo Gallery:** High-resolution categorized imagery (Restaurant, Food, Ambience, Desserts, Beverages) with full-screen lightbox navigation.
- **Verified Guest Testimonials:** 5-star review carousel with guest review submission form.
- **Location, Map & Directions:** Regency Madurai location details, phone reservation helpline, opening schedules, and interactive Google Map iframe.

### 2. Functional Restaurant Web Application
- **AJAX Shopping Cart:** Instant slide-in flyout drawer, quantity increment/decrement, 5% Restaurant GST calculation, delivery thresholds, and live badge updates.
- **Checkout & Order Flow:** Choice of Dine-In, Takeaway, or Doorstep Delivery, custom instructions, and transparent bill calculation.
- **Order Success & Tracking:** Dedicated receipt view with live order progress status bar (*Received → Preparing → Ready → Delivered*).
- **Table Reservation System:** Multi-party table bookings with preferred meal slot, party size, seating preference, and instant reference ID generation.
- **Customer Profiles & Bookmarks:** Customer authentication (registration & sign-in), saved favourite dishes list with 1-click cart addition, order history, and booking tracking.
- **Executive Administration Console:**
  - Real-time KPI analytics (Revenue, Order volume, Pending orders, Reservations, Customers).
  - Food Catalog management (Add, Edit, Delete dishes, toggle stock availability, feature signature items).
  - Order Processing queue with dynamic status updates (*Pending*, *Preparing*, *Ready*, *Completed*, *Cancelled*).
  - Table Reservation master schedule with status management.
  - Customer directory with historical order & booking statistics.
  - Review moderation.

---

## 🔑 Demo & Test Credentials

For effortless evaluation, quick auto-fill buttons are provided on the login page:

| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@ahaaram.com` | `admin123` | Full Admin Console (`/admin`) |
| **Customer Guest** | `guest@ahaaram.com` | `guest123` | Customer Portal (`/profile`, `/orders`) |

*New customer accounts can also be created via the registration form.*

---

## 🍽️ Multi-Cuisine Menu Structure

The database is pre-seeded with **50 diverse dishes** across 10 distinct categories:
1. **South Indian:** Kari Dosa, Podi Idli, Bun Parotta, Appam & Stew, Pongal, Chettinad Kozhi.
2. **North Indian:** Dal Makhani, Paneer Tikka Masala, Murgh Makhani (Butter Chicken), Awadhi Korma.
3. **Asian:** Chilli Garlic Noodles, Veg Dim Sums, Schezwan Fried Rice, Thai Green Curry.
4. **Continental:** Creamy Penne Alfredo, Grilled Cottage Cheese Steak, Wild Mushroom Risotto.
5. **Starters:** Madurai Mutton Chukka, Gobi 65, Paneer Malai Tikka, Tandoori Chicken.
6. **Main Course:** Malabar Fish Curry, Paneer Lababdar, Kadai Vegetable, Chettinad Mutton Gravy.
7. **Breads:** Madurai Parotta, Garlic Butter Naan, Tandoori Roti, Cheese Stuffed Kulcha.
8. **Rice & Biryani:** Seeraga Samba Mutton Dum Biryani, Ambur Chicken Biryani, Ghee Rice, Curd Rice.
9. **Desserts:** Signature Royal Jigarthanda, Elaneer Payasam, Gulab Jamun with Rabri.
10. **Beverages:** Kumbakonam Degree Filter Coffee, Tempered Neer Mor, Tender Coconut Cooler.

---

## 🛠️ Technology Stack & Architecture

- **Backend Framework:** Python 3 + Flask
- **Templating Engine:** Jinja2 with template inheritance (`base.html`, `base_admin.html`)
- **Database:** SQLite 3 (`restaurant.db`) with automatic schema initialization and seeding
- **Authentication:** `werkzeug.security` (`generate_password_hash`, `check_password_hash`) and secure sessions
- **Frontend / Styling:** Custom CSS3 Design System (`/static/css/style.css`)
  - Warm Luxury Palette: Deep Charcoal (`#1a1918`), Warm Gold (`#c5a059`), Soft Ivory (`#fdfbf7`), Warm Cream (`#f4efe6`)
  - Mobile-responsive layout, CSS Grid, Flexbox, accessible touch targets
- **Client Scripting:** Pure Vanilla JavaScript (`/static/js/script.js`) with modern `fetch` APIs for asynchronous cart updates, slide drawer, and favorites.

---

## 🚀 Installation & Local Run Guide

### Prerequisites
- Python 3.9+ installed
- `pip` package manager

### Step-by-Step Setup

1. **Clone or Navigate to the Project Directory:**
   ```bash
   cd Ahaaram_Restaurant
   ```

2. **(Optional) Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database (Automatic on Startup):**
   The database seeds automatically on first run. If you wish to manually re-seed or reset:
   ```bash
   python3 database/seed_data.py
   ```

5. **Run the Application:**
   ```bash
   python3 app.py
   ```
   *The application will start on `http://0.0.0.0:5000` (or `PORT` defined in your environment).*

---

## 📂 Project Structure

```
Ahaaram_Restaurant/
├── app.py                      # Core Flask application, controllers & REST APIs
├── requirements.txt            # Python dependencies (Flask, Werkzeug)
├── README.md                   # Complete system documentation
├── database/
│   ├── seed_data.py            # SQLite schema definition and 50-dish seed dataset
│   └── restaurant.db           # SQLite database file (auto-generated)
├── static/
│   ├── css/
│   │   └── style.css           # Luxury design system, responsive styles, animations
│   └── js/
│       └── script.js           # AJAX shopping cart, drawer, favorites, lightbox
└── templates/
    ├── base.html               # Master layout with navbar, cart drawer & footer
    ├── index.html              # Homepage with hero, specials, and reviews
    ├── about.html              # Restaurant story and Madurai heritage
    ├── menu.html               # Full menu with search, filters & price sorting
    ├── food_details.html       # Dish detail view with quantity controls
    ├── dining.html             # Breakfast, Lunch, Dinner dining experiences
    ├── gallery.html            # High-res photo gallery with modal lightbox
    ├── reviews.html            # Customer testimonials & review submission
    ├── contact.html            # Contact info, timings, and interactive Google map
    ├── reservation.html        # Table booking form
    ├── my_reservations.html    # Customer's active table reservations
    ├── cart.html               # Full shopping cart page
    ├── checkout.html           # Checkout with Dine-in / Takeaway / Delivery
    ├── order_success.html      # Receipt and 4-step status tracker
    ├── orders.html             # Customer order history
    ├── login.html              # Authentication with 1-click demo auto-fill
    ├── register.html           # New guest account registration
    ├── profile.html            # Customer dashboard with saved favourites
    ├── 404.html                # Custom 404 error page
    ├── 500.html                # Custom 500 error page
    └── admin/
        ├── base_admin.html     # Administration console sidebar layout
        ├── dashboard.html      # Real-time KPIs, recent orders & reservations
        ├── foods.html          # Menu catalog management & stock toggling
        ├── add_food.html       # Add dish form with dietary and pricing fields
        ├── edit_food.html      # Edit dish details form
        ├── orders.html         # Kitchen order queue with status updater
        ├── reservations.html   # Table seating log with confirmation actions
        ├── customers.html      # Customer profiles directory & order metrics
        └── reviews.html        # Guest feedback moderation
```

---

## 🛡️ Security & Quality Standards

- **Password Hashing:** PBKDF2 with SHA-256 via Werkzeug.
- **SQL Injection Prevention:** 100% parameterized SQL queries (`?` placeholders).
- **Role-Based Access Control:** `@login_required` and `@admin_required` decorators protecting sensitive routes.
- **Session Protection:** Signed sessions with server-side secret key.
- **Input Validation:** Required field validation, date constraint checks (no past reservation bookings).
- **Responsive Viewports:** Tested for seamless performance across mobile, tablet, and widescreen desktop screens.
