import React from 'react';
import axios from "axios";

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const handleInput = (message) => {
    axios.get('http://127.0.0.1:5000/gpt?text_input=' + message).then((response) => {
      console.log(response.data['output_gpt']);
      const botMessage = createChatBotMessage(response.data['output_gpt']['DesignDoc']['Intent'], {
        widget: 'umlRenderer',
        payload: {"diagram": response.data['diagram'],"document": response.data['document']}
      });
      setState((prev) => ({
        ...prev,
        messages: [...prev.messages, botMessage],
      }));
    });
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleInput
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;