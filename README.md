## LLM Agent chatbot with access to multiple tools!
  - LangChain, LangServe, FastAPI, and OpenAI API used for backend.
  - React.js, and HTML used for frontend.
  - Elasticsearch database as external vectorstore.
  - Chatbot acts as Romeo from Romeo and Juliet.
  - Deployed backend using Railway.app and frontend using GitHub Pages.
  
**LLM Agent Tools:**
- Retrieval tool: for LLM Agent to access all of Romeo's lines from the original script. Agent uses this tool to answer questions about Romeo.
- Web Search tool: Tavily Search API used to search information our LLM Agent does not know (including current events.)
- Weather tool: accessed through weather API, to find current weather conditions in a city.
- Math tool: used to answer math questions.
- YouTube search tool: used to find YouTube video URLs.
 
Preview:
| Backend      | Frontend |
| ----------- | ----------- |
| ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/844e83d5-e898-4cbe-b620-5218dc9074b4) | <img src="https://github.com/asvch/llm-agent-fullstack/assets/66492476/23722a4a-4b2b-47ac-883c-cd8749dc358b" width="400" height="400"> |
| Retrieval tool: <br> ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/44eb6029-5c33-47e0-995f-3289e9a2522e) <br> ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/476b7be1-a1f9-425d-ab16-2d396bce22c9) | ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/5da001c3-e601-4c03-9291-2a249f2aef53)|
| Weather tool: <br> ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/148f50a7-a769-4d23-9919-94754551cfde) |![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/142528eb-ff8b-46aa-b8f2-9774663fd0ea)|
| Web Search tool: <br> ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/95533633-6604-482f-b3ef-cafbfd300ca9) <br> ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/1a53e9f2-38db-47fb-985e-3a352b93b29e) | ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/da7114a2-4821-48f3-b7ae-fef596ffe831) |
| Math tool: <br> ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/ea21311d-c35b-4d3a-b5d1-392caffd24ad) | ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/7cbd005e-d543-439c-863f-afdc23348daa) |
| YouTube tool: ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/a5734635-221e-4484-8d95-e6a30642ad56) | ![image](https://github.com/asvch/llm-agent-fullstack/assets/66492476/f1eeedca-752c-4cf2-943d-2907aedd46ad) |
