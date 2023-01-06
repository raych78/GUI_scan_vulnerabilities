
import string
import itertools
import hashlib
import queue

def bruteForce_Hash(password_hash,killing_queue,return_queue, length=1, startWith='', finishWith='', algorithm = "sha256"):
    # Create a list of all possible characters to use in the brute-force attack
    chars = string.ascii_letters + string.digits + string.punctuation
    return_queue.put("Searching...")
    killed = False
    if length != 1: #If the length is define, we assume its lenToFind + lenFinish + LenStart
        length = length - len(finishWith) - len(startWith)
    while True:
        for combination in itertools.product(chars, repeat=length):
            CurrentPass = "".join(combination)
            CurrentPass = startWith + CurrentPass + finishWith
            #print(CurrentPass)
            hash = HashThis(CurrentPass,algorithm)
            #hash = hashlib.sha256(CurrentPass.encode()).hexdigest()
            # Check if the current combination matches the password
            if hash == password_hash:
                return_queue.put("Password Found : "+CurrentPass)
                return None
            try:
                killed = killing_queue.get_nowait()
                if killed:
                    return_queue.put("Stopped")
                    return None 
            except queue.Empty:
                pass
        length += 1
        return_queue.put("Searching... Current length : "+str(length))



def Dictionary_Hash(password_hash, path, return_queue_Dico, algorithm = "sha256"):
    with open(path,'r') as f:
        for p in f.readlines():
            p = p[:len(p)-1]
            #hash = hashlib.sha256(p.encode()).hexdigest()
            hash = HashThis(p,algorithm)
            if hash == password_hash:
                return_queue_Dico.put("Password Found : "+p)
    return_queue_Dico.put("Password not found in "+path)

def HashThis(toHash, algorithm = "sha256"):
        return getattr(hashlib, algorithm)(toHash.encode()).hexdigest()