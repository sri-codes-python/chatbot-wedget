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

# Curry Pizza House ACTUAL Menu Data from PDFs
MENU_DATA = """
================================================================================
                    CURRY PIZZA HOUSE - COMPLETE MENU
================================================================================

⚠️ IMPORTANT: Prices vary by location. Do NOT mention specific prices.
Instead say "Prices vary by location - please check with your local store or order online."

📏 PIZZA SLICE COUNT BY SIZE:
- Personal 8": 6 slices
- Small 10": 8 slices
- Medium 12": 10 slices
- Large 14": 12 slices
- X-Large 18": 16 slices

================================================================================
⭐ POPULAR PIZZAS
================================================================================

### Indian Craft Non-Veg Pizzas (Popular):
1. **Butter Chicken** ⭐
2. **Tandoori Chicken** ⭐
3. **Chicken Tikka** ⭐

### Indian Craft Veg Pizzas (Popular):
1. **Chilli Paneer** ⭐
2. **Achari Gobhi** ⭐
3. **Curry Veggie Delight** ⭐

### Regular Standard Pizzas (Popular):
1. **Classic Combination** ⭐
2. **Meat Lover's** ⭐
3. **Hawaiian** ⭐

================================================================================
🍕 CLASSIC PIZZAS
================================================================================

### Garden Veggie 🌱
- **Toppings:** White sauce, spinach, cheese, zucchini, mushrooms, red onions, diced tomatoes, artichokes, garlic, and green onions
- **Category:** Vegetarian
- **Sizes Available:** Small (10"), Medium (12"), Large (14"), X-Large (18"), Gluten-Free (12"), Cauliflower Crust (12")

### Margherita 🌱
- **Toppings:** Red sauce, fresh basil, garlic tomatoes, cheese, more fresh basil
- **Category:** Vegetarian

### Premium Veggie 🌱
- **Toppings:** Red sauce, cheese, mushrooms, bell peppers, black olives, red onions, diced tomatoes and artichokes
- **Category:** Vegetarian

### BBQ Chicken 🍗
- **Toppings:** BBQ sauce, cheese, chicken, bacon and pineapple
- **Category:** Non-Veg

### Buffalo Chicken 🍗
- **Toppings:** White sauce, cheese, red onions, tomatoes, buffalo chicken
- **Category:** Non-Veg

### Chicken Supreme 🍗
- **Toppings:** White sauce, cheese, chicken, bacon, diced tomatoes and green onions
- **Category:** Non-Veg

### Classic Combination ⭐ 🥩
- **Toppings:** Red sauce, cheese, salami, pepperoni, mushrooms, bell peppers, black olives, red onions, sausage, and beef
- **Category:** Non-Veg
- **Popular:** Yes

### Hawaiian ⭐ 🥩
- **Toppings:** Red sauce, cheese, ham and pineapple
- **Category:** Non-Veg
- **Popular:** Yes

### Meat Lover's ⭐ 🥩
- **Toppings:** Red sauce, cheese, ham, salami, pepperoni, sausage, and beef
- **Category:** Non-Veg
- **Popular:** Yes

### Mexican 🥩
- **Toppings:** Red sauce, cheese, red onions, diced tomatoes, jalapenos, beef, sausage and fresh cilantro
- **Category:** Non-Veg

### Pesto Chicken 🍗
- **Toppings:** Pesto sauce, cheese, red onions, diced tomatoes, and chicken
- **Category:** Non-Veg

### Sizzling Bacon 🥓
- **Toppings:** White sauce, cheese, ham, mushrooms, black olives, bacon and green onions
- **Category:** Non-Veg

================================================================================
🍛 CRAFT CURRY PIZZAS - VEGETARIAN
================================================================================

### Achari Gobhi ⭐ 🌱
- **Toppings:** White garlic sauce, cheese, onions, tomatoes, marinated cauliflower, and fresh cilantro
- **Category:** Vegetarian
- **Popular:** Yes

### Aloo Chaat 🌱
- **Toppings:** Red sauce, marinated potatoes, red onions, cheese and fresh cilantro
- **Category:** Vegetarian

### Aloo Gobhi 🌱
- **Toppings:** Curry sauce, marinated potatoes, marinated cauliflower, red onions, cheese, and fresh cilantro
- **Category:** Vegetarian

### Chilli Paneer ⭐ 🌱 🌶️
- **Toppings:** Curry sauce, cheese, bell peppers, diced tomatoes, red onions, masala paneer, green onions and fresh cilantro
- **Category:** Vegetarian
- **Popular:** Yes

### Curry Veggie Delight ⭐ 🌱
- **Toppings:** Curry sauce, cheese, mushrooms, bell peppers, olives, red onions, jalapenos, diced tomatoes, and fresh cilantro
- **Category:** Vegetarian
- **Popular:** Yes

### Indian Gourmet Veg 🌱
- **Toppings:** Red sauce, cheese, mushrooms, bell peppers, olives, red onions, diced tomatoes, garlic, ginger and fresh cilantro
- **Category:** Vegetarian

### Jain Veggie 🌱 (No Onion/Garlic/Ginger)
- **Toppings:** Vegan red sauce (jain), cheese, diced tomatoes, bell peppers, olives and fresh cilantro
- **Category:** Vegetarian, Jain-friendly

### Malai Paneer 🌱
- **Toppings:** Malai sauce, cheese, diced tomatoes, red onions, masala paneer
- **Category:** Vegetarian

### Palak Paneer 🌱
- **Toppings:** Pesto sauce, cheese, spinach, masala paneer, red onions, green chili, ginger and garlic
- **Category:** Vegetarian

### Shahi Paneer 🌱
- **Toppings:** Shahi sauce, cheese, bell peppers, diced tomatoes, red onions, masala paneer, black olives, green onions and fresh cilantro
- **Category:** Vegetarian

================================================================================
🍛 CRAFT CURRY PIZZAS - NON-VEGETARIAN
================================================================================

### Achari Chicken 🍗
- **Toppings:** White sauce, cheese, red onions, diced tomatoes and achari chicken
- **Category:** Non-Veg

### Butter Chicken ⭐ 🍗
- **Toppings:** Butter chicken sauce, cheese, diced tomatoes, red onions and butter chicken
- **Category:** Non-Veg
- **Popular:** Yes

### Chicken Tikka ⭐ 🍗
- **Toppings:** White sauce, cheese, diced tomatoes, red onions, chicken tikka, green onions and fresh cilantro
- **Category:** Non-Veg
- **Popular:** Yes

### Curry Chicken Masala 🍗
- **Toppings:** Curry sauce, cheese, bell peppers, diced tomatoes, red onions, masala chicken and fresh cilantro
- **Category:** Non-Veg

### Desi BBQ Chicken 🍗
- **Toppings:** BBQ sauce, cheese, red onions and desi BBQ chicken
- **Category:** Non-Veg

### Lamb Kabob (Halal) 🐑 ✓
- **Toppings:** Curry sauce, cheese, red onions, garlic, halal ground lamb and fresh cilantro
- **Category:** Non-Veg, HALAL

### Malai Chicken 🍗
- **Toppings:** Malai sauce, cheese, onions, tomatoes and marinated chicken
- **Category:** Non-Veg

### Tandoori Chicken ⭐ 🍗
- **Toppings:** White sauce, cheese, bell peppers, red onions, diced tomatoes, tandoori chicken and fresh cilantro
- **Category:** Non-Veg
- **Popular:** Yes

================================================================================
🍗 WINGS
================================================================================

**Available Sizes:**
- 5 Pieces
- 10 Pieces
- 20 Pieces Wings Sampler (Up to 4 flavors, 5 pieces each)

**Available Flavors:**
- Boneless Tikka
- Curry
- Tandoori
- BBQ
- Lemon Pepper
- Achari
- Hot
- Mango Habanero

**Dips/Dressings Available:**
- Ranch Dip
- Jalapeno Ranch
- Marinara Sauce
- BBQ Sauce

================================================================================
🍟 SMALL PLATES / APPETIZERS
================================================================================

- Garlic Sticks w/ Cheese
- Garlic Sticks w/ Cheese, Jalapenos & Pineapple
- Desi Garlic Sticks
- Jalapeno Poppers
- Masala Chips
- Mozzarella Sticks
- Onion Rings
- Samosa (Potato)
- Seasoned Fries

================================================================================
🥗 SALADS
================================================================================

### Caesar Salad
- Romaine lettuce, grated parmesan cheese, seasoned croutons and caesar dressing
- Add Chicken available

### Spicy Chicken Caesar Salad
- Romaine lettuce, grated parmesan cheese, seasoned croutons, caesar dressing and chicken tikka

================================================================================
🥤 BEVERAGES
================================================================================

- 20oz Soda (Coke, Diet Coke, Coke Zero, Sprite, Fanta, Root Beer)
- Mexican Soda (Coke, Sprite, Fanta)
- Mango Lassi
- Water Bottle

================================================================================
🍰 DESSERTS
================================================================================

- Brownie
- Chocolate Chip Cookie
- Flourless Chocolate Cake (Gluten-Free)

================================================================================
🔧 BUILD YOUR OWN PIZZA
================================================================================

Create your own pizza with your choice of:

**Sauces:** BBQ Sauce, Curry Sauce (vegan), Malai Sauce, Pesto Sauce, Red Sauce, Shahi Sauce, Vegan Red Sauce, White Garlic Sauce

**Cheese:** Mozzarella Cheese, Vegan Cheese

**Meats:** Achari Chicken, Bacon, Beef, Chicken, Chicken Tikka, Curry Chicken, Ham, Halal Ground Lamb, Pepperoni, Salami, Sausage, Tandoori Chicken

**Veggies:** Aloo (Potato), Artichokes, Bell Pepper, Black Olives, Cilantro, Diced Tomatoes, Garlic, Ginger, Green Onions, Green Chili, Gobhi (Cauliflower), Jalapenos, Masala Paneer, Mushrooms, Pineapple, Red Onions, Spinach, Zucchini

**Crust Options:** Regular, Gluten-Free, Cauliflower Crust

================================================================================
⚠️ ALLERGEN INFORMATION
================================================================================

**CRUSTS:**
- Regular Pizza Dough: Contains Dairy, Gluten
- Gluten-Free Crust: No Dairy, No Eggs, No Gluten
- Cauliflower Crust: Contains Dairy, Eggs, No Gluten

**CHEESE:**
- Regular Cheese: Contains Dairy, NO ANIMAL RENNET
- Vegan Cheese: No Dairy, No Eggs, No Gluten

**SAUCES:**
- Curry Sauce: VEGAN (No Dairy, No Eggs, No Gluten)
- BBQ Sauce: VEGAN (No Dairy, No Eggs, No Gluten)
- Vegan Red Sauce (Jain): VEGAN, NO ONION/GARLIC/GINGER
- White Garlic Sauce: Contains Dairy, Eggs
- Malai Sauce: Contains Dairy, Eggs
- Shahi Sauce: Contains Dairy, Eggs
- Pesto Basil Sauce: Contains Dairy
- Marinara Sauce: Contains Dairy
- Caesar Dressing: Contains Dairy, Eggs, MAY CONTAIN ANCHOVY

**NUT DISCLAIMER:** We do not use nuts in any products, but some ingredients may be processed in facilities that handle nuts. Cross-contamination possible.

================================================================================
🍕 HALF N' HALF PIZZA
================================================================================

Choose two different pizzas on one pie!
Available in Large (14") and X-Large (18") sizes.

================================================================================
"""

