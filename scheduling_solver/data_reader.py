def ler_instancia(file):
    lines = file.read().decode('utf-8').splitlines()
    n = int(lines[0].strip().split('=')[1])
    processing_times = list(map(int, lines[1].strip().split('=')[1].strip('()').split(',')))
    precedence_constraints = []
    setup_times = []
    reading_A = False
    reading_S = False
    for line in lines[2:]:
        if 'A=' in line:
            reading_A = True
            continue
        if 'Sij=' in line:
            reading_A = False
            reading_S = True
            continue
        if reading_A:
            i, j, d = map(int, line.strip().split(','))
            precedence_constraints.append((i, j, d))
        if reading_S:
            setup_times.append(list(map(int, line.strip().split(','))))

    return n, processing_times, precedence_constraints, setup_times