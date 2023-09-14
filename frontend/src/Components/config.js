import UMLRenderer from './UMLRenderer';
import { createChatBotMessage } from 'react-chatbot-kit';


const config = {
  initialMessages: [createChatBotMessage
    (`Hi! I'm GPT-PPT, please share your design idea with me and watch me generate a design document and a UML diagram for you!`)],
  widgets: [
    {
      widgetName: 'umlRenderer',
      widgetFunc: (props) => <UMLRenderer {...props} />,
    },
  ],
};

export default config;