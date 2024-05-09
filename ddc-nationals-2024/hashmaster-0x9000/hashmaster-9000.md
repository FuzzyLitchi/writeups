# Hashmaster 0x9000
This was a challenge for the danish cybersecurity championship. The challenge description is as follows
```
Der kom lidt for meget regneri i den anden hashmaster, så prøver vi lige med lidt xor i sted for
```
Which translates to "There was a bit too much calculating in the other hashmaster, so lets try a bit of xor instead" The following two files are attached.

### chal.py
```py
from Crypto.Hash import MD5

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def bytes_to_int(a):
    return int(a.hex(),16)

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

assert len(FLAG) == 69
assert FLAG.startswith("DDC{")
assert FLAG.endswith("}")

for x in FLAG[4:-1]:
    assert x in "mMmMmMmMmMm"

hashes = []
for i in range(len(FLAG)):
    c = str(i) + FLAG[i] 
    md5 = MD5.new()
    md5.update(c.encode())
    h = md5.digest()
    hashes.append(h)


hash = hashes[0]
for x in hashes[1:]:
    hash = xor(hash,x)

with open("output.txt", "w") as f:
    f.write(hash.hex())
```

### output.txt
```
c79d3af2053b81332fb4e1bc7ad8a805
```

## Solution

This is the exact same challenge as [Hashmaster 9000](../hashmaster-9000/hashmaster-9000.md) but with an xor operation instead of addition modulo $2^{128}$. We can perform a similar analysis and simply swap addition and substraction operators with xor (since addition and substraction are the same operation in xor).

$$
\begin{align*}
h \oplus h' \oplus \sum_{i=4}^{67} H(i, m) &= \sum_{i=4}^{67} b_i(H(i, M) \oplus H(i, m))\\
\widetilde{h} &= \sum_{i=4}^{67} b_i(H(i, M) \oplus H(i, m))\\
\widetilde{h} &= \sum_{i=4}^{67} b_i \widetilde{h}_i\\
\end{align*}
$$

The xor operation over 128 bits is the same as addition on vectors modulo 2. We can turn bit strings, into $\mathbb{Z_2^{128}}$. This lets us turn the bits of $b_i$ into a vector with 64 values, and $\widetilde{h}_i$ into a 64 by 128 matrix.

$$
\begin{align*}
\widetilde{h} &= \sum_{i=4}^{67} b_i \widetilde{h}_i\\
\widetilde{h} &= \sum_{i=4}^{67} \widetilde{h}_i b_i\\
\widetilde{h} &= \widetilde{H} b\\
\end{align*}
$$

We can then solve this with classical linear algebra tools.

```py
from Crypto.Hash import MD5

def bytes_to_int(a):
    return int(a.hex(),16)

def H(i, c_):
    c = str(i) + c_
    md5 = MD5.new()
    print(c)
    md5.update(c.encode())
    h = md5.digest()
    return bytes_to_int(h)

h_tilde = H(0, "D")
h_tilde ^^= H(1, "D")
h_tilde ^^= H(2, "C")
h_tilde ^^= H(3, "{")
h_tilde ^^= H(68, "}")

h_array = []
for i in range(4, 68):
    h_tilde ^^= H(i, "m")
    h_i = (H(i, "M") ^^ H(i, "m"))
    h_array.append(h_i)

h_tilde ^^= 0xc79d3af2053b81332fb4e1bc7ad8a805

def get_bit(a, i):
    return (a >> i) & 1

R = IntegerModRing(2)

h_tilde_vector = vector([R(get_bit(h_tilde, i)) for i in range(128)])
H_tilde = Matrix([
    [R(get_bit(h, i)) for i in range(128)] for h in h_array
]).transpose()

b = H_tilde.solve_right(h_tilde_vector)

print(b)

flag = "DDC{"
for bit in b:
    if bit == 1:
        flag += "M"
    else:
        flag += "m"
print(flag+"}")
```

```sh
$ sage solve.sage
<...snip...>
(0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1)
DDC{mMMmmMmmMMMMmmMmmMmmMMmmMmmMMMmmMMMmMmMmmMMMmMMMMMMmMMMmmmmmMMMM}
```