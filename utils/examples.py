#!run_examples.py
random()
check(random())
same(random(magic=123),random(magic=123))
same(random(magic=123),random(magic=456))
