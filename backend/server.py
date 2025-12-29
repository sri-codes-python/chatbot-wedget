from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.openai import LlmChat, UserMessage


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Emergent LLM Key
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# Curry Pizza House Complete Menu Data
MENU_DATA = """
================================================================================
                    CURRY PIZZA HOUSE - COMPLETE MENU
================================================================================

🏪 ABOUT US:
- Indian Fusion Pizza Restaurant
- All chicken and lamb are HALAL certified
- Only Vindaloo Pizza contains pork (NOT halal)
- NO BBQ sauce - we use authentic Indian curry sauces

================================================================================
🍗 WINGS MENU
================================================================================

### Tandoori Wings (Bone-In) - Our Signature!
Marinated in yogurt and tandoori spices, grilled to perfection
- 6 Wings: $8.99
- 12 Wings: $15.99
- 18 Wings: $22.99
- 24 Wings: $28.99
- Sauce Options: Mint Chutney, Mango Habanero, Tikka Masala Glaze
- Allergens: Dairy
- Halal: Yes

### Curry Chicken Wings (Bone-In)
Tossed in our signature curry sauce
- 6 Wings: $9.99
- 12 Wings: $17.99
- 18 Wings: $24.99
- 24 Wings: $31.99
- Sauce Options: Butter Chicken, Tikka Masala, Vindaloo (spicy)
- Allergens: Dairy
- Halal: Yes

### Boneless Wings / Chicken Bites
Crispy boneless chicken pieces with Indian spices
- 8 Pieces: $9.99
- 16 Pieces: $17.99
- 24 Pieces: $24.99
- Sauce Options: Any curry sauce
- Allergens: Dairy, Gluten
- Halal: Yes

================================================================================
🍕 CURRY CHICKEN PIZZAS (Non-Vegetarian)
================================================================================

### 1. Butter Chicken Pizza ⭐ BESTSELLER
Also known as: "Curry Chicken", "Butter Curry Pizza"
- Small (10"): $14.99 | Medium (12"): $18.99 | Large (14"): $22.99
- Sauce: Creamy Butter Chicken Curry (tomato-cream with cashews)
- Toppings: Tender chicken pieces, bell peppers, red onions, cilantro
- Cheese: Mozzarella blend
- Spice Level: Mild (can be made spicier on request)
- Allergens: Dairy, Gluten, Nuts (cashew)
- Halal: Yes ✓

### 2. Chicken Tikka Masala Pizza
Also known as: "Tikka Pizza", "Masala Chicken Pizza"
- Small (10"): $15.99 | Medium (12"): $19.99 | Large (14"): $23.99
- Sauce: Tikka Masala (spiced tomato-cream)
- Toppings: Chicken tikka pieces, roasted bell peppers, red onions
- Cheese: Fresh mozzarella
- Spice Level: Medium
- Allergens: Dairy, Gluten
- Halal: Yes ✓

### 3. Tandoori Chicken Pizza
Also known as: "Tandoori Pizza"
- Small (10"): $14.99 | Medium (12"): $18.99 | Large (14"): $22.99
- Sauce: Mint Chutney base with tandoori spices
- Toppings: Smoky tandoori chicken, red onions, jalapeños, cilantro
- Cheese: Mozzarella
- Spice Level: Medium-Hot 🌶️
- Allergens: Dairy, Gluten
- Halal: Yes ✓

### 4. Keema Pizza (Lamb) ⭐ HALAL LAMB
Also known as: "Lamb Pizza", "Minced Meat Pizza"
- Small (10"): $15.99 | Medium (12"): $19.99 | Large (14"): $23.99
- Sauce: Spiced Tomato Keema Sauce
- Toppings: Spiced minced lamb, green peas, onions, garam masala
- Cheese: Mozzarella
- Spice Level: Medium
- Allergens: Dairy, Gluten
- Halal: YES - Certified Halal Lamb ✓

### 5. Vindaloo Pizza 🔥🔥🔥 (VERY SPICY - Contains Pork)
- Small (10"): $15.99 | Medium (12"): $19.99 | Large (14"): $23.99
- Sauce: Vindaloo Curry (very spicy!)
- Toppings: Pork pieces, potatoes, hot chilies
- Cheese: Mozzarella
- Spice Level: EXTRA HOT 🔥🔥🔥
- Allergens: Dairy, Gluten
- Halal: NO ✗ (Contains Pork)

================================================================================
🥬 VEGETARIAN CURRY PIZZAS
================================================================================

### 6. Paneer Tikka Pizza 🌱
Also known as: "Paneer Pizza", "Cottage Cheese Pizza"
- Small (10"): $13.99 | Medium (12"): $17.99 | Large (14"): $21.99
- Sauce: Spiced Tomato Tikka Sauce
- Toppings: Marinated paneer cubes, bell peppers, onions, fresh herbs
- Cheese: Mozzarella + Paneer
- Spice Level: Medium
- Allergens: Dairy, Gluten
- Vegetarian: Yes ✓

### 7. Achari Gobhi Pizza 🌱 ⭐ MOST POPULAR VEGETARIAN
Also known as: "Cauliflower Pizza", "Pickle Pizza", "Gobhi Pizza"
- Small (10"): $12.99 | Medium (12"): $16.99 | Large (14"): $20.99
- Sauce: Achari (Pickle) Masala - tangy and spicy
- Toppings: Spiced cauliflower, green chilies, fresh coriander
- Cheese: Mozzarella (Vegan option: No cheese)
- Spice Level: Medium-Hot 🌶️
- Allergens: Gluten, Mustard
- Vegetarian: Yes ✓ | Vegan Option Available

### 8. Saag Paneer Pizza 🌱
Also known as: "Spinach Pizza", "Palak Paneer Pizza"
- Small (10"): $13.99 | Medium (12"): $17.99 | Large (14"): $21.99
- Sauce: Creamy Saag (Spinach) Sauce
- Toppings: Paneer cubes, garlic, Indian spices
- Cheese: Mozzarella + Paneer
- Spice Level: Mild
- Allergens: Dairy, Gluten
- Vegetarian: Yes ✓

### 9. Aloo Gobi Pizza 🌱
Also known as: "Potato Cauliflower Pizza"
- Small (10"): $11.99 | Medium (12"): $15.99 | Large (14"): $19.99
- Sauce: Turmeric-Cumin Spiced Sauce
- Toppings: Spiced potatoes, cauliflower, cumin seeds
- Cheese: Mozzarella
- Spice Level: Mild
- Allergens: Dairy, Gluten
- Vegetarian: Yes ✓

### 10. Chana Masala Pizza 🌱 (Vegan Available)
Also known as: "Chickpea Pizza"
- Small (10"): $12.99 | Medium (12"): $16.99 | Large (14"): $20.99
- Sauce: Chana Masala (spiced tomato)
- Toppings: Chickpeas, tomatoes, onions, cumin, coriander
- Cheese: Mozzarella (Vegan: No cheese)
- Spice Level: Medium
- Allergens: Gluten
- Vegetarian: Yes ✓ | Vegan Option Available

### 11. Malai Kofta Pizza 🌱
Also known as: "Kofta Pizza", "Veggie Balls Pizza"
- Small (10"): $14.99 | Medium (12"): $18.99 | Large (14"): $22.99
- Sauce: Malai (Cream) Tomato Sauce
- Toppings: Vegetable kofta balls, cream sauce
- Cheese: Mozzarella
- Spice Level: Mild
- Allergens: Dairy, Gluten, Nuts
- Vegetarian: Yes ✓

================================================================================
🥗 APPETIZERS & SIDES
================================================================================

### Samosas (Vegetable)
Crispy pastry filled with spiced potatoes and peas
- 2 Pieces: $4.99
- 4 Pieces: $8.99
- 6 Pieces: $12.99
- Served with: Mint & Tamarind Chutney
- Vegetarian: Yes | Allergens: Gluten

### Chicken Samosas
Crispy pastry filled with spiced chicken
- 2 Pieces: $5.99
- 4 Pieces: $10.99
- 6 Pieces: $14.99
- Served with: Mint & Tamarind Chutney
- Halal: Yes | Allergens: Gluten

### Garlic Naan Sticks
- Regular Order (4 sticks): $5.99
- Large Order (8 sticks): $10.99
- Served with: Curry dipping sauce
- Vegetarian: Yes | Allergens: Dairy, Gluten

### Paneer Pakora
Crispy fried paneer fritters
- 6 Pieces: $7.99
- 12 Pieces: $13.99
- Vegetarian: Yes | Allergens: Dairy, Gluten

### Onion Bhaji
Crispy onion fritters
- 6 Pieces: $5.99
- 12 Pieces: $10.99
- Vegetarian: Yes | Vegan: Yes | Allergens: Gluten

================================================================================
🥤 BEVERAGES
================================================================================

### Mango Lassi - $4.99
Sweet yogurt drink with mango | Allergens: Dairy

### Sweet Lassi - $3.99
Traditional sweet yogurt drink | Allergens: Dairy

### Salted Lassi - $3.99
Savory yogurt drink with cumin | Allergens: Dairy

### Masala Chai - $3.49
Spiced Indian tea with milk | Allergens: Dairy

### Soft Drinks - $2.49
Coke, Diet Coke, Sprite, Fanta

### Bottled Water - $1.99

================================================================================
🍨 DESSERTS
================================================================================

### Gulab Jamun (2 pieces) - $4.99
Sweet milk dumplings in rose syrup | Allergens: Dairy, Gluten

### Kheer (Rice Pudding) - $4.99
Creamy rice pudding with cardamom | Allergens: Dairy, Nuts

### Mango Kulfi - $5.99
Indian mango ice cream | Allergens: Dairy, Nuts

================================================================================
➕ EXTRAS & CUSTOMIZATIONS
================================================================================

- Extra Cheese: +$2.50
- Extra Meat/Paneer: +$3.50
- Gluten-Free Crust: +$3.00
- Dairy-Free Cheese: +$2.00
- Extra Spicy: FREE
- Side of Raita: $2.99
- Side of Chutney (Mint/Tamarind): $1.99

================================================================================
"""

