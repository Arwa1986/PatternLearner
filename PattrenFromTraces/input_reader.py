import os, shutil

"""
version: 3.0
"""

def import_input(input_file):
    accepted = []
    rejected = []
    reading_status = ''

    input = [l.strip().lower() for l in open(input_file).readlines()]

    for line in input:

        if not line or line.strip().startswith("#") or line.strip() == '':
            continue
        if line in ['postive sequences', 'positive sequences', 'negative sequences']:
            reading_status = line
            continue

        if reading_status in  ['positive sequences', 'postive sequences']:
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').split(',') if l != ""]
            nodes = ",".join(nodes)+','
            accepted.append(nodes)
        elif reading_status == 'negative sequences':
            nodes = [l.strip().upper() for l in line.replace('[','').replace(']','').split(',') if l != ""]
            nodes = ",".join(nodes) + ','
            rejected.append(nodes)

#    build_adjs_matrix('evaluation/exp.txt')
    return accepted, rejected

def build_adjs_matrix(input_file):
    # open original file
    input = [l.strip().lower() for l in open(input_file).readlines()]

    # create file named "matrixOfRefrencedAuotmata.adjlist"
    # W: will overwirte any previous contents
    f = open("test_cases\matrixOfRefrencedAuotmata.adjlist", "w")

    for line in input:
        if not line or line.strip().startswith("#") or line.strip() == '':
            continue
        elif line in ['postive sequences', 'positive sequences', 'negative sequences']:
            break

        list = [l.strip().upper() for l in line.replace(' - ',',').replace(' -> ',',').split(',') if l != ""]
        row = list[0] + ' ' +list[2] + ' ' + list[1] +'\n'
        f.write(row)

    f.close()


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
    accepted, rejected= import_input('exp1.txt')

    print('accepted', accepted)
    print('rejected', rejected )

    # build_adjs_matrix('adjMatrix.txt')

