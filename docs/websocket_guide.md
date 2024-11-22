# Grami AI WebSocket Communication Guide

## Overview

The Grami AI Framework uses WebSocket communication to enable real-time, bidirectional interaction between agents, tools, and clients.

## Communication Architecture

### Key Components
- **Growth Manager**: Central WebSocket server
- **Agents**: Intelligent processing units
- **Clients**: External connection points
- **Tools**: Modular functionality providers

## WebSocket Connection Flow

1. **Server Initialization**
   - Growth Manager starts WebSocket server
   - Dynamically selects available port
   - Writes port to environment variable

2. **Client Connection**
   - Retrieve server port
   - Establish WebSocket connection
   - Authenticate (future implementation)

3. **Message Processing**
   - Clients send request messages
   - Growth Manager routes to appropriate agent/tool
   - Asynchronous processing
   - Results streamed back to client

## Message Structures

### Request Message
```json
{
    "type": "content_request",
    "platform": "instagram",
    "niche": "tech",
    "content_type": "post"
}
```

### Response Message
```json
{
    "status": "success",
    "data": {
        "text": "AI-generated content...",
        "hashtags": ["#TechInnovation", "#AIFuture"]
    }
}
```

## Error Handling

### Common Error Scenarios
- Connection failures
- Tool execution errors
- Authentication issues
- Resource constraints

### Error Response Format
```json
{
    "status": "error",
    "error_code": "TOOL_EXECUTION_FAILED",
    "message": "Detailed error description"
}
```

## Security Considerations

- Environment-based configuration
- No hardcoded credentials
- Future: Implement authentication
- Use secure WebSocket (wss://)

## Performance Optimization

- Async design minimizes blocking
- Efficient message routing
- Lazy tool loading
- Configurable concurrency

## Example: Client Connection

```python
import asyncio
import websockets

async def connect_to_grami():
    uri = "ws://localhost:PORT/ws"
    async with websockets.connect(uri) as websocket:
        # Send request
        await websocket.send(json.dumps({
            "type": "content_request",
            "platform": "instagram"
        }))
        
        # Receive response
        response = await websocket.recv()
        print(response)
```

## Extensibility

### Custom Message Types
- Define new request types
- Implement corresponding agent handlers
- Extend tool capabilities dynamically

## Monitoring and Logging

- Comprehensive WebSocket connection logs
- Track connection lifecycle
- Record tool execution metrics
- Performance profiling

## Troubleshooting

### Connection Issues
- Check server port
- Verify network connectivity
- Validate message formats

### Performance Bottlenecks
- Monitor async task execution
- Profile tool response times
- Optimize long-running operations

## Future Roadmap

- Enhanced authentication
- More sophisticated routing
- Multi-agent coordination
- Advanced error recovery

## Best Practices

1. Keep messages lightweight
2. Use async programming
3. Implement robust error handling
4. Log comprehensively
5. Design for scalability

## Conclusion

WebSocket communication is the backbone of the Grami AI Framework, enabling real-time, flexible, and powerful AI interactions.
