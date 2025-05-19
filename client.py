import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

request1 = {
    "threshold": 50,
    "city": "Seattle",
    "state": "WA",
    "date": "2025-05-20"    
}

request2 = {
    "threshold": 50,
    "city": "Notacity",
    "state": "WA",
    "date": "2025-05-20"
}

request3 = {
    "city": "Seattle",
    "state": "WA",
    "date": "2025-05-20"
}

request4 = {
    "threshold": 50,
    "city": "Seattle",
    "state": "WA",
    "date": "2025-07-20" 
}
socket.send_json(request4)

result = socket.recv_json()

if "error" in result:
    print(result.get("error"))
else:
    print(result.get("will_rain"))
