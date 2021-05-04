class Base():
    pass

temp = None

class Template():
    def __init__(self):
        self.data = temp # get data, then assign to attributes
        # if full will calculate those values as well
    
    def complete(self):
        pass # calculate and fill out, returning full version from Partial (only Partial will have)

    def save(self):
        pass # save the data back into the database if any changes made (will be different for full and Partial)