"""
Database schema definition and seed data for Ahaaram Multi Cuisine Restaurant.
Contains 50 diverse food items across 10 multi-cuisine categories,
default admin and demo customer credentials, sample reviews and reservations.
Note: Unverified menu items and sample reviews are provided as clearly marked demo data.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'restaurant.db')

CATEGORIES = [
    {
        "name": "South Indian",
        "slug": "south-indian",
        "description": "Authentic regional delicacies of Tamil Nadu, Madurai specialties, and fragrant spiced classics.",
        "image": "https://images.unsplash.com/photo-1610192244261-3f33de3f55e4?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "North Indian",
        "slug": "north-indian",
        "description": "Rich gravies, slow-cooked dal, aromatic gravies, and sizzling clay-oven tandoor delights.",
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Asian",
        "slug": "asian",
        "description": "Wok-tossed noodles, vibrant stir-fries, and fragrant oriental specialities.",
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Continental",
        "slug": "continental",
        "description": "Delicately grilled meats, rich creamy pastas, herb-infused risottos, and garden salads.",
        "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Starters",
        "slug": "starters",
        "description": "Crisp appetizers, spicy meat chukkas, crunchy fritters, and palate-awakening bites.",
        "image": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Main Course",
        "slug": "main-course",
        "description": "Substantial curries, comforting gravies, and chef-curated signature platters.",
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Breads",
        "slug": "breads",
        "description": "Flaky layered parottas, butter-brushed tandoori naans, and hot puffed rotis.",
        "image": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Rice & Biryani",
        "slug": "rice-biryani",
        "description": "Traditional Seeraga Samba dum biryanis, fragrantly spiced pulaos, and tempered rice bowls.",
        "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Desserts",
        "slug": "desserts",
        "description": "Madurai's legendary chilled sweets, decadent payasams, and warm artisanal confections.",
        "image": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=800&q=80"
    },
    {
        "name": "Beverages",
        "slug": "beverages",
        "description": "Frothy degree filter coffees, iced coolers, spiced lassis, and fresh tropical infusions.",
        "image": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=800&q=80"
    }
]

# 50 complete food items with high quality imagery
FOOD_ITEMS = [
    # 1-5: South Indian
    {
        "name": "Madurai Kari Dosa (Mutton)",
        "category": "South Indian",
        "description": "Iconic three-layered crispy dosa topped with egg omelette and tender minced spicy mutton chukka. (Demo Specialty)",
        "price": 340.0,
        "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 1
    },
    {
        "name": "Ghee Podi Thattu Idli",
        "category": "South Indian",
        "description": "Steamed fluffy rice cakes soaked in golden aromatic cow ghee and coarse roasted lentil gunpowder spice.",
        "price": 160.0,
        "image": "https://images.unsplash.com/photo-1589301760014-d929f3979dbc?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Madurai Bun Parotta with Salna",
        "category": "South Indian",
        "description": "Legendary flaky, pillowy, deep-tossed golden parotta served with piping hot spiced street-style gravy.",
        "price": 190.0,
        "image": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 1
    },
    {
        "name": "Chettinad Kozhi Varuval",
        "category": "South Indian",
        "description": "Country chicken pan-roasted dry with freshly pounded peppercorns, shallots, curry leaves, and fennel.",
        "price": 360.0,
        "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 1
    },
    {
        "name": "Meen Pollichathu",
        "category": "South Indian",
        "description": "Fresh sea bass marinated in shallot-chilli masala, wrapped in tender banana leaves and slow griddled.",
        "price": 440.0,
        "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },

    # 6-10: North Indian
    {
        "name": "Murgh Makhani (Butter Chicken)",
        "category": "North Indian",
        "description": "Tandoor-charred pulled chicken simmered in a velvety satin sauce of vine-ripened tomatoes, butter, and kasuri methi.",
        "price": 390.0,
        "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 1
    },
    {
        "name": "Dal Makhani Grand Regency",
        "category": "North Indian",
        "description": "Whole black urad lentils and kidney beans slow-simmered overnight over smoldering tandoor embers with butter.",
        "price": 280.0,
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Paneer Tikka Angara",
        "category": "North Indian",
        "description": "Malai cottage cheese cubes marinated in smoked hung curd, carom seeds, and Kashmiri degi mirch, skewered in clay tandoor.",
        "price": 310.0,
        "image": "https://images.unsplash.com/photo-1567184109411-b28f2baf63b2?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Awadhi Mutton Rogan Josh",
        "category": "North Indian",
        "description": "Slow-braised tender goat shank cooked with Kashmiri chili, ratan jot, dry ginger, and aromatic garam spices.",
        "price": 450.0,
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Pindi Chole Rawalpindi Style",
        "category": "North Indian",
        "description": "Dark and tangy chickpeas cooked with dried pomegranate seeds, amchur, black tea infusion, and green chilies.",
        "price": 250.0,
        "image": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },

    # 11-15: Asian
    {
        "name": "Dim Sum Steamed Basket",
        "category": "Asian",
        "description": "Handmade translucent crystal parcels filled with water chestnuts, shiitake mushrooms, and fresh garden vegetables.",
        "price": 320.0,
        "image": "https://images.unsplash.com/photo-1496116218417-1a781b1c416c?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Wok Schezwan Jumbo Prawns",
        "category": "Asian",
        "description": "Succulent coastal prawns tossed vigorously in a fierce wok with crushed Sichuan peppercorns, scallions, and peppers.",
        "price": 480.0,
        "image": "https://images.unsplash.com/photo-1559742811-822873691df8?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 1
    },
    {
        "name": "Chilli Garlic Hakka Noodles",
        "category": "Asian",
        "description": "Al-dente wok noodles tossed with charred garlic cloves, crunchy shredded cabbage, capsicum, and house chili oil.",
        "price": 240.0,
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Thai Green Chicken Curry",
        "category": "Asian",
        "description": "Fragrant coconut milk emulsion infused with fresh galangal, lemongrass, kaffir lime, and tender chicken morsels.",
        "price": 410.0,
        "image": "https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Crispy Dragon Chicken",
        "category": "Asian",
        "description": "Thin strips of golden fried chicken glazed in sweet honey-chili sauce, toasted sesame, and fried cashews.",
        "price": 330.0,
        "image": "https://images.unsplash.com/photo-1525755662778-989d0524087e?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },

    # 16-20: Continental
    {
        "name": "Herb-Crusted Grilled Salmon",
        "category": "Continental",
        "description": "Atlantic salmon fillet seared with parsley herb crust, served with garlic mashed potato and lemon caper emulsion.",
        "price": 620.0,
        "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 1
    },
    {
        "name": "Wild Mushroom & Truffle Risotto",
        "category": "Continental",
        "description": "Creamy Italian arborio rice simmered with porcini stock, sautéed button mushrooms, parmesan, and white truffle essence.",
        "price": 380.0,
        "image": "https://images.unsplash.com/photo-1633964913295-ceb43826e7c9?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Penne all'Arrabbiata with Burrata",
        "category": "Continental",
        "description": "Rigged penne pasta tossed in fiery crushed tomato sauce, fresh basil, extra virgin olive oil, and creamy fresh burrata.",
        "price": 350.0,
        "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Rosemary Garlic Roast Chicken",
        "category": "Continental",
        "description": "Corn-fed chicken breast roasted with fresh garden rosemary, butter-glazed baby vegetables, and rich red jus.",
        "price": 420.0,
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Ahaaram Garden Caesar Salad",
        "category": "Continental",
        "description": "Crisp romaine hearts, toasted herb brioche croutons, aged parmesan shavings, and house emulsion dressing.",
        "price": 260.0,
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },

    # 21-25: Starters
    {
        "name": "Madurai Mutton Kola Urundai",
        "category": "Starters",
        "description": "Crispy fried golden spiced minced mutton spheres with roasted gram flour and stone-ground Chettinad spices.",
        "price": 340.0,
        "image": "https://images.unsplash.com/photo-1541544741938-0af808871cc0?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Crispy Honey Chilli Lotus Stem",
        "category": "Starters",
        "description": "Thin-sliced crunchy lotus stems tossed with toasted sesame, scallions, dry red chili flakes, and raw hill honey.",
        "price": 270.0,
        "image": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Amritsari Ajwaini Fish Tikka",
        "category": "Starters",
        "description": "Boneless river fish cubes marinated in roasted carom seed flour, lemon juice, ginger-garlic, and flash-charred.",
        "price": 380.0,
        "image": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Bharwan Tandoori Khumb (Mushroom)",
        "category": "Starters",
        "description": "Button mushroom caps stuffed with spiced paneer and bell peppers, coated in smoked mustard yogurt.",
        "price": 290.0,
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Kongu Nattu Kozhi Sukka",
        "category": "Starters",
        "description": "Country chicken dry fry prepared with small country onions, pounded green peppercorns, and fresh curry leaves.",
        "price": 350.0,
        "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },

    # 26-30: Main Course
    {
        "name": "Malabar Fish Curry with Kokum",
        "category": "Main Course",
        "description": "Fresh catch simmered in rich coconut milk, infused with sun-dried Malabar kokum, fenugreek, and mustard seeds.",
        "price": 430.0,
        "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Paneer Lababdar",
        "category": "Main Course",
        "description": "Soft cottage cheese chunks and grated paneer in a rich onion-tomato gravy with melon seeds and fresh coriander.",
        "price": 310.0,
        "image": "https://images.unsplash.com/photo-1567184109411-b28f2baf63b2?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Madurai Milagu Mutton Curry",
        "category": "Main Course",
        "description": "Traditional thick mutton curry enriched with coarse black pepper, shallots, and fragrant coconut paste.",
        "price": 460.0,
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Vegetable Chettinad Kurma",
        "category": "Main Course",
        "description": "Assorted garden vegetables in an authentic Chettinad masala gravy of star anise, stone flower, and poppy seeds.",
        "price": 260.0,
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Dhaba Style Kadhai Chicken",
        "category": "Main Course",
        "description": "Chicken pieces tossed in an iron kadhai with crushed coriander seeds, chunky bell peppers, and coarse dry chili.",
        "price": 370.0,
        "image": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },

    # 31-35: Breads
    {
        "name": "Garlic Butter Naan",
        "category": "Breads",
        "description": "Refined flour dough slapped against clay tandoor walls, baked golden and brushed with minced garlic and melted butter.",
        "price": 75.0,
        "image": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Malabar Flaky Coin Parotta (2 pcs)",
        "category": "Breads",
        "description": "Crisp multi-layered Kerala style parottas beaten by hand to fluffy perfection with butter.",
        "price": 90.0,
        "image": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Cheese Chilli Kulcha",
        "category": "Breads",
        "description": "Tandoor baked leavened bread stuffed with melted mozzarella, cheddar, and finely chopped green bird-eye chilies.",
        "price": 120.0,
        "image": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Tandoori Whole Wheat Roti (Butter)",
        "category": "Breads",
        "description": "Traditional stone-ground whole wheat flatbread baked crisp in the clay oven and glazed with butter.",
        "price": 45.0,
        "image": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Ajwain Laccha Paratha",
        "category": "Breads",
        "description": "Multi-layered flaky whole wheat bread delicately perfumed with crushed carom seeds and desi ghee.",
        "price": 70.0,
        "image": "https://images.unsplash.com/photo-1626074353765-517a681e40be?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },

    # 36-40: Rice & Biryani
    {
        "name": "Madurai Mutton Seeraga Samba Biryani",
        "category": "Rice & Biryani",
        "description": "Ahaaram's pride: tiny aromatic Seeraga Samba short-grain rice cooked on dum with tender young mutton, mint, and pure ghee.",
        "price": 420.0,
        "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 1
    },
    {
        "name": "Chettinad Kozhi Biryani",
        "category": "Rice & Biryani",
        "description": "Fragrant Seeraga Samba rice infused with spiced chicken, shallots, and roasted Chettinad spices, served with onion raita.",
        "price": 350.0,
        "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "nonveg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Awadhi Subz Dum Biryani",
        "category": "Rice & Biryani",
        "description": "Aged royal basmati rice layered with seasoned seasonal vegetables, golden fried onions, saffron milk, and kewra.",
        "price": 280.0,
        "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Tempered Curd Rice (Madurai Style)",
        "category": "Rice & Biryani",
        "description": "Creamy soft mashed rice blended with set yogurt, mustard seeds, green chilies, ginger, and crispy pomegranate pearls.",
        "price": 170.0,
        "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Ghee Roasted Jeera Pulao",
        "category": "Rice & Biryani",
        "description": "Long-grain basmati rice gently tempered in desi ghee with roasted cumin seeds and fresh green coriander leaves.",
        "price": 210.0,
        "image": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },

    # 41-45: Desserts
    {
        "name": "Madurai Famous Jigarthanda Special",
        "category": "Desserts",
        "description": "The timeless Madurai royal drink-dessert made with badam pisin (almond gum), nannari syrup, reduced milk, and ice cream.",
        "price": 150.0,
        "image": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 1
    },
    {
        "name": "Elaneer Payasam (Tender Coconut)",
        "category": "Desserts",
        "description": "Silky chilled dessert made with fresh tender coconut flesh, condensed milk, and green cardamom essence.",
        "price": 180.0,
        "image": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Gulab Jamun with Malai Rabri",
        "category": "Desserts",
        "description": "Warm khoya dumplings fried golden, soaked in rose syrup, paired with thick slow-churned chilled rabri.",
        "price": 190.0,
        "image": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Royal Shahi Tukda",
        "category": "Desserts",
        "description": "Crisp ghee-fried bread triangles drenched in saffron sugar syrup and topped with pistachios, almonds, and silver vark.",
        "price": 210.0,
        "image": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Sizzling Dark Chocolate Brownie",
        "category": "Desserts",
        "description": "Warm walnut brownie served on a sizzling hot cast iron skillet with vanilla bean gelato and hot chocolate sauce.",
        "price": 240.0,
        "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },

    # 46-50: Beverages
    {
        "name": "Kumbakonam Degree Filter Coffee",
        "category": "Beverages",
        "description": "Traditional South Indian chicory blend brewed in brass filters, frothed high with thick boiling dairy milk.",
        "price": 95.0,
        "image": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Madurai Spiced Buttermilk (Neer Mor)",
        "category": "Beverages",
        "description": "Refreshing churned curd tempered with ginger, green chilies, asafoetida, curry leaves, and rock salt.",
        "price": 85.0,
        "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Alphonso Mango Saffron Lassi",
        "category": "Beverages",
        "description": "Thick rich yogurt shake whipped with Ratnagiri Alphonso mango pulp, saffron strands, and crushed pistachios.",
        "price": 140.0,
        "image": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Tender Coconut & Mint Cooler",
        "category": "Beverages",
        "description": "Sparkling fresh coconut water shaken with crushed garden mint leaves, lime juice, and sweet basil seeds.",
        "price": 130.0,
        "image": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    },
    {
        "name": "Masala Chai Pot",
        "category": "Beverages",
        "description": "Assam black tea leaves boiled with crushed green cardamom, ginger root, cloves, and cinnamon sticks.",
        "price": 90.0,
        "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=700&q=80",
        "veg_or_nonveg": "veg",
        "availability": 1,
        "featured": 0
    }
]

SAMPLE_REVIEWS = [
    {
        "customer_name": "R. Sundaram",
        "rating": 5,
        "review": "Ahaaram brings the true culinary spirit of Madurai along with fantastic multi-cuisine options. The Kari Dosa and Seeraga Samba Biryani were outstanding!",
        "is_approved": 1
    },
    {
        "customer_name": "Dr. Ananya Sharma",
        "rating": 5,
        "review": "Visited during our stay at Regency Madurai. Elegant ambience, welcoming hospitality, and the continental salmon was prepared to perfection.",
        "is_approved": 1
    },
    {
        "customer_name": "Karthik Subramanian",
        "rating": 4,
        "review": "The authentic Madurai Bun Parotta with spicy salna is a must-try. Finished our meal with the iconic Jigarthanda. Highly recommended for family dining.",
        "is_approved": 1
    },
    {
        "customer_name": "Elena Rostova",
        "rating": 5,
        "review": "Remarkable blend of Indian flavours and international comfort dishes. Warm staff and beautiful lighting. Best dining experience in Madakulam!",
        "is_approved": 1
    }
]


def init_database():
    """Initializes tables and populates seed data if empty."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 2. Categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            description TEXT,
            image TEXT
        );
    """)

    # 3. Foods table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image TEXT NOT NULL,
            veg_or_nonveg TEXT NOT NULL,
            availability INTEGER DEFAULT 1,
            featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 4. Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            dining_type TEXT NOT NULL,
            delivery_address TEXT,
            special_instructions TEXT,
            subtotal REAL NOT NULL,
            tax REAL NOT NULL,
            delivery_fee REAL NOT NULL,
            grand_total REAL NOT NULL,
            payment_method TEXT DEFAULT 'Cash / Demo Payment',
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    """)

    # 5. Order items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            food_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (food_id) REFERENCES foods (id)
        );
    """)

    # 6. Reservations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_code TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            guests INTEGER NOT NULL,
            special_requests TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    """)

    # 7. Favorites table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            food_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, food_id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (food_id) REFERENCES foods (id)
        );
    """)

    # 8. Reviews table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            customer_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review TEXT NOT NULL,
            is_approved INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    """)

    # Seed Admin and Demo Customer if not existing
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        admin_pass = generate_password_hash("admin123")
        customer_pass = generate_password_hash("customer123")
        guest_pass = generate_password_hash("guest123")
        cursor.execute("""
            INSERT INTO users (name, email, phone, password_hash, is_admin)
            VALUES (?, ?, ?, ?, ?)
        """, ("Ahaaram Restaurant Admin", "admin@ahaaram.com", "+91 452 237 1155", admin_pass, 1))

        cursor.execute("""
            INSERT INTO users (name, email, phone, password_hash, is_admin)
            VALUES (?, ?, ?, ?, ?)
        """, ("Ravi Chandran", "customer@ahaaram.com", "+91 98401 23456", customer_pass, 0))

        cursor.execute("""
            INSERT INTO users (name, email, phone, password_hash, is_admin)
            VALUES (?, ?, ?, ?, ?)
        """, ("Anand Raghavan", "guest@ahaaram.com", "+91 98765 43210", guest_pass, 0))

    # Seed Categories
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        for cat in CATEGORIES:
            cursor.execute("""
                INSERT INTO categories (name, slug, description, image)
                VALUES (?, ?, ?, ?)
            """, (cat["name"], cat["slug"], cat["description"], cat["image"]))

    # Seed 50 Food items
    cursor.execute("SELECT COUNT(*) FROM foods")
    if cursor.fetchone()[0] == 0:
        for item in FOOD_ITEMS:
            cursor.execute("""
                INSERT INTO foods (name, category, description, price, image, veg_or_nonveg, availability, featured)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["name"],
                item["category"],
                item["description"],
                item["price"],
                item["image"],
                item["veg_or_nonveg"],
                item["availability"],
                item["featured"]
            ))

    # Seed initial reviews
    cursor.execute("SELECT COUNT(*) FROM reviews")
    if cursor.fetchone()[0] == 0:
        for rev in SAMPLE_REVIEWS:
            cursor.execute("""
                INSERT INTO reviews (customer_name, rating, review, is_approved)
                VALUES (?, ?, ?, ?)
            """, (rev["customer_name"], rev["rating"], rev["review"], rev["is_approved"]))

    # Seed initial demo reservations
    cursor.execute("SELECT COUNT(*) FROM reservations")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO reservations (reservation_code, user_id, name, phone, email, date, time, guests, special_requests, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "RES-2026-1001",
            2,
            "Ravi Chandran",
            "+91 98401 23456",
            "customer@ahaaram.com",
            "2026-09-20",
            "19:30",
            4,
            "Window table with garden view for family anniversary.",
            "Confirmed"
        ))

    # Seed initial demo order
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO orders (order_number, user_id, customer_name, customer_phone, customer_email, dining_type, delivery_address, subtotal, tax, delivery_fee, grand_total, payment_method, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "AHR-2026-8001",
            2,
            "Ravi Chandran",
            "+91 98401 23456",
            "customer@ahaaram.com",
            "delivery",
            "Flat 4B, Meenakshi Towers, Madakulam Main Road, Madurai - 625003",
            820.0,
            41.0,
            0.0,
            861.0,
            "Cash / Demo Payment",
            "Completed"
        ))
        order_id = cursor.lastrowid
        cursor.execute("""
            INSERT INTO order_items (order_id, food_id, food_name, price, quantity, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, 1, "Madurai Kari Dosa (Mutton)", 340.0, 1, 340.0))
        cursor.execute("""
            INSERT INTO order_items (order_id, food_id, food_name, price, quantity, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, 36, "Madurai Mutton Seeraga Samba Biryani", 420.0, 1, 420.0))
        cursor.execute("""
            INSERT INTO order_items (order_id, food_id, food_name, price, quantity, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order_id, 46, "Kumbakonam Degree Filter Coffee", 60.0, 1, 60.0))

    conn.commit()
    conn.close()
    print("Database initialized successfully with 50 food items and seed data.")

if __name__ == "__main__":
    init_database()
