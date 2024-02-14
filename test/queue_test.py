from queue import Queue


q = Queue()

q.put("Dette er en test")


test = q.get()
print(test)
