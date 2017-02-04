def decrator(info):
    def _decrator(cls):
        def wrapper(*args,**kw):
            print info
            return cls(*args,**kw)
        wrapper.cls = cls
        return wrapper
    return _decrator

@decrator('A decrator')
class A(object):
    def __init__(self,name):
        self.name=name
        print "init A class",self.name

@decrator('B decrator')
class B(A.cls):
    def __init__(self,name,passwd):
        super(B.cls, self).__init__(name)
        self.passwd=passwd
        print "init B class",self.name,self.passwd

b = B('uuu','pp')