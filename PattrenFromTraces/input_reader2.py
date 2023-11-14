import os, shutil

"""
version: 3.0
"""

def import_input(input_file):
    trainingPositive = []
    trainingNegative = []
    evaluationPositive = []
    evaluationNegative = []
    reading_status = ''

    input = [l.strip().lower() for l in open(input_file).readlines()]

    for line in input:

        if not line or line.strip().startswith("#") or line.strip() == '':
            continue

        if line in ['training positive:', 'training negative:', 'evaluation positive:', 'evaluation negative:']:
            reading_status = line
            continue

        if reading_status == 'training positive:':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').replace('\'','').split(',') if l != ""]
            trainingPositive.append(nodes)
        elif reading_status == 'training negative:':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').replace('\'','').split(',') if l != ""]
            trainingNegative.append(nodes)
        elif reading_status == 'evaluation positive:':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').replace('\'','').split(',') if l != ""]
            evaluationPositive.append(nodes)
        elif reading_status == 'evaluation negative:':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').replace('\'','').split(',') if l != ""]
            evaluationNegative.append(nodes)

    return trainingPositive, trainingNegative, evaluationPositive, evaluationNegative

def build_adjs_matrix(input_file):
    # open original file
    input = [l.strip().lower() for l in open(input_file).readlines()]

    # create file named "matrixOfRefrencedAuotmata.adjlist"
    # W: will overwirte any previous contents
    f = open("test_cases\matrixOfRefrencedAuotmata.adjlist", "w")

    for line in input:
        if not line or line.strip().startswith("#") or line.strip() == '':
            continue

        elif line in ['postive sequences', 'positive sequences', 'negative sequences', 'blocked_loop', 'k_tail', 'special_path']:
            break

        list = [l.strip().upper() for l in line.replace(' - ',',').replace(' -> ',',').split(',') if l != ""]
        # convert the list to string and re-arrange the
        # items to build the matrix
        # list = [state1, lable, state2]
        # row = state1 state2 lable
        row = list[0] + ' ' +list[2] + ' ' + list[1] +'\n'
        f.write(row)

    f.close()
    # # open and read the file after the overwriting:
    # f = open("test_cases\matrixOfRefrencedAuotmata.adjlist", "r")
    # print(f.read())

def clean_folder():
    folder = 'output'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == '__main__':

    trainingPositive, trainingNegative, evaluationPositive, evaluationNegative = import_input('output/traces.txt')

    print('trainingPositive: ', trainingPositive)
    print('trainingNegative: ', trainingNegative )
    print('evaluationPositive: ', evaluationPositive )
    print('evaluationNegative: ', evaluationNegative)

    # build_adjs_matrix('evaluation/exp.txt')

