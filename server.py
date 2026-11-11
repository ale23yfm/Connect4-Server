import asyncio, os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed
from domain.board import Board
from service.game import GameService
from errors.errors import InvalidColumn, ColumnFullError, GameServiceError

from http import HTTPStatus
from pathlib import Path


BASE = Path(__file__).parent
FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/script.js": ("script.js", "application/javascript; charset=utf-8"),
}

def render(board, message=""):
    text = "1 2 3 4 5 6 7\n" + str(board)
    return (message + "\n" + text) if message else text

async def run_game(ws):
    print("Connected")
    board = Board()
    service = GameService(board)
    try:
        await ws.send("Choose mode (ALGORITHM or AI):")
        while True:
            data = (await ws.recv()).strip().upper()
            if data in ("ALGORITHM", "AI"):
                mode = data
                service.set_mode(mode)
                break
            await ws.send("Invalid mode. Choose mode (ALGORITHM or AI):")

        await ws.send("Choose a piece (beige or red):")
        while True:
            data = await ws.recv()
            try:
                service.choose_piece(data.strip().upper())
                break
            except ValueError:
                await ws.send("Invalid piece. Choose a piece (beige or red):")

        if service._computer_piece == "X":
            service.computer_move()

        await ws.send(render(board) + "\nChoose a column (1-7):")

        while not service._game_over:
            data = await ws.recv()
            message = ""
            try:
                service.make_move(int(data.strip()) - 1)
            except ValueError:
                message = "Invalid input: not an integer."
            except (InvalidColumn, ColumnFullError):
                message = "Invalid column, try again."
            except GameServiceError as e:
                message = str(e)

            if service._game_over:
                if service._winner == "X":
                    message = "Game over! Winner: Beige"
                elif service._winner == "O":
                    message = "Game over! Winner: Red"
                else:
                    message = "Game over! Draw!"
            else:
                message += "\nChoose a column (1-7):"

            await ws.send(render(board, message.strip()))
    except ConnectionClosed:
        print("Client dropped")

async def process_request(connection, request):
    if request.headers.get("Upgrade", "").lower() == "websocket":
        return None  # let WebSocket connections through
    path = request.path.split("?")[0]
    if path in FILES:
        name, ctype = FILES[path]
        response = connection.respond(HTTPStatus.OK, (BASE / name).read_text(encoding="utf-8"))
        response.headers["Content-Type"] = ctype
        return response
    return connection.respond(HTTPStatus.NOT_FOUND, "Not found\n")

async def main():
    port = int(os.environ.get("PORT", 5988))
    async with serve(run_game, "0.0.0.0", port, process_request=process_request):
        print("Server is waiting for connections...")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())