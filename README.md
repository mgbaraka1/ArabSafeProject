# ArabSafe

**ArabSafe** is a cybersecurity research project aimed at evaluating the vulnerabilities of Large Language Models (LLMs) to **jailbreaking attacks** using **Arabic prompts** across three dialects:  
- **Modern Standard Arabic (MSA)**  
- **Egyptian (Cairene)**  
- **Saudi (Najdi)**

The project includes dataset preparation, dialect translation, LLM interaction, response classification, and risk categorization to better understand the safety gaps of LLMs in the Arabic linguistic context.

---

## Project Overview

This repository contains the source code, database schema, attack pipeline, and evaluation tools developed for the ArabSafe project as part of a Cybersecurity Master's thesis at King Saud University.

### Key Features

- Structured SQLite database for prompt storage and metadata tracking
- Multi-dialect translation using DeepL, OpenAI, and ALLaM
- LLM attack automation scripts (OpenAI, Claude, Gemini, DeepSeek, Qwen, and ALLaM)
- Categorization of harmful content into 12 security risk domains
- Flask web interface for human review and scoring
- Statistical export and performance measurement

---

## Database Hugging Face URL
https://huggingface.co/datasets/mgbaraka/ArabSafe

---
