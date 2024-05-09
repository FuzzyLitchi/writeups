# Hashmaster 9000
This was a challenge for the danish cybersecurity championship. The challenge description is as follows
```
øv, du fik nok lige for mange outputs der. Men hvad så når du kun får en?
```
Which translates to "Dang, it seems you got too many output there. But what if you only get one?" The following two files are attached.

### chal.py
```py
from Crypto.Hash import MD5

def bytes_to_int(a):
    return int(a.hex(),16)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

assert len(FLAG) == 69
assert FLAG.startswith("DDC{")
assert FLAG.endswith("}")

for x in FLAG[4:-1]:
    assert x in "LlLlLlL"

hashes = []
for i in range(len(FLAG)):
    c = str(i) + FLAG[i] 
    md5 = MD5.new()
    md5.update(c.encode())
    h = md5.digest()
    hashes.append(h)


hash = bytes_to_int(hashes[0])
for x in hashes[1:]:
    hash += bytes_to_int(x)
    hash %= 2**128

with open("output.txt", "w") as f:
    f.write(hex(hash)[2:])
```
### output.txt
```
c2be729e418981b516ce80ef22385b9d
```

## Solution

This challenge is similar to [hashmaster 101](../hashmaster-101/hashmaster-101.md), but has a few changes. Other than the surrounding `DDC{` and `}` the flag consists entirely of the characters `L` and `l`, which greatly reduces the input space. A quick back-of-the-envelope calculation reveals it is beyond bruteforce tho. Each character is either `l` or `L`, so there is one bit of entropy for each unkown character and there are 64 such characters therfore 64 bits of entropy. Which is outside of what I can compute.

The other change is that we no longer get the hash of each character, instead we got the sum of them all modulo $2^{128}$. The string truncation on the last line just remove the `"0x"` prefix from the hex string, and we can double check that the output.txt is 128 bits of data.

```py
In [1]: len("c2be729e418981b516ce80ef22385b9d")*4
Out[1]: 128
```

We get 128 bits of output, and only need to recover 64 bits of input, so information theory tells us we probably can do it.

We start with some definitions. We have our hash function.
$$H(i, x) = MD5(str(i) || x)$$
As opposed to Hashmaster 101, this function also takes in an index, which means an `L` at position 10 will have a different hash than an `L` at position 20.

$$h_i = H(i, c_i)$$

Each character $c_i$ corresponds to a hash $h_i$.

$$ h = \sum_{i=0}^{68} h_i \mod 2^{128} $$

We know the some of the $h_i$ values.
$$
\begin{align*} 
h_0 &= H(0, D)\\
h_1 &= H(1, D)\\
h_2 &= H(0, C)\\
h_3 &= H(3, \{)\\
h_{68} &= H(68, \})
\end{align*}
$$

We can call the sum (modulo $2^{128}$) of these known hashes $h'$

$$
\begin{align*}
h &= h' + \sum_{i=4}^{67} h_i \mod 2^{128}\\
h - h' &= \sum_{i=4}^{67} h_i \mod 2^{128}
\end{align*}
$$

Since there are only 2 possible values for any given $h_i$ (where $4 \le i \le 67$) we can introduce a variable $b_i$ which is 0 if $c_i = l$ and 1 if $c_i = L$.

$$
h - h' = \sum_{i=4}^{67} H(i, l) + b_i(H(i, L) - H(i, l)) \mod 2^{128}
$$

If $b_i = 0$ then $H(i, l) + 0(H(i, L) - H(i, l)) = H(i,l)$. And if $b_i = 1$ then $H(i, l) + 1(H(i, L) - H(i, l)) = H(i, L)$. So our equation is still correct. We can then move the constant part (that doesn't depend on $b_i$) to the left side.

$$
h - h' - \sum_{i=4}^{67} H(i, l) = \sum_{i=4}^{67} b_i(H(i, L) - H(i, l)) \mod 2^{128}
$$

The left side consists only of known values, and the right side is a subset sum of known values. This lets us apply existing subset sum solvers to our problem. We can steal [this implementation.](https://github.com/josephsurin/lattice-based-cryptanalysis/blob/main/lbc_toolkit/problems/knapsack.sage)

$$
\widetilde{h} = h - h' - \sum_{i=4}^{67} H(i, l)
$$

The full solve script is [here](solve.sage), and the flag is `DDC{LLlLLllLllLLlllLlLLLLllllLlLlLLllllLLllLlLllllLLllLLlLLllLllLlLL}`

