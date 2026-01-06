import { useState, useRef, useEffect } from "react";
import "@/App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Chat message component
const ChatMessage = ({ message, isUser }) => (
  <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
    {!isUser && (
      <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center mr-2 flex-shrink-0">
        <span role="img" aria-label="pizza">🍕</span>
      </div>
    )}
    <div
      className={`max-w-[85%] px-4 py-3 rounded-2xl ${
        isUser
          ? 'bg-orange-500 text-white rounded-br-md'
          : 'bg-gray-100 text-gray-800 rounded-bl-md'
      }`}
      data-testid={isUser ? 'user-message' : 'bot-message'}
    >
      <p className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
      <span className="text-xs opacity-60 mt-1 block">
        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </span>
    </div>
  </div>
);

// Quick action button component
const QuickAction = ({ text, onClick }) => (
  <button
    onClick={onClick}
    className="px-4 py-2 rounded-full text-sm font-medium bg-white border border-gray-200 text-gray-700 hover:border-orange-400 hover:text-orange-600 hover:bg-orange-50 transition-all whitespace-nowrap"
    data-testid={`quick-action-${text.toLowerCase().replace(/\s+/g, '-')}`}
  >
    {text}
  </button>
);

// Main Chat Widget
const ChatWidget = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! Welcome to Curry Pizza House! 🍕\n\nI'm your AI menu assistant. I can help you with:\n• Pizza menu & toppings\n• Vegetarian options\n• Allergen information\n• Wings & appetizers\n\nWhat would you like to know?",
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
    'Wings',
    'Allergen info'
  ];

  return (
    <div className="w-full h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-4 py-4 flex items-center justify-between shadow-md">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <span role="img" aria-label="pizza" className="text-xl">🍕</span>
          </div>
          <div>
            <h1 className="font-bold text-lg">Curry Pizza House</h1>
            <p className="text-xs text-orange-100">AI Menu Assistant</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
          <span className="text-xs">Online</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4" data-testid="messages-container">
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
      <div className="px-4 py-3 bg-white border-t border-gray-100 flex gap-2 overflow-x-auto">
        {quickActions.map((action) => (
          <QuickAction
            key={action}
            text={action}
            onClick={() => sendMessage(action)}
          />
        ))}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 bg-white border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask about our pizzas..."
            className="flex-1 px-4 py-3 border border-gray-200 rounded-full focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100 text-sm"
            disabled={isLoading}
            data-testid="chat-input"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="w-12 h-12 bg-orange-500 text-white rounded-full flex items-center justify-center hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-md"
            data-testid="send-button"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" />
            </svg>
          </button>
        </div>
        <p className="text-xs text-gray-400 text-center mt-2">
          Powered by Curry Pizza House AI • <a href="https://www.currypizzahouse.com" target="_blank" rel="noopener noreferrer" className="text-orange-500 hover:underline">Order Online</a>
        </p>
      </form>
    </div>
  );
};

function App() {
  return <ChatWidget />;
}

export default App;
