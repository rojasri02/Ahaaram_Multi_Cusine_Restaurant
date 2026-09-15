import os
import sqlite3
import random
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify, g, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

# Import seed script for automatic first-time schema setup
from database.seed_data import init_database, DB_PATH

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "ahaaram-luxury-hospitality-madurai-2026-secret")

# Ensure database exists and is populated on startup
init_database()


def get_db():
    """Opens a database connection if not already open in context."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Closes database connection at the end of the request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """Convenience helper to run SQL queries and return dict rows."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=()):
    """Helper to execute INSERT/UPDATE/DELETE and commit."""
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id


def current_user():
    """Returns currently authenticated user from session if valid."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)


@app.context_processor
def inject_global_vars():
    """Injects user state and cart counts into all Jinja templates."""
    user = current_user()
    cart = session.get("cart", {})
    cart_count = sum(item["quantity"] for item in cart.values())
    return {
        "current_user": user,
        "cart_count": cart_count,
        "now": datetime.now()
    }


def login_required(f):
    """Decorator to enforce customer login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please sign in to continue.", "info")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to enforce admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user()
        if not user or not user["is_admin"]:
            flash("Admin access required.", "error")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# PUBLIC WEBSITE ROUTES
# ==============================================================================

@app.route("/")
def index():
    """Home page with hero section, signature dishes, categories, and reviews."""
    signature_dishes = query_db(
        "SELECT * FROM foods WHERE featured = 1 AND availability = 1 LIMIT 6"
    )
    categories = query_db("SELECT * FROM categories ORDER BY id ASC")
    reviews = query_db(
        "SELECT * FROM reviews WHERE is_approved = 1 ORDER BY id DESC LIMIT 4"
    )
    return render_template(
        "index.html",
        signature_dishes=signature_dishes,
        categories=categories,
        reviews=reviews
    )


@app.route("/about")
def about():
    """About page: 'Where Madurai Meets the World'."""
    return render_template("about.html")


@app.route("/menu")
def menu():
    """Full menu page with search, filters (veg/nonveg, categories), and sorting."""
    search_query = request.args.get("search", "").strip()
    category_slug = request.args.get("category", "").strip()
    diet_filter = request.args.get("diet", "").strip()  # 'veg' or 'nonveg'
    sort_by = request.args.get("sort", "featured").strip()

    sql = "SELECT * FROM foods WHERE 1=1"
    params = []

    if search_query:
        sql += " AND (name LIKE ? OR description LIKE ? OR category LIKE ?)"
        wildcard = f"%{search_query}%"
        params.extend([wildcard, wildcard, wildcard])

    if category_slug and category_slug != "all":
        # Resolve category name
        cat = query_db("SELECT name FROM categories WHERE slug = ?", (category_slug,), one=True)
        if cat:
            sql += " AND category = ?"
            params.append(cat["name"])

    if diet_filter in ["veg", "nonveg"]:
        sql += " AND veg_or_nonveg = ?"
        params.append(diet_filter)

    if sort_by == "price_asc":
        sql += " ORDER BY price ASC"
    elif sort_by == "price_desc":
        sql += " ORDER BY price DESC"
    elif sort_by == "popular":
        sql += " ORDER BY id DESC"
    else:
        # Default featured first
        sql += " ORDER BY featured DESC, id ASC"

    foods = query_db(sql, params)
    categories = query_db("SELECT * FROM categories ORDER BY id ASC")

    # Get user favorites if logged in
    user = current_user()
    user_fav_ids = set()
    if user:
        fav_rows = query_db("SELECT food_id FROM favorites WHERE user_id = ?", (user["id"],))
        user_fav_ids = {row["food_id"] for row in fav_rows}

    return render_template(
        "menu.html",
        foods=foods,
        categories=categories,
        selected_category=category_slug,
        selected_diet=diet_filter,
        selected_sort=sort_by,
        search_query=search_query,
        user_fav_ids=user_fav_ids,
        total_items=len(foods)
    )