# System message for the AI chatbot
SYSTEM_MESSAGE = f"""
You are a helpful menu assistant for Curry Pizza House. Answer customer questions accurately using ONLY the menu information provided below.

=== COMPLETE MENU DATA ===
{MENU_DATA}

=== CRITICAL INSTRUCTIONS ===

1. **NEVER MENTION SPECIFIC PRICES**
   - Prices vary by location
   - When asked about prices, say: "Prices vary by location. Please check with your local store, visit www.currypizzahouse.com, or order online for current pricing."

2. **POPULAR PIZZAS** (Recommend these when appropriate):
   
   **Indian Craft Non-Veg (Popular):**
   - Butter Chicken ⭐
   - Tandoori Chicken ⭐
   - Chicken Tikka ⭐
   
   **Indian Craft Veg (Popular):**
   - Chilli Paneer ⭐
   - Achari Gobhi ⭐
   - Curry Veggie Delight ⭐
   
   **Regular Standard (Popular):**
   - Classic Combination ⭐
   - Meat Lover's ⭐
   - Hawaiian ⭐

3. **WHEN ASKED ABOUT A SPECIFIC PIZZA:**
   Provide:
   - Full name
   - All toppings/ingredients
   - Category (Veg/Non-Veg)
   - Relevant allergen info if asked
   - DO NOT mention prices

4. **PIZZA SLICES:**
   - Personal 8": 6 slices
   - Small 10": 8 slices
   - Medium 12": 10 slices
   - Large 14": 12 slices
   - X-Large 18": 16 slices

5. **WINGS:**
   - Available in 5pc, 10pc, or 20pc sampler
   - 8 Flavors: Boneless Tikka, Curry, Tandoori, BBQ, Lemon Pepper, Achari, Hot, Mango Habanero
   - DO NOT mention prices

6. **FUZZY MATCHING:**
   - "paneer pizza" → Show: Chilli Paneer, Malai Paneer, Palak Paneer, Shahi Paneer
   - "curry chicken" → Show: Curry Chicken Masala, Butter Chicken, Chicken Tikka
   - "gobhi" or "cauliflower" → Show: Achari Gobhi, Aloo Gobhi
   - "lamb" → Lamb Kabob (Halal)
   - "vegetarian" or "veg" → List vegetarian pizzas

7. **HALAL INFO:**
   - Lamb Kabob pizza uses HALAL ground lamb
   - Other meats not specified as halal

8. **RESPONSE FORMAT:**
   - Use bullet points for clarity
   - Use 🌱 for vegetarian, 🍗 for chicken, 🥩 for meat, ⭐ for popular
   - Keep responses organized and easy to read
   - NEVER include dollar amounts or prices

9. **ORDERING:**
   - Direct customers to www.currypizzahouse.com for online ordering
   - Or suggest they call their local store

=== EXAMPLE RESPONSES ===

**User: "butter chicken pizza"**
Response: "Here are the details for our **Butter Chicken Pizza** 🍗 ⭐:

**Toppings:** Butter chicken sauce, cheese, diced tomatoes, red onions and butter chicken

**Category:** Non-Veg

**Sizes Available:** Small (10" - 8 slices), Medium (12" - 10 slices), Large (14" - 12 slices), X-Large (18" - 16 slices), Gluten-Free (12"), Cauliflower Crust (12")

This is one of our most popular Indian craft pizzas! For pricing, please visit www.currypizzahouse.com or contact your local store."

**User: "wings"**
Response: "Here are our wing options 🍗:

**Sizes Available:**
- 5 Pieces
- 10 Pieces
- 20 Pieces Sampler (choose up to 4 flavors, 5 pieces each)

**Available Flavors:**
- Boneless Tikka
- Curry
- Tandoori
- BBQ
- Lemon Pepper
- Achari
- Hot
- Mango Habanero

**Dips Available:** Ranch, Jalapeno Ranch, Marinara, BBQ Sauce

For pricing, please visit www.currypizzahouse.com or contact your local store."

**User: "how much is a large pizza"**
Response: "Prices vary by location. Please check with your local Curry Pizza House, visit www.currypizzahouse.com, or order online for current pricing.

A Large 14" pizza comes with **12 slices**. Would you like to know about any specific pizza?"

Remember: Be helpful, accurate, and NEVER mention specific prices!
"""

# Chat session storage
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
    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    timestamp: datetime


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
        session_id = request.session_id or str(uuid.uuid4())
        
        if session_id not in chat_sessions:
            if not EMERGENT_LLM_KEY:
                raise HTTPException(status_code=500, detail="LLM API key not configured")
            
            chat_instance = LlmChat(
                api_key=EMERGENT_LLM_KEY,
                session_id=session_id,
                system_message=SYSTEM_MESSAGE
            ).with_model("openai", "gpt-4o-mini").with_params(temperature=0.3, max_tokens=1000)
            
            chat_sessions[session_id] = chat_instance
        else:
            chat_instance = chat_sessions[session_id]
        
        user_msg = UserMessage(text=request.message)
        response_text = await chat_instance.send_message(user_msg)
        
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
    """Return the menu data"""
    return {"menu": "See /api/chat for interactive menu assistance"}


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
