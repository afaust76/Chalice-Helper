from fileobj import File
from os import getcwd, listdir, mkdir, chdir
from os.path import isfile


# The Directory object contains the File objects associated with the Chalice
# files in the directory
class Directory:
    # Creates Directory object associated with the current directory
    def __init__(self):
        # path is the path to the directory that the object is associated with
        self.path = getcwd()
        # files is the list of File objects associated with the Chalice files
        # in the directory
        self.files = []
        # numfiles is the number of Chalice files in the directory
        self.numfiles = 0
        # filenames is a list of the names of all the items in the directory
        filenames = listdir(self.path)
        filenames.sort()
        # Iterates through the names of the items
        for f in filenames:
            # If the item is a Chalice file
            if (isfile(f) & f.endswith(".chalicetab")):
                # Creates a File object associated with that item and add it to
                # the directory's list of files
                self.files.append(File(f))
                self.numfiles += 1

    # Exports a text file containing the entry summaries for all files in the
    # directory
    def export(self):
        # If there are files
        if (len(self.files) > 0):
            # If the destination folder does not exist, it is created
            filenames = listdir(getcwd())
            if ("Chalice_Helper_Entry_Summaries" not in filenames):
                mkdir("Chalice_Helper_Entry_Summaries")
            chdir("Chalice_Helper_Entry_Summaries")

            # Creates a list of entry summaries from the files
            lines = []
            for f in self.files:
                temp = f.selected
                f.selected = list(range(f.numentries))
                f.reset_summary()
                summary = f.summarylist()
                lines.append(f.name)
                lines.extend(summary)
                lines.append("\n")
                f.selected = temp
                f.reset_summary()

            # Outputs the summaries to a file
            fileobj = open("Folder Summary.txt", "w")
            fileobj.write("\n".join(lines))
            fileobj.close()
            chdir("..")