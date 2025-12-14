# quvar-net

Educational lab for node discovery and monitoring in a local network. A bootstrap
node keeps a registry of connected agents, agents report their host info, and a
small web panel shows what is online.

The point of the project is to study distributed systems plumbing: newline-delimited
JSON over raw TCP, an event dispatcher on both sides of the connection, and a
registry that survives agent reconnects.

## Architecture

- **Bootstrap node** (`src/infrastructure/adapters/bootstrap.py`) — accepts agent
  connections on port 7583, dispatches events, keeps the client registry.
- **Agent** (`src/infrastructure/adapters/client.py`) — connects to the bootstrap
  node, sends host info once on connect, re-requests the node list every 3 minutes,
  reconnects on failure.
- **Peer listener** — each agent also opens a local port (46720–46730) and announces
  it, so the registry can hand out a full node list.
- **Web panel** (`src/infrastructure/admin/`) — FastAPI with JSON endpoints, bound
  to `127.0.0.1:3567`.

## Events

| Event | Direction | Purpose |
|---|---|---|
| `info` | agent → bootstrap | host info: OS, user, CPU, RAM, GPU |
| `new_node` | agent → bootstrap | announce peer listener address |
| `nodes_info` | both | request / share the node list |
| `receive_nodes` | bootstrap → agent | deliver the node list |

## Run

```bash
uv sync
uv run main.py
```

This starts both the bootstrap node and a local agent (demo mode on one machine).
The panel API is then available at `http://127.0.0.1:3567/api/list/`.

## Tests

```bash
uv run pytest
```

## Notes

The panel has no authentication and binds to localhost only — do not expose it
outside your own machine. This is a study toy, not production software.
