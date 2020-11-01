import sys


# The Entry object contains the values entered for each parameter in the
# associated entry
class Entry:
    # Takes in the lines of text that compose the entry, the line number where
    # the entry begins in the file
    def __init__(self, lines, firstline):
        # datalines is a list of the lines of text containing the data
        # concerning Compound-A and Compound-D
        datalines = lines[17:]
        # variables is a list of the parameter values of the associated entry
        self.variables = []
        # beginparams is the line number where the entry begins in the file
        self.beginparams = firstline
        # beginAvals is the line number where the data concerning Compound-A
        # begins in the file
        self.beginAvals = firstline + 17

        # Extracts the entered parameter values from the text
        self.variables.append(lines[0][6:-4]) # ID
        self.variables.append(lines[1][18:-4]) # protocol
        self.variables.append(lines[2][22:-4]) # datasource
        self.variables.append(lines[3][18:-4]) # Test Type
        self.variables.append(lines[4][41:-4]) # BNEID
        self.variables.append(lines[5][20:-4]) # Cell Line
        self.variables.append(lines[6][31:-4]) # Cell Line B
        self.variables.append(lines[7][22:-4]) # Cancer Type
        self.variables.append(lines[8][22:-4]) # Assay Start
        self.variables.append(lines[9][23:-4]) # Assay Length
        self.variables.append(lines[10][25:-4]) # Assay End
        self.variables.append(lines[11][22:-4]) # Screen Name
        self.variables.append(lines[12][23:-4]) # Experimenter
        self.variables.append(lines[13][23:-4]) # Cell Density
        self.variables.append(lines[14][23:-4]) # Plate format
        self.variables.append(lines[15][21:-4]) # Compound D
        self.variables.append(lines[16][21:-4]) # Compound A
        self.variables.append(set()) # Compound-A values (17)
        self.variables.append(set()) # Compound-A names (18)
        self.variables.append(set()) # Compound-D vals (19)
        self.variables.append(set()) # Compound-D names (20)

        # Iterates through the lines of text containing the Compound-A data
        linenum = 0
        for l in datalines:
            # If the beginning of the lines containing Compound-D data is
            # reached, iteration stops
            if ((l[0:2] == "1\t") & (linenum != 0)):
                break
            # Extracts the entered values for Compound-A and adds them to
            # the relevant sets of values
            tokens = l.split("\t")
            if("" in tokens):
                print("Error parsing file")
                sys.exit(1)
            self.variables[17].add(tokens[1])
            self.variables[18].add(tokens[2])
            linenum += 1

        # beginDvals is the line number where the data concerning Compound-D
        # begins in the file
        self.beginDvals = firstline + 17 + linenum

        # Iterates through the lines of text containing the Compound-D data
        for l in datalines[linenum:]:
            # Extracts the entered values for Compound-D and adds them to
            # the relevant sets of values
            tokens = l.split("\t")
            self.variables[19].add(tokens[1])
            self.variables[20].add(tokens[2])