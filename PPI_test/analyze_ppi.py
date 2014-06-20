#!/usr/bin/python

import foldx, re, shutil, random, os, math, sys, subprocess, glob
import numpy as np
from Bio import *
import Bio.PDB as PDB

def main():
  start_structure = '2eke.bak'

  ancestral_structure1 = capture_pdb(start_structure[0:-4] + '_A.pdb', start_structure, 'A')
  ancestral_structure2 = capture_pdb(start_structure[0:-4] + '_C.pdb', start_structure, 'C')

  #make_combined_file([ancestral_structure1, ancestral_structure2], start_structure[0:-4] + '_combined.pdb')
  
  all_pdbs = glob.glob('*.pdb')
  final_pdb_list = []
  for a_file in all_pdbs:
    if 'wt' not in a_file:
      final_pdb_list.append(a_file)

  print(final_pdb_list)

  #Make binding comparison using ancestral chain A
  for a_file in ['A43K.pdb']:
    ancestral_structure1 = capture_pdb(start_structure[0:-4] + '_A.pdb', start_structure, 'A')
    new_structure2 = capture_pdb(a_file[0:-4] + '_C.pdb', a_file, 'C')
    new_combo = new_structure2[0:-4] + '_combined.pdb'
    combined_file = make_combined_file([ancestral_structure1, new_structure2], new_combo)
    foldx.runFoldxRepair(a_file, [combined_file])
    repair_file = glob.glob('Repair*.pdb')
    shutil.move(repair_file[0], new_combo)
    foldx.runFoldxAnalyzeComplex(new_combo[0:-4], [new_combo])

    ancestral_structure2 = capture_pdb(start_structure[0:-4] + '_C.pdb', start_structure, 'C')
    new_structure1 = capture_pdb(a_file[0:-4] + '_A.pdb', a_file, 'A')
    new_combo = new_structure1[0:-4] + '_combined.pdb'
    combined_file = make_combined_file([new_structure1, ancestral_structure2], new_combo)
    foldx.runFoldxRepair(a_file, [combined_file])
    repair_file = glob.glob('Repair*.pdb')
    shutil.move(repair_file[0], new_combo)
    foldx.runFoldxAnalyzeComplex(new_combo[0:-4], [new_combo])

    score_ob = foldx.Scores()
    score_ob.parseAnalyzeComplex()

    iden1 = calc_identity(ancestral_structure1, new_structure1)
    inter1 = score_ob.getInteractionEnergies()[0]
    iden2 = calc_identity(ancestral_structure2, new_structure2)
    inter2 = score_ob.getInteractionEnergies()[1]

    print(iden1)
    print(inter1)
    print(iden2)
    print(inter2)

    score_ob.cleanUp([])

  clean_up(['*_*.pdb'])

def capture_pdb(out_name, fn, chain_letter):
  parser = PDB.PDBParser()
  structure = parser.get_structure('working_pdb', fn)
  
  writer = PDB.PDBIO()
  writer.set_structure(structure)
  writer.save(out_name, select=SelectChains(chain_letter))
  return(out_name)
    
def calc_identity(fn1, fn2):
  parser = PDB.PDBParser()
  structure1 = parser.get_structure('working_pdb1', fn1)
  structure2 = parser.get_structure('working_pdb2', fn2)

  count = 0
  identical = 0

  ppb1 = PDB.PPBuilder()
  pp1 = (ppb1.build_peptides(structure1)[0]).get_sequence()

  ppb2 = PDB.PPBuilder()
  pp2 = (ppb2.build_peptides(structure2)[0]).get_sequence()

  for i in range(0, len(pp1)):
     if pp1[i] == pp2[i]:
       identical += 1
     count += 1

  return(float(identical)/float(count))

class SelectChains(PDB.Select):
  """ Only accept the specified chains when saving. """
  def __init__(self, chain_letters):
    self.chain_letters = chain_letters

  def accept_chain(self, chain):
    return (chain.get_id() in self.chain_letters)

def make_combined_file(files, path):
  with open(path, 'w') as outfile:
    for fname in files:
      with open(fname) as infile:
        for line in infile:
          outfile.write(line)
  subprocess.call("sed -i 's/END//g' " + path, shell=True)
  return(path)

def clean_up(delete_files):
  import glob
  for name in delete_files:
    for files in glob.glob(name):
      if os.path.isfile(files):
        os.remove(files)

#Run main program
if __name__ == '__main__':
   main()
