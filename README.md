# Curry Pizza House AI Chat Assistant

An AI-powered menu assistant chatbot for Curry Pizza House that helps customers explore the menu, ask about ingredients, allergens, and get recommendations.

## Features

- 🍕 **Menu Information**: Get details about all pizzas, wings, appetizers, and more
- 🌱 **Dietary Options**: Find vegetarian, vegan, and Jain-friendly options
- ⚠️ **Allergen Info**: Get allergen information for sauces, crusts, and ingredients
- 🍗 **Wings Menu**: 8 flavors available in multiple sizes
- 🔧 **Build Your Own**: Information about custom pizza options

## Popular Pizzas

### Indian Craft Non-Veg
- Butter Chicken ⭐
- Tandoori Chicken ⭐
- Chicken Tikka ⭐

### Indian Craft Veg
- Chilli Paneer ⭐
- Achari Gobhi ⭐
- Curry Veggie Delight ⭐

### Regular Standard
- Classic Combination ⭐
- Meat Lover's ⭐
- Hawaiian ⭐

---

## 🔌 How to Embed This Chat Widget on www.currypizzahouse.com

### Option 1: Embed as an iFrame

Add this code to your website where you want the chat button to appear:

```html
<!-- Curry Pizza House Chat Widget -->
<iframe 
  src="https://cph-ai-assistant.emergent.host" 
  style="position: fixed; bottom: 20px; right: 20px; width: 400px; height: 600px; border: none; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); z-index: 9999;"
  allow="microphone"
></iframe>
```

### Option 2: Embed as a Chat Button with Popup

Add this code before the closing `</body>` tag:

```html
<!-- Curry Pizza House Chat Widget -->
<style>
  #cph-chat-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #f97316, #dc2626);
    border-radius: 50%;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(249, 115, 22, 0.4);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease;
  }
  
  #cph-chat-button:hover {
    transform: scale(1.1);
  }
  
  #cph-chat-button svg {
    width: 28px;
    height: 28px;
    fill: white;
  }
  
  #cph-chat-iframe {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 380px;
    height: 550px;
    border: none;
    border-radius: 16px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.2);
    z-index: 9998;
    display: none;
    background: white;
  }
  
  #cph-chat-iframe.open {
    display: block;
  }
  
  @media (max-width: 480px) {
    #cph-chat-iframe {
      width: calc(100% - 40px);
      height: 70vh;
      bottom: 80px;
      right: 20px;
      left: 20px;
    }
  }
</style>

<button id="cph-chat-button" onclick="toggleCPHChat()">
  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
  </svg>
</button>

<iframe id="cph-chat-iframe" src="https://cph-ai-assistant.emergent.host"></iframe>

<script>
  function toggleCPHChat() {
    const iframe = document.getElementById('cph-chat-iframe');
    iframe.classList.toggle('open');
  }
</script>
```

### Option 3: Full Page Embed

If you want a dedicated chat page on your website:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chat with Us - Curry Pizza House</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: Arial, sans-serif; }
    iframe {
      width: 100%;
      height: 100vh;
      border: none;
    }
  </style>
</head>
<body>
  <iframe src="https://cph-ai-assistant.emergent.host"></iframe>
</body>
</html>
```

---

## 🛠️ Integration Steps for www.currypizzahouse.com

### Step 1: Choose Your Integration Method
- **Floating Chat Button** (Recommended): Non-intrusive, appears on all pages
- **iFrame Embed**: Embed in a specific section of your website
- **Dedicated Page**: Create a separate /chat page

### Step 2: Add the Code
1. Access your website's HTML/CMS (WordPress, Squarespace, Wix, etc.)
2. Navigate to the footer section or theme settings
3. Paste the code snippet from Option 2 above
4. Save and publish

### Step 3: For WordPress Sites
1. Go to **Appearance → Theme Editor** or use a plugin like "Insert Headers and Footers"
2. Add the code before `</body>` in your theme's footer.php
3. Or use a plugin like **WPCode** to insert custom code

### Step 4: For Squarespace/Wix/Shopify
1. Go to **Settings → Advanced → Code Injection**
2. Paste the code in the "Footer" section
3. Save changes

### Step 5: Test the Integration
1. Visit your website
2. Look for the chat button in the bottom-right corner
3. Click to open the chat and test a few queries:
   - "Show me vegetarian pizzas"
   - "What's on the Butter Chicken pizza?"
   - "Do you have wings?"

---

## 🔄 URL Change Request

To change the URL from `pickle-gobi-pizza.emergent.host` to `cph-ai-assistant.emergent.host`:

**Contact Emergent Support:**
- Email: support@emergentagent.com
- Include:
  - Current URL: `pickle-gobi-pizza.emergent.host`
  - Desired URL: `cph-ai-assistant.emergent.host`
  - Your account/project details

---

## 📱 Mobile Responsiveness

The chat widget is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones

---

## 🔒 Security Notes

- The chat uses HTTPS for secure communication
- No customer data is stored permanently
- CORS is configured for cross-origin requests

---

## 📞 Support

For technical issues or questions:
- Emergent Platform: support@emergentagent.com
- Curry Pizza House: Visit www.currypizzahouse.com

---

## 📝 Customization

If you need to customize the chat widget appearance or functionality:
1. Colors can be modified in the CSS
2. Position can be changed (bottom-left, top-right, etc.)
3. Size can be adjusted for different screen sizes

For backend/AI response customization, contact your development team.
