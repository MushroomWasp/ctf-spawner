# Dynamic Docker Instance Manager

This project provides a simple system to dynamically start and stop Docker Compose instances with unique names and ports.  
It is useful for CTF challenges, lab environments, or temporary isolated services.

---

## Files

### `script.sh`
A shell script that manages Docker Compose instances:

- **START <port> <name>** → starts a new instance with the given port and project name.  
- **STOP <name>** → stops and removes the instance (including volumes).  

When stopped, the container is completely removed, freeing space and CPU.

---

### `server.py`
A Flask-based API server that automates instance management:

- Assigns **random ports and names** to new instances.  
- Associates instances with team **tokens**.  
- Ensures only one active instance per team (old instance is stopped if a new one is spawned).  
- Instances automatically **expire after a set lifetime** (default: 300s).  
- Returns the public **URL** of the running service.  

---

## Setup

Put **`script.sh`** and **`server.py`** in the **root of your app**, where your `docker-compose.yml` file exists.  
This ensures the scripts can properly manage the Docker Compose services.

---

## API Endpoints

### `POST /spawn`
Spawns a new Docker instance for a team.

**Request:**
```json
{
  "token": "team1token"
}
````

**Response:**

```json
{
  "url": "http://138.68.65.113:21543/",
  "name": "abc123"
}
```

---

## Configuration

Inside `server.py`, you can adjust:

* `INSTANCE_LIFETIME` → how long an instance stays alive before auto-stop.
* `PORT_RANGE` → range of random ports to assign.
* `SERVER_IP` → your public server’s IP.
* `TOKENS` → allowed team tokens.

---

## Usage

### Start the API server:

```bash
python3 server.py
```

### Spawn a new instance (via API call):

```bash
curl -X POST http://localhost:8484/spawn \
    -H "Content-Type: application/json" \
    -d '{"token": "team1token"}'
```

### Direct script usage:

```bash
./script.sh START 20001 myproject
./script.sh STOP myproject
```

---

## Notes

* Each team token can run **only one instance at a time**.
* When a new one is spawned, the old one is removed automatically.
* Designed for **ephemeral lab/CTF setups**, not for production.

---
