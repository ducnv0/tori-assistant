from fastapi import APIRouter, WebSocket, WebSocketDisconnect

chat_router = APIRouter(tags=['Chat'])


@chat_router.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print('Client connected')

    try:
        while True:
            try:
                data = await websocket.receive()

                if 'text' in data:
                    print('Received text:', data['text'])
                    await websocket.send_text(f"Server received: {data['text']}")

                elif 'bytes' in data:
                    print('Received binary data, length:', len(data['bytes']))
                    await websocket.send_text(
                        f"Received {len(data['bytes'])} bytes of binary data"
                    )

            except RuntimeError as e:
                print('RuntimeError:', e)
                break

    except WebSocketDisconnect:
        print('Client disconnected')

    finally:
        await websocket.close()
        print('WebSocket connection closed')
