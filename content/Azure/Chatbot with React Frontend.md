---
title: "Building an AI-Powered App Using Azure OpenAI Services"
date: 2025-06-23
draft: false
tags: ["azure", "vm", "resize", "cloud", "beginner-guide"]
categories: ["azure", "cloud"]
---

🔹 1️⃣ Introduction to Azure OpenAI
In today’s cloud-native world, many organizations want to add AI features like chatbots, summarization, sentiment analysis, and document Q&A into their apps. Azure OpenAI Services makes this easy by giving secure, enterprise access to powerful models like GPT-4, ChatGPT, and DALL·E via REST APIs — all hosted in Microsoft’s trusted Azure cloud.

Benefits:

No need to host large AI models yourself

Microsoft’s enterprise security and compliance

Pay as you go

Available in various regions globally

In this post, you’ll learn how to build an AI-powered chatbot using:
✅ Azure OpenAI
✅ React.js frontend
✅ FastAPI backend
✅ Secured with Azure Active Directory

🔹 2️⃣ Getting API Keys and Setup
a) Prerequisites
Azure Subscription

OpenAI resource created in Azure

React and Node installed

Python 3.10+ installed

b) Create OpenAI Resource
Go to Azure Portal → Create Resource → Azure OpenAI

Select Region (e.g. East US or West Europe)

Select Pricing Tier

Deploy → Once deployed, navigate to Keys & Endpoint

You’ll get:

AZURE_OPENAI_API_KEY

AZURE_OPENAI_ENDPOINT

c) Example Environment Variables (Backend)
env
Copy
Edit
AZURE_OPENAI_API_KEY=xxxxx
AZURE_OPENAI_ENDPOINT=https://xxxxxx.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_TENANT_ID=xxxxx
AZURE_CLIENT_ID=xxxxx
AZURE_CLIENT_SECRET=xxxxx
🔹 3️⃣ Sample App: Chatbot with React Frontend
a) Backend with FastAPI
main.py

python
Copy
Edit
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2023-05-15"

@app.post("/chat")
async def chat(request: dict):
    try:
        messages = request.get("messages", [])
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=messages,
            max_tokens=500
        )
        return {"response": response.choices[0].message["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
b) React Frontend (Chat UI)
ChatApp.jsx

jsx
Copy
Edit
import React, { useState } from 'react';
import axios from 'axios';

function ChatApp() {
  const [messages, setMessages] = useState([{ role: "system", content: "You are a helpful assistant." }]);
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');

  const handleSend = async () => {
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);

    try {
      const res = await axios.post('/chat', { messages: newMessages });
      setResponse(res.data.response);
      setMessages([...newMessages, { role: "assistant", content: res.data.response }]);
      setInput('');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>AI Chatbot with Azure OpenAI</h1>
      <div style={{ border: '1px solid #ccc', padding: '10px', height: '300px', overflowY: 'auto' }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ margin: '5px 0' }}>
            <b>{msg.role}: </b> {msg.content}
          </div>
        ))}
      </div>
      <input value={input} onChange={e => setInput(e.target.value)} style={{ width: '80%', padding: '10px' }} />
      <button onClick={handleSend} style={{ padding: '10px', marginLeft: '5px' }}>Send</button>
    </div>
  );
}

export default ChatApp;
🔹 4️⃣ Securing APIs with Azure AD
In enterprise apps, you won’t expose the OpenAI API directly. Instead:

Secure your FastAPI backend using Azure AD tokens

Only authenticated users can call /chat

FastAPI Example with Azure AD:

python
Copy
Edit
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

bearer_scheme = HTTPBearer()

@app.post("/chat")
async def chat(request: dict, token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # Validate token (you can use MSAL or Azure AD JWT validation libraries)
    # If token valid:
    return actual_chat_logic()
🔹 5️⃣ Use Cases and Limitations
✅ Common Use Cases
Chatbots for customer support

AI assistants in enterprise apps

Document summarization

Sentiment analysis

Q&A over internal knowledge bases

⚠️ Limitations
Cost: OpenAI usage can get expensive at scale

API rate limits per subscription

No control over the model weights (black box)

Always validate AI outputs — do not blindly trust!

Requires correct prompt engineering to get the best results

🔹 Conclusion
You’ve now seen an end-to-end architecture:
✅ React Chat frontend
✅ FastAPI secured backend
✅ Azure OpenAI services
✅ Azure AD authentication

