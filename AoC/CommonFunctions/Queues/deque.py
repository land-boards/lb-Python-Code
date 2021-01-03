import collections

# Create a deque
myDeque = collections.deque(["Mon","Tue","Wed"])
print (myDeque)

# Additional Deque Operations

# extend(iterable) − This function is used to add multiple values 
# at the right end of deque. The argument passed is an iterable.

# extendleft(iterable) − This function is used to add multiple values 
# at the left end of deque. The argument passed is an iterable. Order 
# is reversed as a result of left appends.

# rotate() − This function rotates the deque by the number specified 
# in arguments. If the number specified is negative, rotation occurs to left. 
# Else rotation is to right.

# append() − This function is used to insert the value in its argument
# to the right end of deque.
print("Adding to the right: ")
myDeque.append("Thu")
print (myDeque)

# appendleft() − This function is used to insert the value in its argument
# to the left end of deque.
print("Adding to the left: ")
myDeque.appendleft("Sun")
print (myDeque)

# pop() − This function is used to delete an argument from the right end 
# of deque.
print("Removing from the right: ")
myDeque.pop()
print (myDeque)

# popleft() − This function is used to delete an argument from the left end 
# of deque.
print("Removing from the left: ")
myDeque.popleft()
print (myDeque)

# reverse() − This function is used to reverse order of deque elements.
print("Reversing the deque: ")
myDeque.reverse()
print (myDeque)
