from queue import Queue
waitlist = Queue()

waitlist.put('Erin')
waitlist.put('Samantha')
waitlist.put('Joe')
waitlist.put('Martin')
waitlist.put('Helena')

print(waitlist.get())
print(waitlist.get())
print(waitlist.get())
