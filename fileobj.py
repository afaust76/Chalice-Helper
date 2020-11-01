from entry import Entry
import sys
from os import listdir, getcwd, mkdir, chdir


# Takes in a list of indexes and returns a formatted string to represent them
def hyphenate(numbers):
    ranges = []
    stack = []

    if(len(numbers) == 1):
        return str(numbers[0] + 1)

    # Iterates through the indexes
    for i in numbers:
        # Adjusts the index to refer to the ID
        i += 1
        # If the stack is empty
        if (len(stack) == 0):
            stack.append(i)
        # If the index is part of a continuous range
        elif (i == stack[-1] + 1):
            stack.append(i)
        # If the index breaks the continuous range
        else:
            # If the broken range was only one value
            if (len(stack) == 1):
                ranges.append(str(stack[0]))
            # If the broken range was multiple values
            else:
                ranges.append(str(stack[0]) + "-" + str(stack[-1]))
            # Starts a new range
            stack = [i]

    # If there are still values on the stack
    if (len(stack) != 0):
        # If the remaining range is only one value
        if (len(stack) == 1):
            ranges.append(str(stack[0]))
        # If the remaining range is multiple values
        else:
            ranges.append(str(stack[0]) + "-" + str(stack[-1]))

    return ",".join(ranges);


