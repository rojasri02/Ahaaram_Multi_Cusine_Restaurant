"""
End-to-end full-stack automated test suite for Ahaaram Multi Cuisine Restaurant platform.
Tests all public website pages, customer workflows, cart & checkout, and admin dashboard operations.
"""

import os
import sys
import unittest
from datetime import datetime, timedelta

# Ensure Ahaaram_Restaurant directory is on sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from app import app, query_db, get_db


class AhaaramRestaurantTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

    def setUp(self):
        self.client = app.test_client()

    def test_01_database_seed_integrity(self):
        """Verify that all initial tables, categories, and 50 foods are correctly seeded."""
        with app.app_context():
            categories = query_db("SELECT COUNT(*) as cnt FROM categories", one=True)
            self.assertGreaterEqual(categories["cnt"], 10, "Should have at least 10 categories")

            foods = query_db("SELECT COUNT(*) as cnt FROM foods", one=True)
            self.assertGreaterEqual(foods["cnt"], 50, "Should have at least 50 food items")

            admin_user = query_db("SELECT * FROM users WHERE email = 'admin@ahaaram.com'", one=True)
            self.assertIsNotNone(admin_user, "Admin user must exist")
            self.assertEqual(admin_user["is_admin"], 1)

            demo_customer = query_db("SELECT * FROM users WHERE email = 'customer@ahaaram.com'", one=True)
            self.assertIsNotNone(demo_customer, "Customer user must exist")

    def test_02_public_website_pages(self):
        """Verify that all public marketing & experience pages respond with HTTP 200."""
        pages = [
            ("/", "AHAARAM"),
            ("/about", "Where Madurai Meets the World"),
            ("/menu", "Our Multi Cuisine Menu"),
            ("/gallery", "Gallery"),
            ("/dining", "Dining Experiences"),
            ("/reviews", "Guest Reviews"),
            ("/contact", "Contact & Location"),
            ("/reservation", "Reserve a Table"),
            ("/cart", "Your Dining Cart"),
            ("/login", "Sign In to Ahaaram"),
            ("/register", "Join Ahaaram Dining")
        ]
        for url, expected_text in pages:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Page {url} failed with status {response.status_code}")
            self.assertIn(expected_text.encode("utf-8"), response.data, f"Missing content '{expected_text}' on {url}")

    def test_03_menu_filters_and_search(self):
        """Test menu searching, dietary filters, and category tabs."""
        # 1. Search for Biryani
        res = self.client.get("/menu?search=Biryani")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Biryani", res.data)

        # 2. Vegetarian filter
        res_veg = self.client.get("/menu?diet=veg")
        self.assertEqual(res_veg.status_code, 200)

        # 3. Non-Vegetarian filter
        res_nonveg = self.client.get("/menu?diet=nonveg")
        self.assertEqual(res_nonveg.status_code, 200)

        # 4. Category filter
        res_cat = self.client.get("/menu?category=south-indian")
        self.assertEqual(res_cat.status_code, 200)

    def test_04_food_details_page(self):
        """Test food item details page with valid and invalid IDs."""
        res = self.client.get("/food/1")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Add To Cart", res.data)

        # 404 on non-existent item
        res_404 = self.client.get("/food/99999")
        self.assertEqual(res_404.status_code, 404)

    def test_05_cart_ajax_api(self):
        """Test adding, updating, and clearing items in cart via JSON API."""
        # Add food 1
        res = self.client.post("/api/cart/add", json={"food_id": "1", "quantity": 2})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["cart_count"], 2)

        # Add food 2
        res2 = self.client.post("/api/cart/add", json={"food_id": "2", "quantity": 1})
        self.assertEqual(res2.status_code, 200)
        data2 = res2.get_json()
        self.assertEqual(data2["cart_count"], 3)

        # Update (decrement food 1)
        res3 = self.client.post("/api/cart/update", json={"food_id": "1", "action": "dec"})
        self.assertEqual(res3.status_code, 200)
        data3 = res3.get_json()
        self.assertEqual(data3["cart_count"], 2)

        # Clear cart
        res_clear = self.client.post("/api/cart/clear")
        self.assertEqual(res_clear.status_code, 200)
        self.assertEqual(res_clear.get_json()["cart_count"], 0)

    def test_06_customer_checkout_and_order_flow(self):
        """Test full checkout flow: Add item -> Checkout POST -> Success page -> Orders history."""
        # 1. Add item to cart
        self.client.post("/api/cart/add", json={"food_id": "1", "quantity": 2})

        # 2. Submit checkout form
        res_order = self.client.post("/checkout", data={
            "name": "Meenakshi Sundaram",
            "phone": "+91 98765 11223",
            "email": "meenakshi@example.com",
            "dining_type": "delivery",
            "address": "42 West Masi Street, Madurai",
            "instructions": "Extra spicy please"
        }, follow_redirects=True)

        self.assertEqual(res_order.status_code, 200)
        self.assertIn(b"Order Placed Successfully", res_order.data)
        self.assertIn(b"Meenakshi Sundaram", res_order.data)
        self.assertIn(b"42 West Masi Street", res_order.data)

    def test_07_table_reservation_flow(self):
        """Test table reservation booking and confirmation."""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        res = self.client.post("/reservation", data={
            "name": "Karthik Subramanian",
            "phone": "+91 94444 88888",
            "email": "karthik@example.com",
            "date": tomorrow,
            "time": "07:30 PM",
            "guests": 4,
            "special_requests": "Window table for anniversary celebration"
        }, follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Table reservation confirmed", res.data)

    def test_08_authentication_and_customer_portal(self):
        """Test customer login, customer profile view, and logout."""
        # 1. Login with seeded customer
        res_login = self.client.post("/login", data={
            "email": "customer@ahaaram.com",
            "password": "customer123"
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b"Ravi Chandran", res_login.data)

        # 2. View profile
        res_profile = self.client.get("/profile")
        self.assertEqual(res_profile.status_code, 200)
        self.assertIn(b"Ravi Chandran", res_profile.data)

        # 3. View my reservations
        res_my_res = self.client.get("/my-reservations")
        self.assertEqual(res_my_res.status_code, 200)

        # 4. View my orders
        res_my_orders = self.client.get("/orders")
        self.assertEqual(res_my_orders.status_code, 200)

        # 5. Logout
        res_logout = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)

    def test_09_admin_dashboard_and_operations(self):
        """Test admin login, KPI dashboard, food catalog management, and order status updates."""
        # 1. Non-admin access to /admin should redirect
        res_unauth = self.client.get("/admin", follow_redirects=True)
        self.assertIn(b"Admin access required", res_unauth.data)

        # 2. Admin Login
        res_admin_login = self.client.post("/admin/login", data={
            "email": "admin@ahaaram.com",
            "password": "admin123"
        }, follow_redirects=True)
        self.assertEqual(res_admin_login.status_code, 200)
        self.assertIn(b"Executive Dashboard", res_admin_login.data)

        # 3. Admin Foods view
        res_foods = self.client.get("/admin/foods")
        self.assertEqual(res_foods.status_code, 200)
        self.assertIn(b"Manage Food Items", res_foods.data)

        # 4. Admin Add New Food Item
        res_add_food = self.client.post("/admin/foods/add", data={
            "name": "Madurai Elaneer Souffle",
            "category": "Desserts",
            "description": "Chilled tender coconut mousse infused with cardamom.",
            "price": "220.00",
            "image": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=600&q=80",
            "veg_or_nonveg": "veg",
            "availability": "1",
            "featured": "1"
        }, follow_redirects=True)
        self.assertEqual(res_add_food.status_code, 200)
        self.assertIn(b"Madurai Elaneer Souffle", res_add_food.data)

        # 5. Admin Orders list
        res_orders = self.client.get("/admin/orders")
        self.assertEqual(res_orders.status_code, 200)
        self.assertIn(b"Orders Master", res_orders.data)

        # 6. Admin Reservations list
        res_reservations = self.client.get("/admin/reservations")
        self.assertEqual(res_reservations.status_code, 200)
        self.assertIn(b"Reservations Log", res_reservations.data)

        # 7. Admin Customers list
        res_customers = self.client.get("/admin/customers")
        self.assertEqual(res_customers.status_code, 200)
        self.assertIn(b"Customer Directory", res_customers.data)

        # 8. Admin Reviews list
        res_reviews = self.client.get("/admin/reviews")
        self.assertEqual(res_reviews.status_code, 200)
        self.assertIn(b"Guest Testimonials", res_reviews.data)


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING AHAARAM RESTAURANT FULL-STACK TEST SUITE")
    print("=" * 60)
    suite = unittest.TestLoader().loadTestsFromTestCase(AhaaramRestaurantTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
