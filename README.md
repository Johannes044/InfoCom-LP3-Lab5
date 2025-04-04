<div align="center">
  <img src="/src/webserver/static/images/gwd.jpg" alt="Drone logo" width=256px>
  <h3>GWD</h3>
  <p>
    Medicine delivery
  </p>
</div>

## Guide
_**IMPORTANT**: All of the following commands must be ran from the root of the repository._

### Installation
- ```bash
  bash scripts/install.sh
  ```

### Running
- Kill previous instances and run everything:
  ```bash
  bash scripts/restart.sh
  ```
- Start web services and swarm separately:
  1. Start the web services:
     ```bash
     bash scripts/start_web.sh
     ```

### Stop
- To kill **ALL** the services (web + drone) run:
  ```bash
  bash scripts/killall.sh
  ```

## Info
- Ports:
  - redis: 6379
  - build.py: 1337
  - database.py: 1338
  - route_planner.py: 1339


