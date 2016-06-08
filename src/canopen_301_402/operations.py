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
        self.operations.append(self.done)
        
    def next_operation(self):
        self.operations[self.current_op]()
        self.current_op += 1

    def done(self):
        pass
