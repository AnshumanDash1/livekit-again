# Starting the Agent
Start the chrome debugging server:
```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome_debug"
```

Start the livekit agent:
```
uv run agent.py console
```

The agent should be able to control your computer! Try opening YouTube, reading what's on the screen, and clicking on a video!