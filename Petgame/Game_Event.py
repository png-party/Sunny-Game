#Makes a delegate-like object that functions can subscribe to, so the functions can be called when the event occurs
class GameEvent:
    def __init__(self):
        #Keep a list of all of the functions subscribed to this delegate
        self.subscribers = []

    def subscribe(self, toCall):
        #Let a callback function subscribe to the delegate if it hasn't already
        if toCall not in self.subscribers:
            self.subscribers.append(toCall)
    
    def unsubscribe(self, toCall):
        #Let a callback function unsubscribe from the delegate event
        if toCall in self.subscribers:
            self.subscribers.remove(toCall)

    #orderedArguments: captures function arguments based on their position
    #keywordArguments: captures function arguments based on their variable names
    #use * and ** to actually collect the arguments
    def invoke(self, *orderedArguments, **keywordArguments):
        #Call every function subscribed when the event actually occurs
        for function in self.subscribers:
            function(*orderedArguments, **keywordArguments)
