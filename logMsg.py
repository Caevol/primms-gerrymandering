

runSilent = False

def setRunSilent(bool):
	global runSilent
	runSilent = bool

def logMessage(msg):
	if not runSilent:
		if isinstance(msg, (list, tuple)):
			print ' '.join(str(p) for p in msg)
		else:
			print msg