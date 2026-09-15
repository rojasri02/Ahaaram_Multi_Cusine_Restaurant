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
| **Customer Guest** | `customer@ahaaram.com` | `customer123` | Customer Portal (`/profile`, `/orders`) |
| **Secondary Demo** | `guest@ahaaram.com` | `guest123` | Customer Portal (`/profile`, `/orders`) |

---

## 🚀 Running the Application & Test Suite

### 1. Launch the Web Application
```bash
cd Ahaaram_Restaurant
python3 app.py
```
*Access the site at `http://localhost:5000` (or `PORT` specified in environment).*

### 2. Execute Automated End-to-End Tests
```bash
python3 Ahaaram_Restaurant/test_app.py
```
All 9 end-to-end integration and acceptance tests verify database seeding, page rendering, menu queries, AJAX cart operations, checkout, table reservations, customer accounts, and administrative CRUD operations.
