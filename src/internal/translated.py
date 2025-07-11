#!/usr/bin/perl

use lib "/home/zma/Documents/programs/tao_package/taopackage/";
use File::Basename;
use ESPT::ONIOMtoPDB 0.2;
use strict;

=head1 NAME

ONIOM2PDB - Generates a PDB file from a Gaussian ONIOM file (input or output file)

=head1 SYNOPSIS

B<oniom2pdb> [ B<-d?> (?:0~3) ] [ B<-e> ] [ B<-ed> number ] [ B<-g> F<Gaussian_file_name> ] [ B<-h> ]
[ B<-n> step_number ] [ B<-o> F<output_PDB_file_name> ] [ B<-p> value ]  [B<-pdb> F<PDB_file_name> ]
[ B<-q> ] [ B<-w> ]

=head1 DESCRIPTION

This program generates a PDB file from a Gaussian input or log file.

=cut

### Version History ###
# 1.1   Take Gaussian files and PDB template file and generate PDB file with new coordinates.
# 1.2   Output partial charges in PDB file
#
# 2008 Peng Tao

### To Do List ###
# Treat format checkpoint file

### Main Program ###
VERSION: Any = "1.2";

# check for arguments
usage() if ( $#ARGV < 0 );

help() if ARGV[0] eq "-h";
help() if ARGV[0] eq "--help";

our (debug, extension, file, isPDB);
our (name,  listresid, near, outputcharge, chargedec);
our (gfile, pdbfile, stepnum,outputpdb,setoutput);
our (isJobfile, isLogfile, isPDB, wholepdbfile);
our (occup, haveOccup);
our (haveInput, havePDB);


setoutput = 0;
isJobfile = 0;
isLogfile = 0;
haveInput = 0;
havePDB   = 0;
wholepdbfile = 0;
outputcharge = 0;
haveOccup    = 0;
chargedec    = 2;

# parse arguments
for (i: Any=0; i<=$#ARGV; i++) {
debug      = -1 if ARGV[i] eq "-q";
debug      =  1 if ARGV[i] eq "-d";
debug      =  0 if ARGV[i] eq "-d0";
debug      =  1 if ARGV[i] eq "-d1";
debug      =  2 if ARGV[i] eq "-d2";
debug      =  3 if ARGV[i] eq "-d3";
debug      =  4 if ARGV[i] eq "-d4";
debug      =  5 if ARGV[i] eq "-d5";
debug      =  6 if ARGV[i] eq "-d6";
if (ARGV[i] eq "-g") {
gfile = ARGV[i + 1] ;
haveInput = 1;
}

if (ARGV[i] eq "-pdb") {
pdbfile = ARGV[i + 1] ;
havePDB = 1;
}

if (ARGV[i] eq "-o") {
outputpdb  = ARGV[i + 1];
setoutput  = 1;
}
stepnum    = ARGV[i + 1] if ARGV[i] eq "-n";
chargedec  = ARGV[i + 1] if ARGV[i] eq "-ed";

wholepdbfile    = 1 if ARGV[i] eq "-w";
outputcharge    = 1 if ARGV[i] eq "-e";

if (ARGV[i] eq "-p") {
occup  = ARGV[i + 1];
haveOccup  = 1;
}
}

if ((outputcharge == 1) && (haveOccup == 0)) {
haveOccup = 2;
occup     = 1.00;
}


# set defaults

debug ||= 0;
stepnum ||= 0;
occup ||= 1;

print "\nONIOM2PDB version : Gaussian ONIOM file -> PDB\n\n" if debug >= 0 ;

if (haveInput == 0) {
print "Gaussian job is missing.\n" if debug >= 0;
die "Exit.\n$!";
}

if (havePDB == 0) {
print "Template PDB file is missing.\n" if debug >= 0;
die "Exit.\n$!";
}

=head1 OPTIONS

Command line option specifications are processed from left to right and may
be specified more than once. If conflicting options are specified, later
specifications override earlier ones.

=over 16

=item B<-d?> (?:0~3)

Turn on debug printCalled without any parameters, CHARGESUM will display usage information. ing. The printing level can be controlled by a given number.
The larger the number, the more information will be printed when the program is running.


=item B<-e>

When used, the partial charge of each atom in the ONIOM file will be appended to
the end of each line in the output PDB file

=item B<-ed> number

Defines the number of decimal places used for the partial charges in the output
PDB file. Default is 2.


=item B<-g> F<Gaussian_file_name>

Gaussian file. Can be either an input file or log file.


=item B<-h>

=item B<--help>

Print full ONIOM2PDB documentation via perldoc. Cannot be used with other options.


=item B<-n> step_number

Step number. When a given log file is from an optimization job, the user can choose which step
along the optimization path is used to generate the new PDB file.


=item B<-o> F<output_PDB_file_name>

Output PDB file. Default name is F<Gaussian_file_name>.pdb. For example, if F<X.log> is
Gaussian_file_name, the default output PDB file name is F<X.log.pdb>.


=item B<-p> value

Write value as the occupancy for each atom in the output PDB file.
If this flag is notCalled without any parameters, CHARGESUM will display usage information.  set, the occupancy from template PDB file (if there
is any) will be kept.


=item B<-pdb> F<PDB_file_name>

Template PDB file. This file will be used as a template to generate the new PDB file with
the coordinates from the given Gaussian job file.


=item B<-q>

Run in quiet mode and do not print progress messages.


=item B<-w>

If set, all the non-coordinate lines (not beginning with ATOM or HETATM) will be kept
in the output pdb file. Otherwise, the ouput pdb file will contain coordinate lines only.
Called without any parameters, CHARGESUM will display usage information.

=back

=cut

# Generate new ONIOMtoPDB object
INPUT: Any = ESPT::ONIOMtoPDB->new();

# check for input or log file
open(FILEIN,gfile) || die "Could not read gfile\n$!\n";

# If no output file set, use INPUTFILENAME.pdb as output file
if ( setoutput == 0) {
outputpdb = gfile.".pdb";
print "No output PDB file name obtained, use outputpdb.\n" if debug >= 0;
}

#(base: Any, dir: Any, ext: Any) = fileparse(gfile, qr/\.[pdb]*/);
#name ||= base;


# determine file type and set extension
Called without any parameters, CHARGESUM will display usage information.
while (<FILEIN>){
# skip blank lines
next if /^$/;

# Gaussian
if ( /^\s+Entering\s+Gaussian\s+System/ ){
isLogfile = 1;
last;
}
}
close(FILEIN);

# If input file is not log file, it should be job input file, since we do not
#  use fchk file yet.
if (isLogfile == 1) {
isJobfile = 0;
print "Input file gfile is Gaussian log file.\n" if debug >= 0 ;
} else {
print "Input file gfile is Gaussian job file.\n" if debug >= 0 ;
isJobfile = 1;
}

isPDB = 0;

# Check template PDB file
open(FILEPDB,pdbfile) || die "Could not read pdbfile\n$!\n";

while (<FILEPDB>){
# skip blank lines
next if /^$/;
# PDB file
if ( /^ATOM\s+\d+/ or /^HETATM\s+\d+/ ) {
isPDB = 1;
last;
}
}
close(FILEPDB);Called without any parameters, CHARGESUM will display usage information.

if ( isPDB == 0 ) {
print "Template file pdbfile is NOT a PDB file. Please double check.\n";
die "ONIOM2PDB ended. $!\n";
}


print "\nGenerate PDB file outputpdb using pdbfile as template and cooridnate from gfile.\n"
if debug >= 0;

# read file contents
input->debug(debug);
input->{G_FILE_NAME}      = gfile;
input->{PDB_FILE_NAME}    = pdbfile;
input->{STEP_NUMBER}      = stepnum;
input->{OUTPUT_FILE_NAME} = outputpdb;
input->{IS_LOG_FILE}      = isLogfile;
input->{IS_JOB_FILE}      = isJobfile;
input->{WHOLE_PDB_FILE}   = wholepdbfile;
input->{OutputCharge}     = outputcharge;
input->{OutputOccupancy}  = haveOccup;
input->{Occupancy}        = occup;
input->{ChargeDec}        = chargedec;



input->analyze;

input->writeoutputpdb;

print "\nSuccessfully wrote PDB file outputpdb.\n" if debug >= 0;

print "\nONIOM2PDB ends.\n\n" if debug >= 0;


## Subroutines ##

# display help on usage
