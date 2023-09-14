// in ActionProvider.jsx
import React from 'react';
import axios from "axios";

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const handleHello = () => {
    const botMessage = createChatBotMessage('Hello. Nice to meet you.');

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, botMessage],
    }));
  };

  const handleDog = (message) => {
    axios.get('http://127.0.0.1:5000/gpt?text_input=' + message).then((response) => {
      console.log(response.data['document']);
      console.log(response.data['diagram']);
      const botMessage = createChatBotMessage(response.data['document'], {
        widget: 'umlRenderer',
        payload: response.data['diagram']
      });
      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, botMessage],
      }));
    });
  };

  // Put the handleHello function in the actions object to pass to the MessageParser
  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleHello,
            handleDog
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;