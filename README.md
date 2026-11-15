# Battleship: Online Multiplayer in Python

A two-player online Battleship game with a client–server architecture, built from scratch in Python.

- **Server** (`ServerSide/`): a threaded TCP server that pairs players into lobbies and relays game events.
  Shared state is protected by locks, and the server ships as a Docker image.
- **Client** (`ClientSide/`): a desktop app in CustomTkinter, organized as MVC with login, ship setup and game views.
- **Protocol**: JSON events built by a shared `EventFactory`, so both sides speak the same message format.
- **Model** (`model/`): board logic with unit tests (`BoardTest.py`).

## Run

```bash
pip install -r requirements.txt
python Main.py -s        # start the server on port 5555
python Main.py           # start a client (run one per player)
```

Or run the server in Docker:

```bash
docker build -t battleship . && docker run -p 5555:5555 battleship
```
