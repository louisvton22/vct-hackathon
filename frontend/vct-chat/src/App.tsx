import React from 'react';
import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import axios from 'axios';
type Message = {
  role: 'user' | 'bot';
  content: string;
};


function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');

  // Handle message input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  // Send new message to the server and receive LLM response
  const handleSend = async () => {
    if (!input) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      // Send user input to LLM endpoint
      const response = await axios.post('http://localhost:5000/', { prompt: input });

      const botMessage: Message = { role: 'bot', content: response.data.reply };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
      setInput('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="App">
      <h1>VCT Assistant Chat Interface</h1>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You' : 'Bot'}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <input type="text" value={input} onChange={handleChange} placeholder="Type your message..." />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default App;
