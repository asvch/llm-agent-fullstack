import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const chatContainerRef = useRef(null);


  const sendMessage = async () => {
    if (input.trim() === '') return;

    // set input to blank after clicking Enter
    setInput('');

    const userMessage = { sender: 'user', text: input };

    setMessages([...messages, userMessage]);


    try {
      // const response = await axios.post('http://localhost:8000/invoke', {
      const response = await axios.post('https://llm-agent-fullstack-production.up.railway.app/invoke', {
        "input": {
          "input": input
        },
        "config": {
          "configurable": {
            "session_id": ""
          }
        },
        "kwargs": {}
      });
      console.log('API Response:', response.data);
      const botMessage = { sender: 'bot', text: response.data.output.output };

      setMessages([...messages, userMessage, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);
    }

    scrollToBottom();  // scroll to bottom after sending message
  };

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  };

   useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-container">
      <div className="chat-box" ref={chatContainerRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default App;