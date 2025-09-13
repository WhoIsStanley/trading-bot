# Trading Bot

A Discord bot for tracking stock information and creating alerts. This bot uses Discord.py, yfinance, and Discord UI components for interactive menus.

---

## Latest Updates

**Version 1.1** - September 2025

## Features

### Stock Commands
- **Interactive Stock Search**
  - If a ticker is invalid, the bot shows a search menu with buttons to select the correct stock.
- **Pre/Post Market Handling**
  - Automatically shows pre-market or post-market prices when available.
- **Stock Embed Details**
  - Current Price  
  - Price Change & %  
  - Volume  
  - Open / Previous Close  
  - 52-week High / Low  
  - P/E Ratio & EPS  

---

### Alerts
- Custom alert system for stocks.
- Set alerts for specific price thresholds or percentage changes.
- Receive notifications directly in Discord when conditions are met.
- Multiple alerts per stock supported.
- Cancel, edit, or view existing alerts via Discord commands.

---

### Help Command
- A **new help command** lists all available commands in a neat embed.

---

## Bug Fixes
- Clicking the **Cancel button** on interactive embeds now properly closes the embed and disables buttons.

## Source / References
- **Discord.py** - [https://discordpy.readthedocs.io/](https://discordpy.readthedocs.io/)
- **yfinance (Yahoo Finance API)** - [https://pypi.org/project/yfinance/](https://pypi.org/project/yfinance/)