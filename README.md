# Solgard Discord Bot

Welcome to the Solgard Discord Bot repository. This bot is designed to bring a range of useful features to Discord servers for the game [Solgard](https://snowprintstudios.com/solgard/).

## Features

- **Connect:** Connect to the game using Python.
- **Attacks/Bombs remining:** The bot can display the remaining bombs and attacks on Discord.
- **Clash infos:** The bot can provide information about the remaining attacks and the current score on Discord.
- **Interpolate powers:** The bot utilizes machine learning to predict powers for clashes, with linear or polynomial implementation.
- **Assign target clash** Use the Kuhn Munkres algorithm to minimize power differences and assign targets for clashes.
- **Traduction** The bot can communicate in French, English, Italian, Spanish, Chinese, and Russian. 


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


3. **Set entrypoint**

    - open the file app/core/entrypoint/connect.exemple.json
    - rename the file connect.exemple.json in connect.json
    - insert your CONNECT json (use a mitm with a proxy for get it)

4. **Set your .env file**

    - Open the file create_env.py.
    - Execute it.
    - You .env is created, you connect.json is now encrypted in the .env, use that for environnement variable for deployement.
    - Add your bot token : `BOT_TOKEN=your-bot-token-here`
     
4. **Run the bot**

    You can now run the bot using the following command:

    ```python
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



