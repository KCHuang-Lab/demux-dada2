import numpy as np
import pandas as pd
import os
import sys

def checkInputs(ssPath, flPath, indPath):
    # Check that the paths are valid:
    if not (os.path.exists(ssPath) & os.path.exists(flPath) & os.path.exists(indPath)):
        print("Warning! One or more of the provided paths are invalid.")
        return
    else:
        pass
        
    # Read in the samplesheet, fastqlist, and indexfordemux file:
    ss = pd.read_table(ssPath)
    fl = pd.read_table(flPath)
    ind = pd.read_table(indPath)
    
    # Check that the fastqlist headings are right:
    cols = fl.columns.tolist()
    if 'read1' not in cols:
        print('Warning! "read1" column not found in fastqlist.')
    if 'read2' not in cols:
        print('Warning! "read2" column not found in fastqlist.')
    if 'file' not in cols:
        print('Warning! "file" column not found in fastqlist.')

    # Check that all the files included in the fastqlist exist:
    MissingReads = []
    for i in range(fl.shape[1]):
        for col in ['read1', 'read2']:
            j = fl[col][i]
            if not os.path.exists(j):
                MissingReads.append(j)
            # else:
            #     MissingReads.append(j)

    # Check that all the right headings are included in the samplesheet:
    cols = ss.columns.tolist()
    if 'filename' not in cols:
        print('Warning! "filename" column not found in fastqlist.')
    if 'sample' not in cols:
        print('Warning! "sample" column not found in fastqlist.')
    if 'group' not in cols:
        print('Warning! "group" column not found in fastqlist.')

    # Check that the filename and sample don't include any invalid characters (" ", "_", or "."):
    invalidChar = []
    for col in ['sample', 'filename']:
        for i in ss[col].tolist():
            if ("_" in i) | (" " in i) | ("." in i):
                invalidChar.append(i)
                print("Warning! Samplesheet entry %s contains invalid characters." % i)

    # Check that the 'filename' in the samplesheet matches the 'file' in fastqlist and existing phases:
    errorFilenames = []
    filenameNoPhase = []
    phases = ind['phase'].tolist()
    files = fl['file'].tolist()
    for i in ss['filename'].tolist():
        j = i.rpartition("-L")
        filenameNoPhase.append(j[0])
        if j[0] not in files:
            print("Warning! Filename %s does not have a corresponding file in fastqlist." % i)
            errorFilenames.append(i)
        if int(j[2]) not in phases:
            print("Warning! Phase in filename %s does not exist in index list." %i)
            errorFilenames.append(i)

    # Check that all files in the fastqlist are used in the samplesheet:
    errorFiles = []
    filenames = ss['filename'].tolist()
    fileSet = set(fl['file'].tolist())
    filenameSet = set(filenameNoPhase)
    if len(fileSet.difference(fileSet.intersection(filenameSet))) > 0:
        print("Warning! Some files in the fastqlist are not used in the samplesheet.")

    print("All done!")
    return

checkInputs(sys.argv[1], sys.argv[2], sys.argv[3])