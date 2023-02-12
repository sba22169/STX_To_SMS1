# The aim of this program is to take data from STX vcs file and numbers file and create a look up table
# and out put the name txt number and time of appointment for the customer.

def read_content(filename):
    with open(filename, 'r') as f:
        return f.read()


content = read_content(filename='Untitled.txt')

print(content)


