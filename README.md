# bachelor-project
AI-powered chatbot based on the database of an online shopping platform

## Overview
This project represents my bachelor thesis and consists of an AI-powered chatbot designed for an online sneaker store.  
The chatbot provides automated responses to user queries related to products, availability, prices, and general store information, using a rule-based approach combined with basic NLP techniques.

The system is developed with a focus on simplicity, performance, and independence from external APIs.


## Key Features
- Automated responses based on a local product database
- Natural language processing for user intent detection
- Product filtering by brand, model, size, and price
- REST API backend built with FastAPI
- SQL-based data storage for products
- Web-based chat interface inspired by Telegram UI


## Technologies Used
- **Backend:** Python, FastAPI  
- **NLP:** spaCy (rule-based intent matching)  
- **Database:** SQL (local database)  
- **Frontend:** HTML, CSS  
- **Architecture:** REST API  


## System Architecture
- The backend processes user messages and extracts relevant attributes using NLP.
- User queries are matched against predefined rules and database records.
- The chatbot returns structured and relevant responses based on available data.
- No external APIs are used for AI responses.
