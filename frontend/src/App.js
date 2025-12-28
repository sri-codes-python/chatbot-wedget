import { useState, useRef, useEffect } from "react";
import "@/App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Pizza emoji component
const PizzaIcon = () => (
  <svg viewBox="0 0 100 100" className="w-12 h-12">
    <circle cx="50" cy="50" r="45" fill="#F5A623" />
    <circle cx="30" cy="35" r="8" fill="#D32F2F" />
    <circle cx="55" cy="30" r="6" fill="#D32F2F" />
    <circle cx="70" cy="50" r="7" fill="#D32F2F" />
    <circle cx="45" cy="60" r="8" fill="#D32F2F" />
    <circle cx="25" cy="55" r="5" fill="#388E3C" />
    <circle cx="60" cy="65" r="4" fill="#388E3C" />
    <path d="M50 5 L95 85 L5 85 Z" fill="none" stroke="#E65100" strokeWidth="3" />
  </svg>
);

// Chat message component
const ChatMessage = ({ message, isUser }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
    {!isUser && (
      <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center mr-2 flex-shrink-0">
        <span role="img" aria-label="pizza">🍕</span>
      </div>
    )}
    <div
      className={`max-w-[80%] px-4 py-3 rounded-2xl ${
        isUser
          ? 'bg-orange-500 text-white rounded-br-md'
          : 'bg-gray-100 text-gray-800 rounded-bl-md'
      }`}
      data-testid={isUser ? 'user-message' : 'bot-message'}
    >
      <p className="text-sm whitespace-pre-wrap">{message.content}</p>
      <span className="text-xs opacity-70 mt-1 block">
        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </span>
    </div>
  </div>
);

