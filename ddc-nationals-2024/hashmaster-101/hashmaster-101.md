# Hashmaster 101
This was a challenge for the danish cybersecurity championship. The challenge description is as follows
```
Jeg har hashet flaget! (tak til openECSC for inspiration :D)
```
Which translates to "I've hashed the flag! (thank you openECSC for inspiration.)" The following two files are attached.

### chal.py
```py
from Crypto.Hash import MD5

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

for x in FLAG:
    assert x in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_"

hashes = []
for c in FLAG:
    md5 = MD5.new()
    md5.update(c.encode())
    h = md5.hexdigest()
    hashes.append(h)

with open("output.txt", "w") as f:
    for i in range(len(hashes)):
        f.write(f'char{i} = {hashes[i]}\n')
```
### output.txt
```
char0 = f623e75af30e62bbd73d6df5b50bb7b5
char1 = f623e75af30e62bbd73d6df5b50bb7b5
char2 = 0d61f8370cad1d412f80b84d143e1257
char3 = f95b70fdc3088560732a5ac135644506
char4 = d95679752134a2d9eb61dbd7b91c4bcc
char5 = 7b8b965ad4bca0e41ab51de7b31363a1
char6 = e1671797c52e15f763380b45e841ec32
char7 = b14a7b8059d9c055954c92674ce60032
char8 = f1290186a5d0b1ceab27f4e77c0c5d68
char9 = 0cc175b9c0f1b6a831c399e269772661
char10 = 415290769594460e2e485922904f345d
char11 = b14a7b8059d9c055954c92674ce60032
char12 = 8277e0910d750195b448797616e091ad
char13 = d95679752134a2d9eb61dbd7b91c4bcc
char14 = e1671797c52e15f763380b45e841ec32
char15 = 03c7c0ace395d80182db07ae2c30f034
char16 = 7b8b965ad4bca0e41ab51de7b31363a1
char17 = e358efa489f58062f10dd7316b65649e
char18 = b14a7b8059d9c055954c92674ce60032
char19 = 6f8f57715090da2632453988d9a1501b
char20 = 0cc175b9c0f1b6a831c399e269772661
char21 = e358efa489f58062f10dd7316b65649e
char22 = e358efa489f58062f10dd7316b65649e
char23 = e1671797c52e15f763380b45e841ec32
char24 = 4b43b0aee35624cd95b910189b3dc231
char25 = b14a7b8059d9c055954c92674ce60032
char26 = 865c0c0b4ab0e063e5caa3387c1a8741
char27 = 8fa14cdd754f91cc6554c9e71929cce7
char28 = b14a7b8059d9c055954c92674ce60032
char29 = 415290769594460e2e485922904f345d
char30 = d95679752134a2d9eb61dbd7b91c4bcc
char31 = 7b774effe4a349c6dd82ad4f4f21d34c
char32 = b14a7b8059d9c055954c92674ce60032
char33 = 92eb5ffee6ae2fec3ad71c777531578f
char34 = 4b43b0aee35624cd95b910189b3dc231
char35 = 7b774effe4a349c6dd82ad4f4f21d34c
char36 = e358efa489f58062f10dd7316b65649e
char37 = e1671797c52e15f763380b45e841ec32
char38 = b14a7b8059d9c055954c92674ce60032
char39 = 865c0c0b4ab0e063e5caa3387c1a8741
char40 = 7b8b965ad4bca0e41ab51de7b31363a1
char41 = 83878c91171338902e0fe0fb97a8c47a
char42 = 7b774effe4a349c6dd82ad4f4f21d34c
char43 = e358efa489f58062f10dd7316b65649e
char44 = b14a7b8059d9c055954c92674ce60032
char45 = 03c7c0ace395d80182db07ae2c30f034
char46 = 83878c91171338902e0fe0fb97a8c47a
char47 = 0cc175b9c0f1b6a831c399e269772661
char48 = 4a8a08f09d37b73795649038408b5f33
char49 = e1671797c52e15f763380b45e841ec32
char50 = cbb184dd8e05c9709e5dcaedaa0495cf
```

## Solution

We can tell from `chal.py` that the input (that is to say the flag) is hashed one letter at a time. This means that we only need to do at most 256 computations to reverse any of these hashes. The input space is further reduced to `"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_"` or just 55 inputs. We can easily construct a lookup table and reverse the function.

```py
from Crypto.Hash import MD5

with open("output.txt", "r") as f:
    OUTPUT = f.read().strip()

mapping = {}
for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{}_":
    md5 = MD5.new()
    md5.update(c.encode())
    h = md5.hexdigest()
    mapping[h] = c

flag = ""
for l in OUTPUT.splitlines():
    l = l[l.index("= ")+2:]
    flag += mapping[l]

print(flag)
```

```sh
$ python solve.py
DDC{one_way_doesnt_matter_if_you_brute_input_space}
```