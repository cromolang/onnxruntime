"""The places of the functions in the table OrtApi of onnxruntime_c_api.h, in its order."""
import re
import sys

text = open(sys.argv[1], encoding='utf-8').read()
start = text.index('struct OrtApi {')
end = text.index('\n};', start)
body = text[start:end]
body = re.sub(r'/\*.*?\*/', '', body, flags=re.S)
body = re.sub(r'//[^\n]*', '', body)
names = []
for m in re.finditer(r'ORT_API2_STATUS\(\s*(\w+)|ORT_CLASS_RELEASE\(\s*(\w+)\s*\)|\(\s*ORT_API_CALL\s*\*\s*(\w+)\s*\)', body):
    names.append(m.group(1) or (m.group(2) and 'Release' + m.group(2)) or m.group(3))
wanted = sys.argv[2:]
if not wanted:
    for i, n in enumerate(names[:110]):
        print(i, n)
for n in wanted:
    print(n, names.index(n))
print('total', len(names))