// Quick action button component
const QuickAction = ({ text, onClick, active }) => (
  <button
    onClick={onClick}
    className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
      active
        ? 'bg-orange-500 text-white'
        : 'bg-white border border-gray-200 text-gray-700 hover:border-orange-300 hover:text-orange-600'
    }`}
    data-testid={`quick-action-${text.toLowerCase().replace(/\s+/g, '-')}`}
  >
    {text}
  </button>
);

// Chat widget component
const ChatWidget = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Welcome to Curry Pizza House! 🍕\n\nI'm your menu assistant. Ask me about our pizzas, toppings, allergens, or prices!",
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        session_id: sessionId,
        message: text
      });

      const botMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(response.data.timestamp)
      };

      setMessages(prev => [...prev, botMessage]);
      if (!sessionId) {
        setSessionId(response.data.session_id);
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        role: 'assistant',
        content: "I'm sorry, I'm having trouble connecting right now. Please try again in a moment! 🙏",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(inputValue);
  };

  const quickActions = [
    'Show menu',
    'Vegetarian options',
    'Popular pizzas',
    'Help'
  ];

  if (!isOpen) return null;

  return (
    <div 
      className="fixed bottom-44 right-6 w-96 h-[500px] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-100"
      style={{ zIndex: 10001 }}
      data-testid="chat-widget"
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white p-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <span role="img" aria-label="pizza" className="text-xl">🍕</span>
          </div>
          <div>
            <h3 className="font-bold">Curry Pizza House</h3>
            <p className="text-xs text-orange-100">Menu Assistant</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          <span className="text-xs">Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50" data-testid="messages-container">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} isUser={msg.role === 'user'} />
        ))}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center mr-2">
              <span role="img" aria-label="pizza">🍕</span>
            </div>
            <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="px-4 py-2 bg-white border-t border-gray-100 flex gap-2 overflow-x-auto">
        {quickActions.map((action) => (
          <QuickAction
            key={action}
            text={action}
            onClick={() => sendMessage(action)}
          />
        ))}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 bg-white border-t border-gray-100">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask about our pizzas..."
            className="flex-1 px-4 py-2 border border-gray-200 rounded-full focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100"
            disabled={isLoading}
            data-testid="chat-input"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="w-10 h-10 bg-orange-500 text-white rounded-full flex items-center justify-center hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            data-testid="send-button"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
            </svg>
          </button>
        </div>
        <p className="text-xs text-gray-400 text-center mt-2">Powered by Curry Pizza House AI</p>
      </form>
    </div>
  );
};

// Feature card component
const FeatureCard = ({ icon, title, description }) => (
  <div className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow border border-gray-100" data-testid="feature-card">
    <div className="text-4xl mb-4">{icon}</div>
    <h3 className="font-bold text-lg mb-2 text-gray-800">{title}</h3>
    <p className="text-gray-600 text-sm">{description}</p>
  </div>
);

// Main Home component
const Home = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 to-white">
      {/* Header */}
      <header className="py-8 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex items-center justify-center gap-4 mb-4">
            <PizzaIcon />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
              Curry Pizza House
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Authentic Indian flavors meet classic pizza perfection</p>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl p-8 text-white shadow-xl">
          <h2 className="text-3xl font-bold mb-4">Welcome to Our Demo!</h2>
          <p className="text-orange-100 mb-6">
            Try our AI-powered menu assistant! Click the chat button in the bottom-right corner to:
          </p>
          <ul className="space-y-2">
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 bg-white rounded-full"></span>
              Browse our complete pizza menu
            </li>
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 bg-white rounded-full"></span>
              Ask about ingredients and toppings
            </li>
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 bg-white rounded-full"></span>
              Get allergen and dietary information
            </li>
            <li className="flex items-center gap-2">
              <span className="w-2 h-2 bg-white rounded-full"></span>
              Check prices and sizes
            </li>
          </ul>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-4xl mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-6">
          <FeatureCard
            icon="🌶️"
            title="Signature Curry Pizzas"
            description="Experience unique fusion flavors with our specialty curry-inspired pizzas"
          />
          <FeatureCard
            icon="🌱"
            title="Vegetarian Options"
            description="Extensive selection of delicious vegetarian pizzas with fresh ingredients"
          />
          <FeatureCard
            icon="🥛"
            title="Allergen Info"
            description="Complete transparency with dairy, gluten, and allergen information"
          />
        </div>
      </section>

      {/* Popular Items Preview */}
      <section className="max-w-4xl mx-auto px-4 py-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Popular Picks</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-white rounded-xl p-5 shadow-md border border-gray-100 hover:border-orange-200 transition-colors">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold text-lg text-gray-800">Achari Gobhi Pizza ⭐</h3>
                <p className="text-gray-600 text-sm mt-1">Pickle-spiced cauliflower with tangy achari masala</p>
                <div className="flex gap-2 mt-2">
                  <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">Vegetarian</span>
                  <span className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full">Popular</span>
                </div>
              </div>
              <span className="text-orange-600 font-bold">$12.99+</span>
            </div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-md border border-gray-100 hover:border-orange-200 transition-colors">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-bold text-lg text-gray-800">Butter Chicken Pizza ⭐</h3>
                <p className="text-gray-600 text-sm mt-1">Creamy butter chicken with bell peppers and cilantro</p>
                <div className="flex gap-2 mt-2">
                  <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full">Bestseller</span>
                </div>
              </div>
              <span className="text-orange-600 font-bold">$14.99+</span>
            </div>
          </div>
        </div>
      </section>

      {/* Chat Toggle Button */}
      <button
        onClick={() => setIsChatOpen(!isChatOpen)}
        className="fixed bottom-24 right-6 w-14 h-14 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-full shadow-lg hover:shadow-xl transition-all flex items-center justify-center hover:scale-105"
        style={{ zIndex: 10000 }}
        data-testid="chat-toggle-button"
      >
        {isChatOpen ? (
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
          </svg>
        )}
      </button>

      {/* Chat Widget */}
      <ChatWidget isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
    </div>
  );
};

function App() {
  return <Home />;
}

export default App;
