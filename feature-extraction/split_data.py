import sys
from sklearn.model_selection import train_test_split

# Default values
train_size_default = 0.6
seed = 2 # Not currently used, but can be applied to split function

def write_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as out_data:
        for file_inst in data:
            out_data.write("{}\n".format(file_inst))

def split_data(file_instances, train_size):
    names = []
    # Read file with instances names
    with open(file_instances, "r", encoding='utf-8') as f_inst_handle:
        for inst_line in f_inst_handle.readlines():
            inst_line = inst_line[:-1]
            if not inst_line.startswith("#") and inst_line.endswith(".txt"):
                names.append(inst_line)
    
    # Split data to training and testing sets
    train, test = train_test_split(names, train_size=train_size, shuffle=True)

    # Save data
    write_data("training_instances.txt", train)
    write_data("testing_instances.txt", test)



if __name__ == "__main__":
    file_names_instances = sys.argv[1]
    train_size = float(sys.argv[2]) if (len(sys.argv) > 2) else train_size_default # set split size to training data
    split_data(file_names_instances, train_size)