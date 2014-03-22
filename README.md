## Fast python library for jenks natural breaks

The history and intent of the Jenks natural breaks algorithm is well covered by

* http://www.macwright.org/2013/02/18/literate-jenks.html
* http://danieljlewis.org/2010/06/07/jenks-natural-breaks-algorithm-in-python/

There are even a few python implementations:

* https://gist.github.com/llimllib/4974446
* https://gist.github.com/drewda/1299198
* http://danieljlewis.org/files/2010/06/Jenks.pdf

However, it has been noted that the python implementations are tediously *slow*. There are two obvious reasons for this...

1. All the data is stored in python lists rather than optimized numpy arrays. The fact that their variables are named `matrices` is perhaps some sort of practical joke...

2. There is a lot of looping. Like exponential-time looping. The algorithm makes this somewhat inevitable. Python sucks at iterating over simple math, exploding the runtime very quickly. `Cython`, through it's variable typing, allows us to write python modules in python-like syntax and compile it to a shared library that can be imported as a python module and run the loops at near-C speed. 

Here's the benchmark against the jenks2.py implementation:

```
In [1]: from jenks2 import jenks

In [2]: %timeit jenks(data, 5)
1 loops, best of 3: 8.16 s per loop

In [3]: from jenks import jenks

In [4]: %timeit jenks(data, 5)
10 loops, best of 3: 69.2 ms per loop
```

Yep that's *118X faster* for just a little bit of static typing and using arrays instead of lists. It even makes the logic easier to read (for those of us who work with matrices/arrays often).

The only cost is that you need Cython and a C compiler to get it working. 

```
sudo apt-get install cython build-essential
pip install -e "git+https://github.com/perrygeo/jenks.git#egg=jenks"

```

And then test it
```
import json
from jenks import jenks

# data should be 1-dimensional array, python list or iterable 
data = json.load(open('test.json')) 
print jenks(data, 5)
```
