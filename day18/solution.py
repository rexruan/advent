"""
You find the original question here:
https://adventofcode.com/2021/day/18
"""

from copy import deepcopy


class Number:
    def __init__(self, number, former, latter):
        self.number = number
        self.former = former
        self.latter = latter
    
class Snailfish:

    def __init__(self, fish):
        self.fish = fish
        self._process()


    def add(self, new_fish):
        self.fish = [self.fish, new_fish]
        self._process()
    
    def _explode(self):
        number_dict, _ = get_number_list(self.fish, dict(), 0, 0)
        number_list = list(number_dict.values())
        print(number_list)
        explosion = False
        max_depth = max(number_list)[0]
        for index, (depth, d, element) in enumerate(number_list):
            if depth == max_depth and depth > 3:
                explosion = True
                if index > 0:
                    number_list[index-1] = number_list[index-1][0], number_list[index-1][1], number_list[index-1][-1] + element
                if index < len(number_list) - 2:
                    number_list[index+2] = number_list[index+2][0], number_list[index+2][1], number_list[index+2][-1] + number_list[index+1][-1]
                number_list[index] = depth-1, None, 0
                del number_list[index+1]
                self.fish = convert2list(number_list)
                break
        if explosion is False:
            self.fish = convert2list(number_list)
        return explosion
    
    def _split(self, checked_part=False, booleans=[], has_booleans=False):
        if checked_part is False: checked_part = self.fish
        for index, fish in enumerate(checked_part):
            if isinstance(fish, int):
                if fish > 9:
                    if has_booleans is False:
                        has_booleans = True
                        checked_part[index] = [fish // 2, (fish+1)//2]
                    booleans.append(True)
                else:
                    booleans.append(False)
            else:
                b, has_booleans = self._split(fish, booleans, has_booleans)
                booleans.extend(b)
        return booleans, has_booleans
    
    def _process(self):
        while True:
            if self._explode():
                continue
            else:
                t, _  = self._split(booleans=[], has_booleans=False)
                if True in t:
                    continue
                else:
                    break

    def magnitude(self):
        return compute_magnitude(self.fish)
            
def get_number_list(l, location={}, depth=0, base=0):
    index = -1
    while l:
        element = l.pop(0)
        index += 1        
        if isinstance(element, list):
            sublocation, base = get_number_list(element, location, depth+1, base)
            location = {**location, **sublocation}
        else:
            location[base] = (depth, index, element)
            base += 1
    return location, base


def convert2list(number_list):
    
    while True:
        merged = False
        for index, (j, _, j_e) in enumerate(number_list[1:]):
            i, _, i_e =  number_list[index]
            if i == j:
                number_list[index] = (i-1, None, [i_e, j_e])
                number_list.pop(index+1)
                merged = True
                break
        if merged is False:
            break
    
    return number_list[-1][-1]             


def compute_magnitude(nums):
    left, right = nums
    if isinstance(left, list):
        left = compute_magnitude(left)
    if isinstance(right, list):
        right = compute_magnitude(right)
    return left * 3 + right * 2


def main():
  with open('input') as f:
      lines = [eval(line) for line in f.read().strip().split('\n')]
      s = Snailfish(deepcopy(lines[0]))
      for line in lines[1:]:
          s.add(deepcopy(line))
      print(s.magnitude())

      max_magnitude = 0
      for i, f1 in enumerate(lines):
          for j, f2 in enumerate(lines):
              if i != j:
                  print(i,j)
                  f = Snailfish(deepcopy(f1))
                  f.add(deepcopy(f2))
                  max_magnitude = max(max_magnitude, f.magnitude())
      print(max_magnitude)
  
if __name__ == '__main__':
    main()