import socket
import json

class QuizClient:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket()
        self.name = ""

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.name = input("Enter your name: ")
            self.send({"name": self.name})
            self.listen_for_messages()
        except ConnectionRefusedError:
            print("Error: Could not connect to the server. Is it running?")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.client_socket.close()

    def send(self, data):
        msg = json.dumps(data).encode()
        self.client_socket.send(msg)

    def listen_for_messages(self):
        try:
            with self.client_socket.makefile('r') as f:
                for line in f:
                    msg = json.loads(line)
                    msg_type = msg.get("type")

                    if "message" in msg and msg_type != "end":
                        print(f"\n[SERVER] {msg['message']}")

                    if msg_type == "question":
                        print(f"\nQuestion {msg['number']}: {msg['question']}")
                        answer = input("Your answer: ")
                        self.send({"answer": answer})

                    elif msg_type == "feedback":
                        status = "Correct" if msg["correct"] else "Wrong"
                        print(f"{status} {msg['message']}")

                    elif msg_type == "end":
                        print("\n" + "-"*20 + "\nFINAL RESULTS\n" + "-"*20)
                        for name, score in msg["scores"].items():
                            print(f"{name}: {score} points")
                        print("-"*20)
                        return
        except Exception as e:
            print(f"Connection error: {e}")

if __name__ == "__main__":
    client = QuizClient()
    client.connect()
