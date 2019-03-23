import mcp

io = mcp.MCP23017()

# controls some output pins
outPins = list(range(10,16))
nextVals = {}
for pinNum in outPins:
	io.setup(pinNum, mcp.OUT)
	nextVals[pinNum] = True
io.output_pins(nextVals)

# monitors and prints some input pins
inPins = list(range(0,10))
for pinNum in inPins:
	io.setup(pinNum, mcp.IN)
while True:
	print(io.input_pins(inPins))
	