# The File object contains the Entry objects associated with the entries in
# the Chalice file
class File:
    # Takes in the name of the file associated with the File object
    def __init__(self, name):
        # name is the name of the associated file
        self.name = name
        # numentries is the number of entries in the file
        self.numentries = 0
        # entries is the list of Entry objects corresponding to the file's
        # entries
        self.entries = []
        # selected is a list continaing the indexes of the entries selected
        # to be summarized
        self.selected = []
        # variables contains the values entered for the selected entries'
        # parameters
        self.variables = []
        for i in range(1,21):
            self.variables.append(set())

        # Opens the file and reads in the lines of text
        fileobj = open(self.name)
        if (fileobj.closed):
            print("Error opening file: " + self.name)
            sys.exit(1)
        lines = fileobj.readlines()
        fileobj.close()

        # Iterates through the lines of text in the file
        entbegin = 0
        linenum = 0
        for l in lines:
            # "id" line is designated as the start of the next entry
            if (l[0:2] == "id"):
                # If it is not the first "id" line
                if (linenum != 0):
                    # Creates an entry from previous lines and adds it to the
                    # file's list of entries
                    self.entries.append(Entry(lines[entbegin:linenum],
                                              entbegin))
                    self.numentries += 1
                # Updates the beginning of the entry
                entbegin = linenum
            # If the end of the file has been reached
            if (linenum + 1 == len(lines)):
                # Creates an entry from remaining lines and adds it to the
                # file's list of entries
                self.entries.append(Entry(lines[entbegin:],entbegin))
                self.numentries += 1
            # Updates the current line number
            linenum += 1

    # Searches all the entries for those with a certain value for a certain
    # parameter
    def search(self,param,value):
        for i in range(0,self.numentries):
            entry = self.entries[i]
            if ((param < 15) & (entry.variables[param] == value)):
                self.selected.append(i)
            elif ((param in [16, 17]) & ((entry.variables[16] == value)
                 | (value in entry.variables[17]))):
                self.selected.append(i)
            elif ((param in [15, 19]) & ((entry.variables[15] == value)
                 | (value in entry.variables[19]))):
                self.selected.append(i)
            elif ((param in [18, 20]) & (value in entry.variables[param])):
                self.selected.append(i)
            else:
                pass

    # Searches selected entries for those with a certain value for a certain
    # parameter
    def searchselected(self,param,value):
        indexes = self.selected
        self.selected = []

        for i in indexes:
            entry = self.entries[i]
            if ((param < 15) & (entry.variables[param] == value)):
                self.selected.append(i)
            elif ((param in [16, 17]) & ((entry.variables[16] == value)
                 | (value in entry.variables[17]))):
                self.selected.append(i)
            elif ((param in [15, 19]) & ((entry.variables[15] == value)
                 | (value in entry.variables[19]))):
                self.selected.append(i)
            elif ((param in [18, 20]) & (value in entry.variables[param])):
                self.selected.append(i)
            else:
                pass

    # Updates the summary of the selected entries' parameters
    def reset_summary(self):
        # Discards the previous summary
        self.variables = []
        for i in range(1,21):
            self.variables.append(set())

        # Repopulates the summary with the values of the selected entries'
        # parameters
        for i in self.selected:
            entry = self.entries[i]
            for i in range(0,16):
                self.variables[i].add(entry.variables[i + 1])
            for i in range(16,20):
                self.variables[i] |= entry.variables[i + 1]

    # Returns the summary of selected entries as a list of strings
    def summarylist(self):
        return (["id: " + hyphenate(self.selected)
                , "protocol: " + (", ".join(self.variables[0]))
                , "datasource: " + (", ".join(self.variables[1]))
                , "Test Type: " + (", ".join(self.variables[2]))
                , "Biobook Notebook Experiment ID: "
                    + (", ".join(self.variables[3]))
                , "Cell Line: " + (", ".join(self.variables[4]))
                , "Cell Line Background: " + (", ".join(self.variables[5]))
                , "Cancer Type: " + (", ".join(self.variables[6]))
                , "Assay Start: " + (", ".join(self.variables[7]))
                , "Assay Length: " + (", ".join(self.variables[8]))
                , "Assay Endpoint: " + (", ".join(self.variables[9]))
                , "Screen Name: " + (", ".join(self.variables[10]))
                , "Experimenter: " + (", ".join(self.variables[11]))
                , "Cell Density: " + (", ".join(self.variables[12]))
                , "Plate Format: " + (", ".join(self.variables[13]))
                , "Compound-D: " + (", ".join(self.variables[14]))
                , "Compound-A: " + (", ".join(self.variables[15]))
                , ""
                , "Compound-A Designation: "
                    + (", ".join(self.variables[16]))
                , "Compound-A Name: " + (", ".join(self.variables[17]))
                , "Compound-D Designation: "
                    + (", ".join(self.variables[18]))
                , "Compound-D Name: " + (", ".join(self.variables[19]))])

    # Exports the displayed entry summary to a text file
    def export(self, params):
        # If the destination folder does not already exist, it is created
        filenames = listdir(getcwd())
        if ("Chalice_Helper_Entry_Summaries" not in filenames):
            mkdir("Chalice_Helper_Entry_Summaries")
        # Goes into the destination folder
        chdir("Chalice_Helper_Entry_Summaries")
        # Opens the file for writing
        file = open(self.name[0:-11] + " entries " + hyphenate(self.selected)
             + ".txt", "w")

        summary = self.summarylist()
        temp = 0
        for i in range(17):
            if(params[i] == 1):
                file.write(summary[i]+"\n")
                temp = 1
        if(temp == 1):
            file.write("\n")
        for i in range(17,21):
            if(params[i] == 1):
                file.write(summary[i + 1] + "\n")

        # Closes the file
        file.close()
        # Returns to main directory
        chdir("..")

    # Updates the value of the specified parameter in all selected entries
    # and in the file containg them
    def update_range(self, param, value):
        # Opens the file and reads in the lines of text
        fileobj = open(self.name)
        if (fileobj.closed):
            print("Error editing file")
            sys.exit(1)
        lines = fileobj.readlines()
        fileobj.close()

        # Iterates through the selected entries
        for i in self.selected:
            entry = self.entries[i]
            # If editing a parameter that does not appear in the lines of data
            if (param < 15):
                entry.variables[param] = value
            # If editing Compound-A's value
            elif (param in [16, 17]):
                entry.variables[16] = value
                entry.variables[17] = {value}
            # If editing Compound-D's value
            elif (param in [15, 19]):
                entry.variables[15] = value
                entry.variables[19] = {value}
            # If editing Compound-A or Compound-D's names
            else:
                entry.variables[param] = {value}

            # If changing one of the parameters, the relevant line is updated
            if((param != 18) & (param != 20)):
                pos = 0
                if(param == 19):
                    pos = 15
                elif(param == 17):
                    pos = 16
                else:
                    pos = param
                line = lines[entry.beginparams + pos]
                tok = line.split("\t")
                line = tok[0] + "\t" + tok[1] + "\t" + value + "\t\t\t\n"
                lines[entry.beginparams + pos] = line

            # If changing the data, the update is applied to all relevant lines
            if (param >= 15):
                # If changing the Compound-A lines
                if((param > 15) & (param < 19)):
                    for i in range(entry.beginAvals, entry.beginDvals):
                        tok = lines[i].split("\t")
                        # If updating the designation
                        if(param in [16, 17]):
                            lines[i] = "\t".join(tok[0:1] + [value] + tok[2:6])
                        # If updating the name
                        else:
                            lines[i] = "\t".join(tok[0:2] + [value] + tok[3:6])

                # If changing the Compound-D lines
                else:
                    for i in range(entry.beginDvals, (entry.beginDvals
                    + (entry.beginDvals - entry.beginAvals))):
                        tok = lines[i].split("\t")
                        # If updating the designation
                        if(param in [15, 19]):
                            lines[i] = "\t".join(tok[0:1] + [value] + tok[2:6])
                        # If updating the name
                        else:
                            lines[i] = "\t".join(tok[0:2] + [value] + tok[3:6])

        # Writes the lines of text back to the file
        fileobj = open(self.name, "w")
        for l in lines:
            fileobj.write(l)
        fileobj.close()