puzzle_input = 359282, 820401


def derive_numbers(current: str, numbers: str):
    if len(current) == 6:
        if not (puzzle_input[0] <= int(current) <= puzzle_input[1]):
            return []

        if len(set(current)) == 6:
            return []

        return [current]

    results = []
    for i in range(len(numbers)):
        results.extend(derive_numbers(current + numbers[i], numbers[i:]))

    return results


print(len(derive_numbers('', '3456789')))


def derive_numbers_part_2(numbers='3456789'):
    candidates = derive_numbers('', numbers)
    results = []

    for candidate in candidates:
        count_map = {n: 0 for n in numbers}
        for letter in candidate:
            count_map[letter] += 1

        for count in count_map.values():
            if count == 2:
                results.append(candidate)
                break

    return results


print(len(derive_numbers_part_2()))
