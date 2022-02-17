"""
You find the original question here:
https://adventofcode.com/2021/day/14
"""


def update(input_dict, rules):
    output_dict = {}
    for key in input_dict:
        char_dict = input_dict[key]
        for char_key, counts in char_dict.items():
            # key-value pair: key char_key
            letter = rules[''.join([key, char_key])]
            # insert key letter
            new_char_dict = output_dict.get(key, {})
            new_char_dict[letter] = new_char_dict.get(letter, 0) + counts
            output_dict[key] = new_char_dict
            # insert letter char_key
            new_char_dict = output_dict.get(letter, {})
            new_char_dict[char_key] = new_char_dict.get(char_key, 0) + counts
            output_dict[letter] = new_char_dict
    
    return output_dict

def main():
    with open('input') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        template = lines[0]
        rules = {line.split(' -> ')[0]:line.split(' -> ')[1] for line in lines[1:]}

        temp = {}
        for index, char in enumerate(template[1:]):
            char_dict = temp.get(template[index], {})
            char_dict[char] = char_dict.get(char, 0) + 1
            temp[template[index]] = char_dict
        
        input_dict = temp
        for _ in range(40):
            input_dict = update(input_dict, rules)

        stats = sorted([(key, sum(values.values())) for key, values in input_dict.items()], key=lambda x:x[1])
        
        # this prints out the end parts. if the first letter in template is the most common one, we need to plus 1.
        print(stats[-1][1] - stats[0][1])

if __name__ == '__main__':
    main()

    
   
    