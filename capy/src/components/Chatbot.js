import React, { useState } from 'react';
import axios from 'axios';
import '../styles/Chatbot.css';

// Set the base URL for Axios
axios.defaults.baseURL = 'http://127.0.0.1:5000';

const Chatbot = () => {
  const [message, setMessage] = useState('');
  const [conversation, setConversation] = useState([]);

  const handleInputChange = (event) => {
    setMessage(event.target.value);
  };

  // Inside the handleSendMessage function
  const handleSendMessage = async () => {
    if (message.trim() !== '') {
      const userMessage = { text: message, isUser: true };
      setConversation((prevConversation) => [...prevConversation, userMessage]);
      setMessage('');

      try {
        const response = await axios.post('/chat', { message: message });
        const botMessage = { text: response.data, isUser: false };
        setConversation((prevConversation) => [...prevConversation, botMessage]);
      } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h2>Chatbot</h2>
      </div>
      <div className="chatbot-conversation">
        {conversation.map((msg, index) => (
          <div
            key={index}
            className={`chatbot-message ${msg.isUser ? 'user-message' : 'bot-message'}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chatbot-input">
        <input
          type="text"
          value={message}
          onChange={handleInputChange}
          placeholder="Type your message..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;