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

# Curry Pizza House Menu Data
MENU_DATA = """
# Curry Pizza House Menu - Indian Fusion Pizzas

## IMPORTANT NOTES:
- We are Curry Pizza House - an Indian fusion pizza restaurant
- We do NOT use BBQ sauce on any pizzas - we use traditional Indian curry sauces and spices
- Our signature base sauces are: Curry sauce, Tikka Masala sauce, Mint Chutney, Creamy Spinach (Saag), and Spiced Tomato sauce
- HALAL: Our Keema Pizza uses halal lamb. Our chicken is also halal-certified.
- PORK: Only our Vindaloo Pizza contains pork (not halal)

## Signature Curry Pizzas (11 Total)

### 1. Butter Chicken Pizza ⭐ BESTSELLER
- **Price:** Small $14.99 | Medium $18.99 | Large $22.99
- **Description:** Creamy butter chicken curry sauce with tender chicken, bell peppers, onions, and cilantro on our signature curry-infused crust
- **Sauce:** Creamy Butter Chicken Curry Sauce (tomato-cream based with Indian spices)
- **Toppings:** Chicken pieces, bell peppers, onions, cilantro
- **Allergens:** Dairy, Gluten, Nuts (cashew paste)
- **Halal:** Yes, chicken is halal-certified
- **Spice Level:** Mild

### 2. Tikka Masala Pizza
- **Price:** Small $15.99 | Medium $19.99 | Large $23.99
- **Description:** Spiced chicken tikka with tomato masala sauce, roasted peppers, and fresh mozzarella
- **Sauce:** Tikka Masala Sauce (spiced tomato-cream)
- **Toppings:** Chicken tikka pieces, roasted bell peppers, onions, mozzarella
- **Allergens:** Dairy, Gluten
- **Halal:** Yes, chicken is halal-certified
- **Spice Level:** Medium

### 3. Paneer Tikka Pizza (Vegetarian)
- **Price:** Small $13.99 | Medium $17.99 | Large $21.99
- **Description:** Marinated paneer cubes with spiced tomato sauce, onions, and fresh herbs
- **Sauce:** Spiced Tomato Tikka Sauce
- **Toppings:** Paneer cubes, onions, bell peppers, fresh herbs
- **Allergens:** Dairy, Gluten
- **Halal:** Vegetarian (no meat)
- **Spice Level:** Medium

### 4. Tandoori Chicken Pizza
- **Price:** Small $14.99 | Medium $18.99 | Large $22.99
- **Description:** Smoky tandoori chicken with mint chutney, red onions, and jalapeños
- **Sauce:** Mint Chutney base with tandoori spices
- **Toppings:** Tandoori chicken, red onions, jalapeños, cilantro
- **Allergens:** Dairy, Gluten
- **Halal:** Yes, chicken is halal-certified
- **Spice Level:** Medium-Hot

### 5. Achari Gobhi Pizza (Vegetarian) ⭐ MOST POPULAR
- **Price:** Small $12.99 | Medium $16.99 | Large $20.99
- **Description:** Pickle-spiced cauliflower (gobhi) with tangy achari masala, green chilies, and fresh coriander
- **Sauce:** Achari (pickle) Masala Sauce - tangy and spicy
- **Toppings:** Spiced cauliflower, green chilies, fresh coriander, pickled spices
- **Allergens:** Gluten, Mustard
- **Halal:** Vegetarian (no meat)
- **Vegan Option:** Available without cheese
- **Spice Level:** Medium-Hot 🌶️

### 6. Keema Pizza (Lamb) ⭐ HALAL LAMB
- **Price:** Small $15.99 | Medium $19.99 | Large $23.99
- **Description:** Spiced minced halal lamb with peas, onions, and garam masala
- **Sauce:** Spiced Tomato Keema Sauce
- **Toppings:** Minced lamb, green peas, onions, garam masala spices
- **Allergens:** Dairy, Gluten
- **Halal:** YES - Uses certified halal lamb
- **Spice Level:** Medium

### 7. Saag Paneer Pizza (Vegetarian)
- **Price:** Small $13.99 | Medium $17.99 | Large $21.99
- **Description:** Creamy spinach with paneer cubes, garlic, and Indian spices
- **Sauce:** Creamy Saag (Spinach) Sauce
- **Toppings:** Paneer cubes, garlic, Indian spices
- **Allergens:** Dairy, Gluten
- **Halal:** Vegetarian (no meat)
- **Spice Level:** Mild

### 8. Vindaloo Pizza (Spicy!) ⚠️ CONTAINS PORK
- **Price:** Small $15.99 | Medium $19.99 | Large $23.99
- **Description:** Fiery vindaloo pork with potatoes and hot chilies - for spice lovers!
- **Sauce:** Vindaloo Curry Sauce (very spicy)
- **Toppings:** Pork pieces, potatoes, hot chilies
- **Allergens:** Dairy, Gluten
- **Halal:** NO - Contains pork
- **Spice Level:** Extra Hot 🔥🔥🔥

### 9. Chana Masala Pizza (Vegan Available)
- **Price:** Small $12.99 | Medium $16.99 | Large $20.99
- **Description:** Spiced chickpeas with tomatoes, onions, and aromatic spices
- **Sauce:** Chana Masala Sauce (spiced tomato)
- **Toppings:** Chickpeas, tomatoes, onions, cumin, coriander
- **Allergens:** Gluten (Vegan option: no dairy)
- **Halal:** Vegetarian (no meat)
- **Vegan Option:** Available without cheese
- **Spice Level:** Medium

### 10. Aloo Gobi Pizza (Vegetarian)
- **Price:** Small $11.99 | Medium $15.99 | Large $19.99
- **Description:** Classic potato and cauliflower with turmeric and cumin
- **Sauce:** Turmeric-Cumin Spiced Sauce
- **Toppings:** Potatoes, cauliflower, turmeric, cumin seeds
- **Allergens:** Dairy, Gluten
- **Halal:** Vegetarian (no meat)
- **Spice Level:** Mild

### 11. Malai Kofta Pizza (Vegetarian)
- **Price:** Small $14.99 | Medium $18.99 | Large $22.99
- **Description:** Creamy veggie koftas in rich tomato-cream sauce
- **Sauce:** Malai (Cream) Tomato Sauce
- **Toppings:** Vegetable kofta balls, cream sauce, nuts
- **Allergens:** Dairy, Gluten, Nuts
- **Halal:** Vegetarian (no meat)
- **Spice Level:** Mild

## Sides & Extras

- **Garlic Naan Sticks:** $5.99
- **Mango Lassi:** $4.99
- **Raita Dipping Sauce:** $2.99
- **Extra Cheese:** $2.50
- **Extra Spicy Option:** Free (just ask!)

## Allergen & Dietary Information
- **Gluten-Free Crust:** Available for +$3.00 on any pizza
- **Dairy-Free Cheese:** Available for +$2.00 on any pizza
- **Nut Allergies:** Butter Chicken and Malai Kofta contain nuts
- **Mustard Allergy:** Achari Gobhi contains mustard
- **Halal Options:** All chicken and lamb are halal-certified. Only Vindaloo (pork) is NOT halal.
- **Vegan Options:** Achari Gobhi and Chana Masala available vegan (no cheese)

## Popular Combinations
1. **Achari Gobhi Pizza** - Our bestselling vegetarian option!
2. **Butter Chicken Pizza** - Customer favorite for meat lovers
3. **Paneer Tikka Pizza** - Perfect for vegetarians who love paneer
"""

