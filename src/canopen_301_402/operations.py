class Operations(object):
    def __init__(self):
        super(Operations, self).__init__()
        self.current_op = 0
        self.operations = list()

        # collect all step methods
        l = []
        for method_name in dir(self):
            s = "step"
            method = getattr(self,method_name)
            if callable(method) and method_name[:len(s)] == s:
                l.append(method_name)
        # sort step methods
        for k in sorted(l):
            self.operations.append(getattr(self,k))
        
    def start(self):
        self.current_op = 0
        self.operations[self.current_op]()        

    def next_operation(self,*args,**kwargs):
        self.current_op += 1
        if self.current_op < len(self.operations):
            self.operations[self.current_op]()
        else:
            self.done()

    def done(self):
        pass