# System message for the AI chatbot
SYSTEM_MESSAGE = f"""
You are a smart, helpful menu assistant for Curry Pizza House - an Indian fusion pizza restaurant.

=== YOUR KNOWLEDGE BASE ===
{MENU_DATA}

=== CRITICAL INSTRUCTIONS ===

1. **FUZZY MATCHING - UNDERSTAND PARTIAL NAMES:**
   - "curry chicken" or "chicken curry" → Suggest: Butter Chicken Pizza, Chicken Tikka Masala Pizza, Tandoori Chicken Pizza
   - "curry pizza" → Ask: "We have several curry pizzas! Are you looking for chicken curry (Butter Chicken, Tikka Masala), lamb curry (Keema), or vegetarian curry options?"
   - "veggie" or "veg" → Show all vegetarian options
   - "gobhi" or "gobi" → Achari Gobhi Pizza or Aloo Gobi Pizza
   - "paneer" → Paneer Tikka Pizza or Saag Paneer Pizza
   - "lamb" or "mutton" → Keema Pizza
   - "spicy" → Suggest Vindaloo (hottest), Tandoori, or Achari Gobhi

2. **ALWAYS ASK CLARIFYING QUESTIONS when query is ambiguous:**
   - If customer says "curry pizza" → "Which type of curry pizza? We have: 1) Butter Chicken 2) Tikka Masala 3) Tandoori Chicken 4) Vegetarian options like Paneer Tikka"
   - If customer says "chicken" → "Which chicken pizza? 1) Butter Chicken (mild, creamy) 2) Tikka Masala (medium spice) 3) Tandoori (smoky, spicy)"

3. **WINGS - ALWAYS SHOW QUANTITY PRICING:**
   When asked about wings, ALWAYS show:
   - Tandoori Wings: 6 for $8.99 | 12 for $15.99 | 18 for $22.99 | 24 for $28.99
   - Curry Wings: 6 for $9.99 | 12 for $17.99 | 18 for $24.99 | 24 for $31.99
   - Boneless: 8 for $9.99 | 16 for $17.99 | 24 for $24.99

4. **DETAILED RESPONSES - Always include:**
   - Full name of item
   - ALL prices (Small/Medium/Large or quantity options)
   - Key ingredients/toppings
   - Spice level
   - Allergens
   - Halal status for meat items
   - Vegan option if available

5. **NO BBQ SAUCE:**
   - We don't have BBQ sauce - explain we use Indian curry sauces instead
   - Suggest similar: "Instead of BBQ, try our Tandoori Wings or Butter Chicken Pizza!"

6. **HALAL QUERIES:**
   - All chicken = Halal ✓
   - Lamb (Keema) = Halal ✓
   - ONLY Vindaloo = NOT Halal (contains pork)

7. **RESPONSE FORMAT:**
   - Use bullet points for clarity
   - Bold important info like prices
   - Use emojis sparingly (🍕 🌶️ ⭐ 🌱)
   - Keep responses organized and scannable

=== EXAMPLE RESPONSES ===

**User: "wings"**
Response: "We have delicious Indian-style wings! 🍗

**Tandoori Wings** (Bone-In) - Our Signature!
• 6 Wings: $8.99
• 12 Wings: $15.99
• 18 Wings: $22.99
• 24 Wings: $28.99
Sauce options: Mint Chutney, Mango Habanero, Tikka Masala Glaze

**Curry Chicken Wings** (Bone-In)
• 6 Wings: $9.99
• 12 Wings: $17.99
• 18 Wings: $24.99
• 24 Wings: $31.99
Sauce options: Butter Chicken, Tikka Masala, Vindaloo

**Boneless Wings**
• 8 Pieces: $9.99
• 16 Pieces: $17.99
• 24 Pieces: $24.99

All wings are halal! Which would you like?"

**User: "curry chicken"**
Response: "We have 3 curry chicken pizzas! Which sounds good?

1. **Butter Chicken Pizza** ⭐ Bestseller
   - Creamy, mild curry sauce with tender chicken
   - Small $14.99 | Medium $18.99 | Large $22.99

2. **Chicken Tikka Masala Pizza**
   - Spiced tomato-cream sauce, medium heat
   - Small $15.99 | Medium $19.99 | Large $23.99

3. **Tandoori Chicken Pizza**
   - Smoky tandoori chicken with mint chutney
   - Small $14.99 | Medium $18.99 | Large $22.99

All are halal! Would you like more details on any of these?"

**User: "is lamb halal"**
Response: "Yes! Our **Keema Pizza** uses certified halal lamb. 🍕

**Keema Pizza Details:**
• Small (10"): $15.99
• Medium (12"): $19.99
• Large (14"): $23.99
• Toppings: Spiced minced lamb, green peas, onions, garam masala
• Spice Level: Medium
• Halal: YES ✓ - Certified Halal Lamb

Would you like to order one?"

Remember: Be helpful, precise, and always provide complete pricing information!
"""

