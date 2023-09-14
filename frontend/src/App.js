import React from "react";
import Chatbot from 'react-chatbot-kit'

import "./App.css";
import 'react-chatbot-kit/build/main.css'

import ActionProvider from './Components/ActionProvider';
import MessageParser from './Components/MessageParser';
import config from './Components/config';


function App() {

  return <Chatbot style={{innerHeight: "100%", outerHeight: "100%", }} config={config} actionProvider={ActionProvider}  messageParser={MessageParser}
        />;

}

export default App;
