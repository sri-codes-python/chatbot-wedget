# Curry Pizza House AI Chat Assistant

A minimal, embeddable AI-powered chat widget for Curry Pizza House.

## 🎯 What This Is

A **chat-only interface** that can be embedded on www.currypizzahouse.com as a widget. No landing page - just the AI chat assistant.

---

## 🔌 How to Embed on www.currypizzahouse.com

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
  
  #cph-chat-button svg {
    width: 22px;
    height: 22px;
    fill: white;
  }
  
  #cph-chat-button span {
    color: white;
    font-size: 15px;
    font-weight: 600;
  }
  
  /* Chat Window */
  #cph-chat-container {
    position: fixed;
    bottom: 90px;
    right: 24px;
    width: 380px;
    height: 600px;
    border: none;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
    z-index: 99998;
    display: none;
    overflow: hidden;
    background: white;
  }
  
  #cph-chat-container.open {
    display: block;
    animation: cphSlideUp 0.3s ease;
  }
  
  @keyframes cphSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  #cph-chat-iframe {
    width: 100%;
    height: 100%;
    border: none;
  }
  
  /* Mobile Responsive */
  @media (max-width: 480px) {
    #cph-chat-button {
      bottom: 16px;
      right: 16px;
      padding: 10px 16px;
    }
    
    #cph-chat-container {
      width: calc(100% - 32px);
      height: 80vh;
      bottom: 80px;
      right: 16px;
      left: 16px;
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
  <iframe id="cph-chat-iframe" src="https://pickle-gobi-pizza.emergent.host"></iframe>
</div>

<script>
  function toggleCPHChat() {
    var container = document.getElementById('cph-chat-container');
    container.classList.toggle('open');
  }
</script>
<!-- End Curry Pizza House Chat Widget -->
```

---

## 🎨 Preview

### Button (Bottom-Right Corner):
```
┌─────────────────────────────────┐
│                                 │
│    Your currypizzahouse.com     │
│         website content         │
│                                 │
│                 ┌─────────────┐ │
│                 │ 💬 Ask AI   │ │
│                 └─────────────┘ │
└─────────────────────────────────┘
```

### When Clicked (Chat Opens):
```
┌─────────────────────────────────┐
│              ┌────────────────┐ │
│              │ 🍕 Curry Pizza │ │
│              │ AI Assistant   │ │
│              │                │ │
│              │ Chat messages  │ │
│              │ appear here... │ │
│              │                │ │
│              │ [Quick Actions]│ │
│              │ [Input Field]  │ │
│              └────────────────┘ │
│                 ┌─────────────┐ │
│                 │ 💬 Ask AI   │ │
│                 └─────────────┘ │
└─────────────────────────────────┘
```

---

## 🛠️ Installation Steps

### For WordPress:
1. Go to **Appearance → Theme Editor → footer.php**
2. Paste the code before `</body>`
3. Click **Update File**

### For Squarespace:
1. Go to **Settings → Advanced → Code Injection**
2. Paste in the **Footer** section
3. Save

### For Wix:
1. Go to **Settings → Custom Code**
2. Add new code to **Body - End**
3. Apply to **All pages**

### For Shopify:
1. Go to **Online Store → Themes → Edit Code**
2. Find **theme.liquid**
3. Paste before `</body>`
4. Save

---

## ✏️ Customization

### Change Button Text:
```html
<span>Ask AI</span>
```
Change to: "Chat", "Need Help?", "Menu Assistant", etc.

### Change Colors:
```css
background: linear-gradient(135deg, #FF6B00 0%, #E63900 100%);
```
- `#FF6B00` = Orange
- `#E63900` = Red-Orange

### Change Position (Left Side):
```css
#cph-chat-button {
  right: auto;
  left: 24px;
}

#cph-chat-container {
  right: auto;
  left: 24px;
}
```

---

## 🔄 URL Change

**Current:** `pickle-gobi-pizza.emergent.host`
**Desired:** `cph-ai-assistant.emergent.host`

Contact: **support@emergentagent.com**

---

## 📱 Features

- ✅ **Chat-only interface** - No landing page
- ✅ **Mobile responsive** - Works on all devices
- ✅ **Quick action buttons** - Show menu, Vegetarian options, Popular pizzas, Wings, Allergen info
- ✅ **AI-powered** - Answers questions about menu, ingredients, allergens
- ✅ **No prices shown** - Directs to website for pricing
- ✅ **Popular pizzas categorized** - Indian Craft, Regular Standard

---

## 📞 Support

- **Emergent Platform:** support@emergentagent.com
- **Curry Pizza House:** www.currypizzahouse.com
