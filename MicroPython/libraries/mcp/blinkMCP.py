import mcp
import time

io = mcp.MCP23017()

# controls some output pins
io.setup(0, mcp.OUT)
io.output_pins([True])

for loopCount in range(0,100):
	io.output_pins([True])
	time.sleep(1)
	io.output_pins([False])
	time.sleep(1)
