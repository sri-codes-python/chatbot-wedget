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

## 🔌 How to Embed "Ask AI" Chat Button on www.currypizzahouse.com

### RECOMMENDED: "Ask AI" Floating Button

Copy and paste this code before the closing `</body>` tag on your website:

```html
<!-- Curry Pizza House "Ask AI" Chat Widget -->
<style>
  /* Ask AI Button */
  #cph-chat-button {
    position: fixed;
    bottom: 24px;
    right: 24px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    background: linear-gradient(135deg, #FF6B00 0%, #E63900 100%);
    border: none;
    border-radius: 50px;
    cursor: pointer;
    box-shadow: 0 4px 20px rgba(255, 107, 0, 0.4);
    z-index: 99999;
    transition: all 0.3s ease;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  
  #cph-chat-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(255, 107, 0, 0.5);
  }
  
  #cph-chat-button:active {
    transform: translateY(0);
  }
  
  #cph-chat-button svg {
    width: 22px;
    height: 22px;
    fill: white;
  }
  
  #cph-chat-button span {
    color: white;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.3px;
  }
  
  /* Chat Window */
  #cph-chat-container {
    position: fixed;
    bottom: 90px;
    right: 24px;
    width: 400px;
    height: 580px;
    border: none;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    z-index: 99998;
    display: none;
    overflow: hidden;
    background: white;
  }
  
  #cph-chat-container.open {
    display: block;
    animation: slideUp 0.3s ease;
  }
  
  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  #cph-chat-iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
  
  /* Close button */
  #cph-close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 30px;
    height: 30px;
    background: rgba(0, 0, 0, 0.1);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
    transition: background 0.2s;
  }
  
  #cph-close-btn:hover {
    background: rgba(0, 0, 0, 0.2);
  }
  
  #cph-close-btn svg {
    width: 14px;
    height: 14px;
    stroke: #333;
  }
  
  /* Mobile Responsive */
  @media (max-width: 480px) {
    #cph-chat-button {
      bottom: 16px;
      right: 16px;
      padding: 10px 16px;
    }
    
    #cph-chat-button span {
      font-size: 14px;
    }
    
    #cph-chat-container {
      width: calc(100% - 32px);
      height: 75vh;
      bottom: 80px;
      right: 16px;
      left: 16px;
      border-radius: 16px;
    }
  }
</style>

<!-- Ask AI Button -->
<button id="cph-chat-button" onclick="toggleCPHChat()">
  <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C6.48 2 2 6.48 2 12c0 1.54.36 2.98.97 4.29L2 22l5.71-.97A9.96 9.96 0 0 0 12 22c5.52 0 10-4.48 10-10S17.52 2 12 2zm-1 15h2v-2h-2v2zm0-4h2V7h-2v6z"/>
  </svg>
  <span>Ask AI</span>
</button>

<!-- Chat Container -->
<div id="cph-chat-container">
  <button id="cph-close-btn" onclick="toggleCPHChat()">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path d="M18 6L6 18M6 6l12 12"/>
    </svg>
  </button>
  <iframe id="cph-chat-iframe" src="https://pickle-gobi-pizza.emergent.host"></iframe>
</div>

<script>
  function toggleCPHChat() {
    const container = document.getElementById('cph-chat-container');
    container.classList.toggle('open');
  }
  
  // Close chat when clicking outside (optional)
  document.addEventListener('click', function(e) {
    const container = document.getElementById('cph-chat-container');
    const button = document.getElementById('cph-chat-button');
    if (container.classList.contains('open') && 
        !container.contains(e.target) && 
        !button.contains(e.target)) {
      container.classList.remove('open');
    }
  });
</script>
<!-- End Curry Pizza House Chat Widget -->
```

---

## 🎨 Button Preview

The "Ask AI" button will look like this:

```
┌─────────────────────────────────────────────────┐
│                                                 │
│              Your Website Content               │
│                                                 │
│                                                 │
│                          ┌──────────────────┐   │
│                          │  💬  Ask AI      │   │
│                          └──────────────────┘   │
└─────────────────────────────────────────────────┘

When clicked:
┌─────────────────────────────────────────────────┐
│                              ┌────────────────┐ │
│                              │ ✕              │ │
│                              │                │ │
│                              │  Chat Window   │ │
│                              │                │ │
│                              │                │ │
│                              └────────────────┘ │
│                          ┌──────────────────┐   │
│                          │  💬  Ask AI      │   │
│                          └──────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Installation Steps for www.currypizzahouse.com

### Step 1: Access Your Website Code
- **WordPress**: Go to Appearance → Theme Editor → footer.php
- **Squarespace**: Settings → Advanced → Code Injection → Footer
- **Wix**: Settings → Custom Code → Body - End
- **Shopify**: Online Store → Themes → Edit Code → theme.liquid

### Step 2: Paste the Code
- Copy the entire code block above
- Paste it just before `</body>`
- Save/Publish changes

### Step 3: Update URL (After Emergent Changes It)
- Replace `https://pickle-gobi-pizza.emergent.host` with `https://cph-ai-assistant.emergent.host`

### Step 4: Test
1. Visit your website
2. Look for the orange "Ask AI" button in bottom-right
3. Click to open chat
4. Test queries like "What's on the Butter Chicken pizza?"

---

## 🎨 Customization Options

### Change Button Colors
Find this line and modify the colors:
```css
background: linear-gradient(135deg, #FF6B00 0%, #E63900 100%);
```
- `#FF6B00` = Orange (primary)
- `#E63900` = Red-Orange (secondary)

### Change Button Text
Find this line and change the text:
```html
<span>Ask AI</span>
```
Options: "Chat with AI", "Need Help?", "Ask Us", etc.

### Change Button Position
Modify these values:
```css
bottom: 24px;  /* Distance from bottom */
right: 24px;   /* Distance from right */
```

For left side:
```css
right: auto;
left: 24px;
```

---

## 🔄 URL Change Request

**Current URL:** `pickle-gobi-pizza.emergent.host`
**Desired URL:** `cph-ai-assistant.emergent.host`

**Contact:** support@emergentagent.com

---

## 📱 Mobile Responsive

The widget is fully responsive:
- **Desktop**: 400px wide chat window
- **Mobile**: Full-width (minus margins), 75% viewport height
- Button adjusts size on mobile

---

## 📞 Support

- **Emergent Platform:** support@emergentagent.com
- **Curry Pizza House:** www.currypizzahouse.com