@app.route("/food/<int:id>")
def food_details(id):
    """Food item details page with quantity selector, related items, and reviews."""
    food = query_db("SELECT * FROM foods WHERE id = ?", (id,), one=True)
    if not food:
        abort(404)

    # Related items in same category
    related_foods = query_db(
        "SELECT * FROM foods WHERE category = ? AND id != ? LIMIT 4",
        (food["category"], id)
    )

    user = current_user()
    is_favorite = False
    if user:
        fav = query_db(
            "SELECT id FROM favorites WHERE user_id = ? AND food_id = ?",
            (user["id"], id),
            one=True
        )
        is_favorite = bool(fav)

    return render_template(
        "food_details.html",
        food=food,
        related_foods=related_foods,
        is_favorite=is_favorite
    )


@app.route("/gallery")
def gallery():
    """Gallery page showcasing restaurant ambience, food, dining, and desserts."""
    gallery_items = [
        {"url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=80", "category": "Restaurant", "title": "Grand Dining Hall"},
        {"url": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=80", "category": "Food", "title": "Traditional Awadhi Spices"},
        {"url": "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?auto=format&fit=crop&w=900&q=80", "category": "Ambience", "title": "Evening Table Setting"},
        {"url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=900&q=80", "category": "Food", "title": "Madurai Seeraga Samba Biryani"},
        {"url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=900&q=80", "category": "Restaurant", "title": "Intimate Booth Seating"},
        {"url": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=900&q=80", "category": "Desserts", "title": "Signature Jigarthanda"},
        {"url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=900&q=80", "category": "Beverages", "title": "Kumbakonam Degree Filter Coffee"},
        {"url": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=900&q=80", "category": "Food", "title": "Crisp Madurai Starters"},
        {"url": "https://images.unsplash.com/photo-1578474846511-04ba529f0b88?auto=format&fit=crop&w=900&q=80", "category": "Dining", "title": "Courtyard Dining Ambience"},
        {"url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80", "category": "Desserts", "title": "Sizzling Chocolate Brownie"},
        {"url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=80", "category": "Beverages", "title": "Tempered Madurai Neer Mor"},
        {"url": "https://images.unsplash.com/photo-1590846406792-0adc7f938f1d?auto=format&fit=crop&w=900&q=80", "category": "Ambience", "title": "Warm Evening Lighting"},
        {"url": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=900&q=80", "category": "Food", "title": "Continental Herb Salmon"},
        {"url": "https://images.unsplash.com/photo-1525610553991-2bede1a236e2?auto=format&fit=crop&w=900&q=80", "category": "Dining", "title": "Family Banquet Layout"},
        {"url": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=900&q=80", "category": "Food", "title": "Madurai Kari Dosa Live Counter"},
        {"url": "https://images.unsplash.com/photo-1559742811-822873691df8?auto=format&fit=crop&w=900&q=80", "category": "Food", "title": "Schezwan Wok Coastal Prawns"}
    ]
    return render_template("gallery.html", gallery_items=gallery_items)


@app.route("/dining")
def dining():
    """Dining Experience page detailing Breakfast, Lunch, Dinner, Family, and Business dining."""
    return render_template("dining.html")


@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    """Customer ratings and reviews page with submission form."""
    if request.method == "POST":
        user = current_user()
        if not user:
            flash("Please sign in to submit a review.", "warning")
            return redirect(url_for("login", next=url_for("reviews")))

        rating = int(request.form.get("rating", 5))
        review_text = request.form.get("review", "").strip()

        if not review_text:
            flash("Review text cannot be empty.", "error")
            return redirect(url_for("reviews"))

        execute_db(
            """
            INSERT INTO reviews (user_id, customer_name, rating, review, is_approved)
            VALUES (?, ?, ?, ?, 1)
            """,
            (user["id"], user["name"], rating, review_text)
        )
        flash("Thank you! Your review has been submitted successfully.", "success")
        return redirect(url_for("reviews"))

    all_reviews = query_db(
        "SELECT * FROM reviews WHERE is_approved = 1 ORDER BY id DESC"
    )
    return render_template("reviews.html", reviews=all_reviews)


@app.route("/contact")
def contact():
    """Location, opening hours, contact details, and directions."""
    return render_template("contact.html")


# ==============================================================================
# TABLE RESERVATION ROUTES
# ==============================================================================

@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    """Table reservation booking form."""
    user = current_user()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        date_str = (request.form.get("date") or request.form.get("reservation_date") or "").strip()
        time_str = (request.form.get("time") or request.form.get("reservation_time") or "").strip()
        guests = int(request.form.get("guests", 2))
        special_requests = request.form.get("special_requests", "").strip()

        # Validation
        if not (name and phone and email and date_str and time_str):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("reservation"))

        try:
            res_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if res_date < datetime.now().date():
                flash("Reservation date cannot be in the past.", "error")
                return redirect(url_for("reservation"))
        except ValueError:
            flash("Invalid date format provided.", "error")
            return redirect(url_for("reservation"))

        code = f"RES-2026-{random.randint(1000, 9999)}"
        user_id = user["id"] if user else None

        execute_db(
            """
            INSERT INTO reservations (reservation_code, user_id, name, phone, email, date, time, guests, special_requests, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
            """,
            (code, user_id, name, phone, email, date_str, time_str, guests, special_requests)
        )

        flash(f"Table reservation confirmed! Reference ID: {code}", "success")
        if user:
            return redirect(url_for("my_reservations"))
        return render_template(
            "reservation.html",
            success_code=code,
            res_details={
                "name": name,
                "date": date_str,
                "time": time_str,
                "guests": guests
            }
        )

    return render_template("reservation.html", user=user)


@app.route("/my-reservations")
@login_required
def my_reservations():
    """Logged in customer's list of reservations."""
    user = current_user()
    res_list = query_db(
        "SELECT * FROM reservations WHERE user_id = ? OR email = ? ORDER BY id DESC",
        (user["id"], user["email"])
    )
    return render_template("my_reservations.html", reservations=res_list)


@app.route("/reservation/cancel/<int:id>", methods=["POST"])
@login_required
def cancel_reservation(id):
    """Allows a customer to cancel their own reservation."""
    user = current_user()
    res = query_db("SELECT * FROM reservations WHERE id = ?", (id,), one=True)
    if res and (res["user_id"] == user["id"] or res["email"] == user["email"]):
        execute_db("UPDATE reservations SET status = 'Cancelled' WHERE id = ?", (id,))
        flash("Your reservation has been cancelled.", "info")
    else:
        flash("Reservation not found or unauthorized.", "error")
    return redirect(url_for("my_reservations"))


# ==============================================================================
# SHOPPING CART & CHECKOUT ROUTES
# ==============================================================================

def calculate_cart_totals(cart):
    """Calculates subtotal, 5% GST (2.5% CGST + 2.5% SGST), delivery fee and grand total."""
    subtotal = sum(item["price"] * item["quantity"] for item in cart.values())
    tax = round(subtotal * 0.05, 2)  # 5% restaurant GST in India
    delivery_fee = 40.0 if (subtotal > 0 and subtotal < 500.0) else 0.0
    grand_total = round(subtotal + tax + delivery_fee, 2)
    return {
        "subtotal": subtotal,
        "tax": tax,
        "delivery_fee": delivery_fee,
        "grand_total": grand_total
    }


@app.route("/cart")
def cart():
    """Customer shopping cart view."""
    cart_dict = session.get("cart", {})
    totals = calculate_cart_totals(cart_dict)
    return render_template("cart.html", cart=cart_dict, totals=totals)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    """Checkout page to place the order with demo payment option."""
    cart_dict = session.get("cart", {})
    if not cart_dict:
        flash("Your cart is empty. Please add items from our menu first.", "info")
        return redirect(url_for("menu"))

    user = current_user()
    totals = calculate_cart_totals(cart_dict)

    if request.method == "POST":
        customer_name = request.form.get("name", "").strip()
        customer_phone = request.form.get("phone", "").strip()
        customer_email = request.form.get("email", "").strip()
        dining_type = request.form.get("dining_type", "delivery")
        delivery_address = request.form.get("address", "").strip() if dining_type == "delivery" else "Dine-in / Takeaway Pickup"
        special_instructions = request.form.get("instructions", "").strip()

        if not (customer_name and customer_phone and customer_email):
            flash("Please fill in your name, phone number, and email.", "error")
            return redirect(url_for("checkout"))

        order_number = f"AHR-2026-{random.randint(1000, 9999)}"
        user_id = user["id"] if user else None

        order_id = execute_db(
            """
            INSERT INTO orders (
                order_number, user_id, customer_name, customer_phone, customer_email,
                dining_type, delivery_address, special_instructions,
                subtotal, tax, delivery_fee, grand_total, payment_method, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Cash / Demo Payment', 'Pending')
            """,
            (
                order_number, user_id, customer_name, customer_phone, customer_email,
                dining_type, delivery_address, special_instructions,
                totals["subtotal"], totals["tax"], totals["delivery_fee"], totals["grand_total"]
            )
        )

        # Insert order items
        for food_id_str, item in cart_dict.items():
            execute_db(
                """
                INSERT INTO order_items (order_id, food_id, food_name, price, quantity, total)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (order_id, int(food_id_str), item["name"], item["price"], item["quantity"], item["price"] * item["quantity"])
            )

        # Clear cart in session
        session["cart"] = {}
        session.modified = True

        flash("Order placed successfully!", "success")
        return redirect(url_for("order_success", order_number=order_number))

    return render_template("checkout.html", cart=cart_dict, totals=totals, user=user)


@app.route("/order-success/<order_number>")
def order_success(order_number):
    """Order confirmation receipt page."""
    order = query_db("SELECT * FROM orders WHERE order_number = ?", (order_number,), one=True)
    if not order:
        abort(404)
    items = query_db("SELECT * FROM order_items WHERE order_id = ?", (order["id"],))
    return render_template("order_success.html", order=order, items=items)


@app.route("/orders")
@login_required
def orders():
    """Customer view of past and active orders."""
    user = current_user()
    user_orders = query_db(
        "SELECT * FROM orders WHERE user_id = ? OR customer_email = ? ORDER BY id DESC",
        (user["id"], user["email"])
    )

    # Fetch items for each order
    orders_with_items = []
    for ord_row in user_orders:
        items = query_db("SELECT * FROM order_items WHERE order_id = ?", (ord_row["id"],))
        orders_with_items.append({"order": ord_row, "order_items": items})

    return render_template("orders.html", orders_with_items=orders_with_items)


# ==============================================================================
# AJAX / JSON CART & FAVORITES APIS
# ==============================================================================

@app.route("/api/cart/add", methods=["POST"])
def api_cart_add():
    """Adds an item to the shopping cart."""
    data = request.get_json() or {}
    food_id = str(data.get("food_id", ""))
    qty = int(data.get("quantity", 1))

    if not food_id:
        return jsonify({"success": False, "message": "Invalid food ID"}), 400

    food = query_db("SELECT * FROM foods WHERE id = ?", (int(food_id),), one=True)
    if not food:
        return jsonify({"success": False, "message": "Food item not found"}), 404

    cart = session.get("cart", {})
    if food_id in cart:
        cart[food_id]["quantity"] += qty
    else:
        cart[food_id] = {
            "id": food["id"],
            "name": food["name"],
            "price": float(food["price"]),
            "image": food["image"],
            "category": food["category"],
            "veg_or_nonveg": food["veg_or_nonveg"],
            "quantity": qty
        }

    session["cart"] = cart
    session.modified = True
    totals = calculate_cart_totals(cart)
    cart_count = sum(item["quantity"] for item in cart.values())

    return jsonify({
        "success": True,
        "message": f"'{food['name']}' added to cart",
        "cart_count": cart_count,
        "totals": totals
    })


@app.route("/api/cart/update", methods=["POST"])
def api_cart_update():
    """Increments, decrements, or removes an item in the cart."""
    data = request.get_json() or {}
    food_id = str(data.get("food_id", ""))
    action = data.get("action", "")

    cart = session.get("cart", {})
    if food_id in cart:
        if action == "inc":
            cart[food_id]["quantity"] += 1
        elif action == "dec":
            cart[food_id]["quantity"] -= 1
            if cart[food_id]["quantity"] <= 0:
                del cart[food_id]
        elif action == "remove":
            del cart[food_id]

    session["cart"] = cart
    session.modified = True
    totals = calculate_cart_totals(cart)
    cart_count = sum(item["quantity"] for item in cart.values())

    return jsonify({
        "success": True,
        "cart": cart,
        "cart_count": cart_count,
        "totals": totals
    })


@app.route("/api/cart/clear", methods=["POST"])
def api_cart_clear():
    """Clears all cart items."""
    session["cart"] = {}
    session.modified = True
    return jsonify({"success": True, "cart_count": 0, "totals": calculate_cart_totals({})})


@app.route("/api/favorites/toggle", methods=["POST"])
def api_favorites_toggle():
    """Adds or removes food item from user's favorites."""
    user = current_user()
    if not user:
        return jsonify({"success": False, "message": "Please sign in to save favorites."}), 401

    data = request.get_json() or {}
    food_id = data.get("food_id")
    if not food_id:
        return jsonify({"success": False, "message": "Invalid food ID"}), 400

    existing = query_db(
        "SELECT id FROM favorites WHERE user_id = ? AND food_id = ?",
        (user["id"], int(food_id)),
        one=True
    )
    if existing:
        execute_db("DELETE FROM favorites WHERE id = ?", (existing["id"],))
        return jsonify({"success": True, "favorited": False, "message": "Removed from favorites."})
    else:
        execute_db("INSERT INTO favorites (user_id, food_id) VALUES (?, ?)", (user["id"], int(food_id)))
        return jsonify({"success": True, "favorited": True, "message": "Added to favorites."})


# ==============================================================================
# AUTHENTICATION & USER PROFILE
# ==============================================================================

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration with secure password hashing."""
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not (name and email and phone and password):
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for("register"))

        existing = query_db("SELECT id FROM users WHERE email = ?", (email,), one=True)
        if existing:
            flash("An account with this email address already exists.", "error")
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)
        user_id = execute_db(
            "INSERT INTO users (name, email, phone, password_hash, is_admin) VALUES (?, ?, ?, ?, 0)",
            (name, email, phone, hashed)
        )
        session["user_id"] = user_id
        session["user_name"] = name
        session["is_admin"] = False
        flash("Welcome to Ahaaram! Your account has been created.", "success")
        return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User login authentication."""
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = query_db("SELECT * FROM users WHERE email = ?", (email,), one=True)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password. Please try again.", "error")
            return redirect(url_for("login"))

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["is_admin"] = bool(user["is_admin"])

        flash(f"Welcome back, {user['name']}!", "success")
        next_url = request.args.get("next")
        if next_url and next_url.startswith("/"):
            return redirect(next_url)
        return redirect(url_for("admin_dashboard" if user["is_admin"] else "profile"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Logs out user and clears active session."""
    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("is_admin", None)
    flash("You have been signed out.", "info")
    return redirect(url_for("index"))


@app.route("/profile")
@login_required
def profile():
    """Customer Dashboard showing profile, recent orders, reservations, and favorites."""
    user = current_user()
    recent_orders = query_db(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user["id"],)
    )
    reservations = query_db(
        "SELECT * FROM reservations WHERE user_id = ? ORDER BY id DESC LIMIT 5",
        (user["id"],)
    )
    favorites = query_db(
        """
        SELECT f.* FROM foods f
        JOIN favorites fav ON f.id = fav.food_id
        WHERE fav.user_id = ?
        """,
        (user["id"],)
    )
    reviews = query_db(
        "SELECT * FROM reviews WHERE user_id = ? ORDER BY id DESC",
        (user["id"],)
    )
    return render_template(
        "profile.html",
        user=user,
        recent_orders=recent_orders,
        reservations=reservations,
        favorites=favorites,
        reviews=reviews
    )


# ==============================================================================
# ADMIN DASHBOARD & MANAGEMENT ROUTES
# ==============================================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Direct admin login endpoint."""
    user = current_user()
    if user and user["is_admin"]:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = query_db("SELECT * FROM users WHERE email = ? AND is_admin = 1", (email,), one=True)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid administrator credentials.", "error")
            return redirect(url_for("admin_login"))

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        session["is_admin"] = True
        flash("Welcome to Ahaaram Administration Dashboard.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("login.html", is_admin_page=True)


@app.route("/admin")
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    """Admin Overview with vital statistics, metrics, and recent orders."""
    total_orders = query_db("SELECT COUNT(*) FROM orders", one=True)[0]
    pending_orders = query_db("SELECT COUNT(*) FROM orders WHERE status = 'Pending'", one=True)[0]
    completed_orders = query_db("SELECT COUNT(*) FROM orders WHERE status = 'Completed'", one=True)[0]
    total_revenue = query_db("SELECT COALESCE(SUM(grand_total), 0) FROM orders WHERE status != 'Cancelled'", one=True)[0]

    total_reservations = query_db("SELECT COUNT(*) FROM reservations", one=True)[0]
    pending_reservations = query_db("SELECT COUNT(*) FROM reservations WHERE status = 'Pending'", one=True)[0]
    total_customers = query_db("SELECT COUNT(*) FROM users WHERE is_admin = 0", one=True)[0]
    total_foods = query_db("SELECT COUNT(*) FROM foods", one=True)[0]

    recent_orders = query_db("SELECT * FROM orders ORDER BY id DESC LIMIT 6")
    recent_reservations = query_db("SELECT * FROM reservations ORDER BY id DESC LIMIT 6")

    stats = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_revenue": round(total_revenue, 2),
        "total_reservations": total_reservations,
        "pending_reservations": pending_reservations,
        "total_customers": total_customers,
        "total_foods": total_foods
    }

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        recent_orders=recent_orders,
        recent_reservations=recent_reservations
    )


@app.route("/admin/foods")
@admin_required
def admin_foods():
    """Admin Food items management list with category filtering."""
    category = request.args.get("category", "")
    if category:
        foods = query_db("SELECT * FROM foods WHERE category = ? ORDER BY id DESC", (category,))
    else:
        foods = query_db("SELECT * FROM foods ORDER BY id DESC")
    categories = query_db("SELECT * FROM categories ORDER BY name ASC")
    return render_template("admin/foods.html", foods=foods, categories=categories, selected_cat=category)


@app.route("/admin/foods/add", methods=["GET", "POST"])
@admin_required
def admin_add_food():
    """Form to add a new food item to the menu."""
    categories = query_db("SELECT * FROM categories ORDER BY name ASC")
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        price = float(request.form.get("price", 0))
        image = request.form.get("image", "").strip()
        veg_or_nonveg = request.form.get("veg_or_nonveg", "veg")
        availability = 1 if request.form.get("availability") else 0
        featured = 1 if request.form.get("featured") else 0

        if not (name and category and price > 0):
            flash("Please provide dish name, category, and valid price.", "error")
            return redirect(url_for("admin_add_food"))

        if not image:
            image = "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80"

        execute_db(
            """
            INSERT INTO foods (name, category, description, price, image, veg_or_nonveg, availability, featured)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (name, category, description, price, image, veg_or_nonveg, availability, featured)
        )
        flash(f"Food item '{name}' added successfully.", "success")
        return redirect(url_for("admin_foods"))

    return render_template("admin/add_food.html", categories=categories)


@app.route("/admin/foods/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_edit_food(id):
    """Form to edit an existing food item."""
    food = query_db("SELECT * FROM foods WHERE id = ?", (id,), one=True)
    if not food:
        abort(404)

    categories = query_db("SELECT * FROM categories ORDER BY name ASC")

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        price = float(request.form.get("price", 0))
        image = request.form.get("image", "").strip()
        veg_or_nonveg = request.form.get("veg_or_nonveg", "veg")
        availability = 1 if request.form.get("availability") else 0
        featured = 1 if request.form.get("featured") else 0

        execute_db(
            """
            UPDATE foods
            SET name = ?, category = ?, description = ?, price = ?, image = ?,
                veg_or_nonveg = ?, availability = ?, featured = ?
            WHERE id = ?
            """,
            (name, category, description, price, image, veg_or_nonveg, availability, featured, id)
        )
        flash(f"'{name}' updated successfully.", "success")
        return redirect(url_for("admin_foods"))

    return render_template("admin/edit_food.html", food=food, categories=categories)


@app.route("/admin/foods/delete/<int:id>", methods=["POST"])
@admin_required
def admin_delete_food(id):
    """Deletes a food item from the database."""
    food = query_db("SELECT name FROM foods WHERE id = ?", (id,), one=True)
    if food:
        execute_db("DELETE FROM foods WHERE id = ?", (id,))
        flash(f"Dish '{food['name']}' deleted.", "info")
    return redirect(url_for("admin_foods"))


@app.route("/admin/orders")
@admin_required
def admin_orders():
    """Admin Order management table with filter by status."""
    status_filter = request.args.get("status", "")
    if status_filter:
        orders_list = query_db("SELECT * FROM orders WHERE status = ? ORDER BY id DESC", (status_filter,))
    else:
        orders_list = query_db("SELECT * FROM orders ORDER BY id DESC")

    # Attach items to each order
    orders_data = []
    for ord_row in orders_list:
        items = query_db("SELECT * FROM order_items WHERE order_id = ?", (ord_row["id"],))
        orders_data.append({"order": ord_row, "order_items": items})

    return render_template("admin/orders.html", orders_data=orders_data, selected_status=status_filter)


@app.route("/admin/orders/update-status/<int:id>", methods=["POST"])
@admin_required
def admin_update_order_status(id):
    """Updates order status: Pending, Confirmed, Preparing, Ready, Completed, Cancelled."""
    new_status = request.form.get("status", "Pending")
    execute_db("UPDATE orders SET status = ? WHERE id = ?", (new_status, id))
    flash(f"Order #{id} status updated to {new_status}.", "success")
    return redirect(url_for("admin_orders"))


@app.route("/admin/reservations")
@admin_required
def admin_reservations():
    """Admin Table Reservation queue."""
    status_filter = request.args.get("status", "")
    if status_filter:
        res_list = query_db("SELECT * FROM reservations WHERE status = ? ORDER BY date ASC, time ASC", (status_filter,))
    else:
        res_list = query_db("SELECT * FROM reservations ORDER BY date DESC, time ASC")
    return render_template("admin/reservations.html", reservations=res_list, selected_status=status_filter)


@app.route("/admin/reservations/update-status/<int:id>", methods=["POST"])
@admin_required
def admin_update_reservation_status(id):
    """Updates table reservation status: Pending, Confirmed, Cancelled, Completed."""
    new_status = request.form.get("status", "Confirmed")
    execute_db("UPDATE reservations SET status = ? WHERE id = ?", (new_status, id))
    flash(f"Reservation #{id} status updated to {new_status}.", "success")
    return redirect(url_for("admin_reservations"))


@app.route("/admin/customers")
@admin_required
def admin_customers():
    """List of registered customers with statistics (order count and reservation count)."""
    customers = query_db("""
        SELECT u.id, u.name, u.email, u.phone, u.created_at,
               (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id) as order_count,
               (SELECT COUNT(*) FROM reservations r WHERE r.user_id = u.id) as reservation_count
        FROM users u
        WHERE u.is_admin = 0
        ORDER BY u.id DESC
    """)
    return render_template("admin/customers.html", customers=customers)


@app.route("/admin/reviews")
@admin_required
def admin_reviews():
    """Admin review moderation page."""
    reviews_list = query_db("SELECT * FROM reviews ORDER BY id DESC")
    return render_template("admin/reviews.html", reviews=reviews_list)


@app.route("/admin/reviews/delete/<int:id>", methods=["POST"])
@admin_required
def admin_delete_review(id):
    """Deletes inappropriate reviews."""
    execute_db("DELETE FROM reviews WHERE id = ?", (id,))
    flash("Review deleted successfully.", "info")
    return redirect(url_for("admin_reviews"))


# ==============================================================================
# ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Ahaaram Restaurant Web Application on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=True)
