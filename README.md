## Fast python library for jenks natural breaks

The history and intent of the Jenks natural breaks algorithm is well covered by

* http://www.macwright.org/2013/02/18/literate-jenks.html
* http://danieljlewis.org/2010/06/07/jenks-natural-breaks-algorithm-in-python/

There are even a few python implementations:

* https://gist.github.com/llimllib/4974446
* https://gist.github.com/drewda/1299198
* http://danieljlewis.org/files/2010/06/Jenks.pdf

However, it has been noted that the python implementations are tediously *slow*. There are two obvious reasons for this...

1. All the data is stored in python lists rather than optimized data structures. The fact that the variables are named "matrices" is perhaps some sort of practical joke given how bad lists are for matrix/array like data structures. **Numpy** arrays are your friend and I can't imagine doing any numeric computation in python without them. 

2. There is a lot of looping. Like exponential-time looping. The algorithm makes this somewhat inevitable. Python sucks at iterating over simple math, exploding the runtime very quickly. **Cython**, through it's variable typing, allows us to *write* the algorithm in python-like syntax, *compile* it to a shared library that can be imported as a python module and run at near-C speeds. 

So I set forth to make good use of my son's afternoon nap time and port the existing [python implementation](https://gist.github.com/llimllib/4974446) (which is, in turn based on the [wonderfully documented javascript implementation](http://www.macwright.org/simple-statistics/docs/simple_statistics.html#section-114)) to cython with numpy arrays. 

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
sudo apt-get install build-essential cython python-numpy
pip install -e "git+https://github.com/perrygeo/jenks.git#egg=jenks"
```

And then test it
```
In [1]: import json

In [2]: from jenks import jenks

In [3]: # data should be 1-dimensional array, python list or iterable 

In [4]: data = json.load(open('test.json')) 

In [5]: print jenks(data, 5)
[0.002810962, 2.0935481, 4.2054954, 6.1781483, 8.0917587, 9.997983]
```
