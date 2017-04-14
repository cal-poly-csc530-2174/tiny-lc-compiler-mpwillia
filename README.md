# Tiny Lambda Calculus Compiler
Authors
* Michael Williams
* Alanna Buss

## Usage

```shell
python3 tiny_lc_compiler.py Source Destination
```

For example
```shell
python3 tiny_lc_compiler.py input.txt output.py
```
Will read `input.txt` and compile it to the file `output.py`


## Python Recursion Limit
Python has a default recursion limit of 1000 which is rather small for the recursive nature of lambda calculus. To alleviate this problem we inject the following code into every compiled program.
```python
import sys
sys.setrecursionlimit(10**6)
```

This dramatically increases the recursion limit to 1000000 rather than 1000.

*Is this excessive?*  Yes

*Does it solve the problem?*  Yup

*Can you now overflow the stack?*  You bet


