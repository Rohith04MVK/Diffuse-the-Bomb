# Bomb Diffusion Challenge

A timed, puzzle-based web application where users race against the clock to "defuse a bomb" by solving a series of challenges. This project is built with Flask and SQLAlchemy, featuring procedurally generated puzzles for each user.

## Features

-   **5 Unique Puzzles**: Each user gets a unique, procedurally generated set of five puzzles.
-   **Timed Missions**: Player sessions are timed from their first login to the moment they solve the final puzzle.
-   **Persistent Progress**: The application uses a SQLite database to save user progress, so you can pick up where you left off.
-   **Global Leaderboard**: Compare your mission completion time with other agents on the leaderboard.
-   **Retro Terminal Aesthetic**: A fun, immersive interface styled to look like a vintage computer terminal.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing.

### Prerequisites

-   Python 3.13 or newer.
-   [UV](https://github.com/astral-sh/uv) - An extremely fast Python package installer and resolver.

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/bomb-diffusion.git
    cd bomb-diffusion
    ```

2.  **Create a virtual environment and install dependencies using UV:**
    This command creates a virtual environment in a `.venv` directory and installs the packages listed in [`pyproject.toml`](pyproject.toml).
    ```sh
    uv pip sync
    ```

3.  **Activate the virtual environment:**
    -   On macOS and Linux:
        ```sh
        source .venv/bin/activate
        ```
    -   On Windows:
        ```sh
        .venv\Scripts\activate
        ```

4.  **Initialize the database:**
    The application includes a command to set up the necessary database tables.
    ```sh
    flask init-db
    ```
    This will create an `app.db` file in your project root.

5.  **Run the application:**
    You can run the app using the built-in Flask development server.
    ```sh
    flask run
    ```
    The application will be available at `http://127.0.0.1:5000`. Open this URL in your browser to start your mission.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a new puzzle idea, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingPuzzle`)
3.  Commit your Changes (`git commit -m 'Add some AmazingPuzzle'`)
4.  Push to the Branch (`git push origin feature/AmazingPuzzle`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

Made with ❤️