# Chat session storage (in-memory for simplicity, could be moved to MongoDB)
chat_sessions = {}


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    timestamp: datetime


# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Welcome to Curry Pizza House API!"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    return status_checks


@api_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages with AI-powered responses"""
    try:
        # Generate or use existing session ID
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get or create chat instance for this session
        if session_id not in chat_sessions:
            if not EMERGENT_LLM_KEY:
                raise HTTPException(status_code=500, detail="LLM API key not configured")
            
            chat_instance = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=session_id,
                system_message=SYSTEM_MESSAGE
            ).with_model("openai", "gpt-4o-mini").with_params(temperature=0.7, max_tokens=800)
            
            chat_sessions[session_id] = chat_instance
        else:
            chat_instance = chat_sessions[session_id]
        
        # Send message and get response
        user_msg = UserMessage(text=request.message)
        response_text = await chat_instance.send_message(user_msg)
        
        # Store conversation in MongoDB for persistence
        conversation_doc = {
            "session_id": session_id,
            "user_message": request.message,
            "assistant_response": response_text,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await db.chat_conversations.insert_one(conversation_doc)
        
        return ChatResponse(
            session_id=session_id,
            response=response_text,
            timestamp=datetime.now(timezone.utc)
        )
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@api_router.get("/menu")
async def get_menu():
    """Return the menu data as structured JSON"""
    return {
        "wings": [
            {
                "name": "Tandoori Wings (Bone-In)",
                "description": "Marinated in yogurt and tandoori spices",
                "prices": {"6pc": 8.99, "12pc": 15.99, "18pc": 22.99, "24pc": 28.99},
                "halal": True
            },
            {
                "name": "Curry Chicken Wings (Bone-In)",
                "description": "Tossed in signature curry sauce",
                "prices": {"6pc": 9.99, "12pc": 17.99, "18pc": 24.99, "24pc": 31.99},
                "halal": True
            },
            {
                "name": "Boneless Wings",
                "description": "Crispy boneless chicken pieces",
                "prices": {"8pc": 9.99, "16pc": 17.99, "24pc": 24.99},
                "halal": True
            }
        ],
        "curry_chicken_pizzas": [
            {
                "name": "Butter Chicken Pizza",
                "prices": {"small": 14.99, "medium": 18.99, "large": 22.99},
                "description": "Creamy butter chicken curry sauce with tender chicken",
                "spice_level": "Mild",
                "halal": True,
                "popular": True
            },
            {
                "name": "Chicken Tikka Masala Pizza",
                "prices": {"small": 15.99, "medium": 19.99, "large": 23.99},
                "description": "Spiced chicken tikka with tomato masala sauce",
                "spice_level": "Medium",
                "halal": True
            },
            {
                "name": "Tandoori Chicken Pizza",
                "prices": {"small": 14.99, "medium": 18.99, "large": 22.99},
                "description": "Smoky tandoori chicken with mint chutney",
                "spice_level": "Medium-Hot",
                "halal": True
            },
            {
                "name": "Keema Pizza (Lamb)",
                "prices": {"small": 15.99, "medium": 19.99, "large": 23.99},
                "description": "Spiced minced halal lamb with peas",
                "spice_level": "Medium",
                "halal": True
            },
            {
                "name": "Vindaloo Pizza",
                "prices": {"small": 15.99, "medium": 19.99, "large": 23.99},
                "description": "Fiery vindaloo pork - very spicy!",
                "spice_level": "Extra Hot",
                "halal": False,
                "contains_pork": True
            }
        ],
        "vegetarian_pizzas": [
            {
                "name": "Paneer Tikka Pizza",
                "prices": {"small": 13.99, "medium": 17.99, "large": 21.99},
                "description": "Marinated paneer cubes with spiced tomato sauce",
                "vegetarian": True
            },
            {
                "name": "Achari Gobhi Pizza",
                "prices": {"small": 12.99, "medium": 16.99, "large": 20.99},
                "description": "Pickle-spiced cauliflower with tangy achari masala",
                "vegetarian": True,
                "vegan_available": True,
                "popular": True
            },
            {
                "name": "Saag Paneer Pizza",
                "prices": {"small": 13.99, "medium": 17.99, "large": 21.99},
                "description": "Creamy spinach with paneer cubes",
                "vegetarian": True
            },
            {
                "name": "Aloo Gobi Pizza",
                "prices": {"small": 11.99, "medium": 15.99, "large": 19.99},
                "description": "Classic potato and cauliflower with turmeric",
                "vegetarian": True
            },
            {
                "name": "Chana Masala Pizza",
                "prices": {"small": 12.99, "medium": 16.99, "large": 20.99},
                "description": "Spiced chickpeas with tomatoes",
                "vegetarian": True,
                "vegan_available": True
            },
            {
                "name": "Malai Kofta Pizza",
                "prices": {"small": 14.99, "medium": 18.99, "large": 22.99},
                "description": "Creamy veggie koftas in tomato-cream sauce",
                "vegetarian": True
            }
        ],
        "sides": [
            {"name": "Garlic Naan Sticks", "price": 5.99},
            {"name": "Vegetable Samosas (2pc)", "price": 4.99},
            {"name": "Chicken Samosas (2pc)", "price": 5.99},
            {"name": "Paneer Pakora (6pc)", "price": 7.99},
            {"name": "Onion Bhaji (6pc)", "price": 5.99}
        ],
        "beverages": [
            {"name": "Mango Lassi", "price": 4.99},
            {"name": "Sweet Lassi", "price": 3.99},
            {"name": "Masala Chai", "price": 3.49}
        ]
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
