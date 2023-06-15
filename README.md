# Solgard Discord Bot

Welcome to the Solgard Discord Bot repository. This bot is designed to bring a range of useful features to Discord servers for the game [Solgard](https://www.solgardgame.com).

## Features

- **Connect:** Connect yourself to the game with python 
- **Attacks/Bombs remining:** The bot can say in discord remining bombs and attacks
- **Clash infos:** The bot can say in discord remining attacks and actual score


## Installation

1. **Clone the repository**

   Run the following command in your terminal to clone this repository:

   ```bash
   git clone https://github.com/AlexTraveylan/solgard-bot-last-refactoring.git
   ```

2. **Install the dependencies**

    Navigate into the cloned repository, create and activated venv and install dependencies :

    - windows
    ```powershell
    cd solgard-bot-last-refactoring
    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt
    ```
    - linux
    ```bash
    cd solgard-bot-last-refactoring
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```


3. **Set up your Discord Bot Token**

    Create a `.env` file in the root directory and set your Discord bot token like so:

    ```
    PYTHONPATH=.
    BOT_TOKEN=your-bot-token-here
    ```
    Replace `your-bot-token-here` with your actual bot token.

4. **Set entrypoint**

    - open the file app/entrypoint/connect.exemple.json
    - rename the file connect.exemple.json in connect.json
    - insert your CONNECT json (use a mitm with a proxy for get it)
     
5. **Run the bot**

    You can now run the bot using the following command:

    ```
    python app/main.py
    ```


## Contributing

We welcome contributions to the Solgard Discord Bot! 
- AlexTraveylan
- Soear

## License

This project is open source.

## Contact

If you have any questions, comments, or concerns, feel free to open an issue on this repository.