# System message for the AI chatbot
SYSTEM_MESSAGE = f"""
You are a friendly and helpful menu assistant for Curry Pizza House, a unique restaurant that combines authentic Indian flavors with classic pizza perfection.

Your role is to:
1. Help customers explore our menu
2. Answer questions about ingredients, allergens, and dietary options
3. Make recommendations based on customer preferences
4. Provide accurate pricing information
5. Be enthusiastic about our unique curry-pizza fusion!

Here is our complete menu information:
{MENU_DATA}

Important guidelines:
- Always be friendly, warm, and welcoming
- If asked about allergens, be thorough and accurate
- Recommend popular items like our Achari Gobhi Pizza when appropriate
- If a customer has dietary restrictions, suggest suitable alternatives
- Use emojis occasionally to be friendly (🍕, 🌶️, ⭐, etc.)
- Keep responses concise but informative
- If you don't know something, say so politely
- Always mention prices when discussing specific items
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
            ).with_model("openai", "gpt-4o-mini").with_params(temperature=0.7, max_tokens=500)
            
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
        "signature_pizzas": [
            {
                "name": "Butter Chicken Pizza",
                "prices": {"small": 14.99, "medium": 18.99, "large": 22.99},
                "description": "Creamy butter chicken with bell peppers, onions, and cilantro",
                "allergens": ["Dairy", "Gluten", "Nuts"],
                "vegetarian": False,
                "popular": True
            },
            {
                "name": "Tikka Masala Pizza",
                "prices": {"small": 15.99, "medium": 19.99, "large": 23.99},
                "description": "Spiced chicken tikka with tomato masala sauce",
                "allergens": ["Dairy", "Gluten"],
                "vegetarian": False,
                "popular": False
            },
            {
                "name": "Paneer Tikka Pizza",
                "prices": {"small": 13.99, "medium": 17.99, "large": 21.99},
                "description": "Marinated paneer cubes with spiced tomato sauce",
                "allergens": ["Dairy", "Gluten"],
                "vegetarian": True,
                "popular": True
            },
            {
                "name": "Tandoori Chicken Pizza",
                "prices": {"small": 14.99, "medium": 18.99, "large": 22.99},
                "description": "Smoky tandoori chicken with mint chutney",
                "allergens": ["Dairy", "Gluten"],
                "vegetarian": False,
                "popular": False
            },
            {
                "name": "Achari Gobhi Pizza",
                "prices": {"small": 12.99, "medium": 16.99, "large": 20.99},
                "description": "Pickle-spiced cauliflower with tangy achari masala",
                "allergens": ["Gluten", "Mustard"],
                "vegetarian": True,
                "vegan_available": True,
                "popular": True,
                "spice_level": "Medium-Hot"
            },
            {
                "name": "Keema Pizza",
                "prices": {"small": 15.99, "medium": 19.99, "large": 23.99},
                "description": "Spiced minced lamb with peas and garam masala",
                "allergens": ["Dairy", "Gluten"],
                "vegetarian": False,
                "popular": False
            },
            {
                "name": "Saag Paneer Pizza",
                "prices": {"small": 13.99, "medium": 17.99, "large": 21.99},
                "description": "Creamy spinach with paneer and Indian spices",
                "allergens": ["Dairy", "Gluten"],
                "vegetarian": True,
                "popular": False
            },
            {
                "name": "Vindaloo Pizza",
                "prices": {"small": 15.99, "medium": 19.99, "large": 23.99},
                "description": "Fiery vindaloo pork with potatoes and hot chilies",
                "allergens": ["Dairy", "Gluten"],
                "vegetarian": False,
                "spice_level": "Extra Hot",
                "popular": False
            }
        ],
        "vegetarian_options": [
            {
                "name": "Chana Masala Pizza",
                "prices": {"small": 12.99, "medium": 16.99, "large": 20.99},
                "description": "Spiced chickpeas with tomatoes and aromatic spices",
                "allergens": ["Gluten"],
                "vegetarian": True,
                "vegan_available": True
            },
            {
                "name": "Aloo Gobi Pizza",
                "prices": {"small": 11.99, "medium": 15.99, "large": 19.99},
                "description": "Classic potato and cauliflower with turmeric",
                "allergens": ["Dairy", "Gluten"],
                "vegetarian": True
            },
            {
                "name": "Malai Kofta Pizza",
                "prices": {"small": 14.99, "medium": 18.99, "large": 22.99},
                "description": "Creamy veggie koftas in rich tomato-cream sauce",
                "allergens": ["Dairy", "Gluten", "Nuts"],
                "vegetarian": True
            }
        ],
        "sides": [
            {"name": "Garlic Naan Sticks", "price": 5.99},
            {"name": "Mango Lassi", "price": 4.99},
            {"name": "Raita Dipping Sauce", "price": 2.99},
            {"name": "Extra Cheese", "price": 2.50},
            {"name": "Extra Spicy Option", "price": 0.00}
        ],
        "allergen_options": {
            "gluten_free_crust": 3.00,
            "dairy_free_cheese": 2.00
        }
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
