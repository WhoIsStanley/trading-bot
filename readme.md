# Trading Bot

A Discord bot for tracking stock information and creating alerts. This bot uses Discord.py, yfinance, and Discord UI components for interactive menus.

---

## Latest Updates

**Version 1.0** - September 2025

### Add Stock Command
- Users can search for stock tickers with the bot.
- Interactive buttons (**YahooSearchView**) display search results.
- Buttons fetch **live stock data** using `yfinance` when clicked.
- Embed safely handles missing fields:
  - Shows `N/A` if price, change, or percentage change is unavailable.
- Fixed file attachment issues in message edits:
  - Use `attachments=[file]` instead of `file=file`.
- Timeout behavior improved:
  - Buttons are **greyed out** after 30 seconds.
  - Disabled buttons are reflected in the original message.

### Finishing Alert Command
- Users can **complete or cancel alerts** after creation.
- Canceling an alert disables the interactive menu and shows a confirmation message.
- Only the user who created the alert can interact with the menu to prevent others from interfering.
- Ensures safe handling of any files or embeds associated with the alert.

## Source / References
- **Discord.py** - [https://discordpy.readthedocs.io/](https://discordpy.readthedocs.io/)
- **yfinance (Yahoo Finance API)** - [https://pypi.org/project/yfinance/](https://pypi.org/project/yfinance/)