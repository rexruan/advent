"""
You find the original question here:
https://adventofcode.com/2021/day/16

Description of the given task
1. convert the hexadecial representation into binary
2. the hexadecimal representation of this packet might encode a few extra 0 bits at the end; 
   These are not part of the transmission and should be ignored.
3. first three bits encode the packet version
4. next three bits encode the packet type ID
"""

def _2bin(n, bin_string=''):
    if n < 2:
        bin_string = str(n) + bin_string
        if len(bin_string) < 4:
            bin_string = '0' * (4-len(bin_string)) + bin_string
        return bin_string
    else:
        r = n % 2
        q = n // 2
        bin_string = str(r) + bin_string
        return _2bin(q, bin_string)
  
def _2dcml(bin_string):
    return sum([2**index for index,b in enumerate(bin_string[::-1]) if b == '1'])

hex_dict = {h:value for h,value in zip(
  list('0123456789ABCDEF'),
  [_2bin(i) for i in range(16)]
)}

def _parse2bin(code):
    return ''.join([hex_dict[i] for i in code])


def parse(binary_code):
    version, typeID = _2dcml(binary_code[:3]), _2dcml(binary_code[3:6])
    remained_binary_code = binary_code[6:]
    res = {'version': version, 'typeID': typeID}
    if typeID == 4:
        label = ''
        while remained_binary_code:
            label += remained_binary_code[1:5]
            isEndGroup, remained_binary_code = remained_binary_code[0], remained_binary_code[5:]
            if isEndGroup == '0':
                break
            elif isEndGroup == '1':
                continue
            else:
                raise TypeError('Parsing String is not compatible')
        res['label'] = _2dcml(label)
        return res, remained_binary_code
    else:
        res['sub'] = []
        lengthTypeId, remained_binary_code = remained_binary_code[0], remained_binary_code[1:]
        if lengthTypeId == '0':
            subpackage_length = _2dcml(remained_binary_code[:15])
            subpackage = remained_binary_code[15:15+subpackage_length]
            while subpackage and set(list(subpackage)) != {'0'}:
                sub, subpackage = parse(subpackage)
                res['sub'].append(sub)
            return res, remained_binary_code[15+subpackage_length:]
        elif lengthTypeId == '1':
            subpackage_number = _2dcml(remained_binary_code[:11])
            remained_binary_code = remained_binary_code[11:]
            while subpackage_number:
                sub, remained_binary_code = parse(remained_binary_code)
                res['sub'].append(sub)
                subpackage_number -= 1
            return res, remained_binary_code
        else:
            raise TypeError('Error')


def sum_version(res):
    v = res.get('version',0)
    if 'sub' in res:
        for s in res['sub']:
            v +=  sum_version(s)
    return v

def prod(args):
    y = 1
    for arg in args:
        y *= arg
    return y

def gt(args):
    a,b = args
    if a > b: return 1
    else: return 0

def lt(args):
    a,b = args
    if a < b: return 1
    else: return 0

def cal(operator):
    if operator == 0: return lambda x: sum(x)
    elif operator == 1: return lambda x: prod(x)
    elif operator == 2: return lambda x: min(x)
    elif operator == 3: return lambda x: max(x)
    elif operator == 5: return lambda x: gt(x)
    elif operator == 6: return lambda x: lt(x)
    elif operator == 7: return lambda x: x[0] == x[1]
    
def compute(res):
    typeID = res.get('typeID')
    subs = res.get('sub')
    if set([sub.get('typeID') for sub in subs]) == {4}:
        label = cal(typeID)([sub.get('label') for sub in subs])
        res['label'] = label
        res['typeID'] = 4
        del res['sub']
    else:
        for i, sub in enumerate(subs):
            if sub.get('typeID') != 4:
                subs[i] = compute(sub)
    return res
       
def get_result(hex_string):
    code = _parse2bin(hex_string)
    res, _ = parse(code)
    # print('version_sum', sum_version(res))
    return res


def main():
  with open('input') as f:
      code = f.read().strip()
      res = get_result(code)
      while True:
          res = compute(res)
          if 'sub' not in res:
              break

if __name__ == '__main__':
    main()
