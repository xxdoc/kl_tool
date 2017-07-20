
def main():
    a = {}
    a.setdefault("a", '123')
    print a
    a["a"] = "apple"
    a.setdefault("a","default")
    a["a"] = None
    a.setdefault("b","default")
    print a

if __name__ == '__main__':
    main()
