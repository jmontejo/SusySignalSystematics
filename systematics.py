systematics = [
    ("qcdw","qcup"),
    ("scdw","scup"),
    #("Var3cdw","Var3cup"),
    ("Var1",None),
    ("Var2",None),
    ("Var3a",None),
    ("Var3b",None),
    ("Var3c",None),
    ]
flat_systematics = [item for sublist in systematics for item in sublist]
