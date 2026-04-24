import socket
import json
import random

QUESTIONS = {
    "What is the capital of France?": "Paris",
    "What is the largest mammal on Earth?": "Whale",
    "What is the chemical symbol for gold?": "Au",
    "What is the currency of Japan?": "Yen",
    "What is the largest planet in our solar system?": "Jupiter",
    "What is the smallest country in the world?": "Vatican City",
    "What is the largest ocean on Earth?": "Pacific Ocean",
    "What is the largest desert in the world?": "Antarctica",
    "What is the largest rainforest in the world?": "Amazon Rainforest",
    "What is the largest mountain in the world?": "Mount Everest"
}

class Player:
    def __init__(self, conn, addr, name):
        self.conn = conn
        self.addr = addr
        self.name = name
        self.score = 0

class QuizServer:
    def __init__(self, host='127.0.0.1', port=5000, player_count=2):
        self.host = host
        self.port = port
        self.player_count = player_count
        self.players = []
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host, self.port))
        
    def start(self):
        print(f"[SERVER STARTED] Listening on {self.host}:{self.port}")
        self.server_socket.listen()
        
        print(f"Waiting for {self.player_count} players to join...")
        while len(self.players) < self.player_count:
            conn, addr = self.server_socket.accept()
            data = conn.recv(1024).decode()
            msg = json.loads(data)
            player_name = msg.get("name", "Anonymous")
            
            player = Player(conn, addr, player_name)
            self.players.append(player)
            print(f"[NEW PLAYER] {player_name} connected from {addr}")
            self.broadcast({"message": f"{player_name} joined the game! ({len(self.players)}/{self.player_count})"})

        self.run_game()

    def broadcast(self, data):
        msg = (json.dumps(data) + "\n").encode()
        for player in self.players:
            try:
                player.conn.send(msg)
            except:
                self.players.remove(player)

    def send_to_player(self, player, data):
        msg = (json.dumps(data) + "\n").encode()
        player.conn.send(msg)

    def run_game(self):
        print("[GAME STARTING] All players connected.")
        self.broadcast({"type": "start", "message": "Game is starting now!"})
        
        question_list = list(QUESTIONS.items())
        random.shuffle(question_list)

        for i, (q_text, q_answer) in enumerate(question_list):
            self.broadcast({
                "type": "question",
                "number": i + 1,
                "question": q_text
            })

            for player in self.players:
                try:
                    data = player.conn.recv(1024).decode()
                    resp = json.loads(data)
                    user_answer = resp.get("answer", "").strip().lower()
                    
                    if user_answer == q_answer.lower():
                        player.score += 1
                        self.send_to_player(player, {"type": "feedback", "correct": True, "message": "Correct!"})
                    else:
                        self.send_to_player(player, {"type": "feedback", "correct": False, "message": f"Wrong! Correct was: {q_answer}"})
                except Exception as e:
                    print(f"Error receiving from {player.name}: {e}")

        self.end_game()

    def end_game(self):
        scores = {p.name: p.score for p in self.players}
        self.broadcast({
            "type": "end",
            "message": "Game Over!",
            "scores": scores
        })
        print("[GAME OVER] Results sent.")
        for p in self.players:
            p.conn.close()
        self.server_socket.close()

if __name__ == "__main__":
    server = QuizServer(player_count=2)
    server.start()
