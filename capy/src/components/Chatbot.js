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
    
    <div className="chatbot-container " >

      <div className="chatbot-header text-tab_border_brown font-mitr " >
      <style>{'body { background-color: #F8DEC1; }'}</style>

        <h2 style={{marginTop:"-40px", marginLeft:"-130px"}}>Chat with Capy</h2>
      </div>
      <div className="chatbot-conversation text-text_brown font-ntr">
        {conversation.map((msg, index) => (
          <div
            key={index}
            className={`chatbot-message ${msg.isUser ? 'user-message' : 'bot-message'}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chatbot-input text-text_brown font-mitr" >
        <input
          type="text"
          value={message}
          onChange={handleInputChange}
          style={{ backgroundColor: "#F8DEC1" , color: "#6D4520", marginRight: "-30px", borderColor:"#6D4520", borderWidth:"2px"}}
          placeholder="Type your message..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;