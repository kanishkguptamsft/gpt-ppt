import UMLRenderer from './UMLRenderer';
import { createChatBotMessage } from 'react-chatbot-kit';


const config = {
  initialMessages: [createChatBotMessage(`Hi! I'm GPT-PPT`)],
  widgets: [
    {
      widgetName: 'umlRenderer',
      widgetFunc: (props) => <UMLRenderer {...props} />,
    },
  ],
};

export default config;