#===========================================================================
#
#                           PUBLIC DOMAIN NOTICE
#              National Center for Biotechnology Information
#
# This software/database is a "United States Government Work" under the
# terms of the United States Copyright Act.  It was written as part of
# the author's official duties as a United States Government employee and
# thus cannot be copyrighted.  This software/database is freely available
# to the public for use. The National Library of Medicine and the U.S.
# Government have not placed any restriction on its use or reproduction.
#
# Although all reasonable efforts have been taken to ensure the accuracy
# and reliability of the software and data, the NLM and the U.S.
# Government do not and cannot warrant the performance or results that
# may be obtained by using this software or data. The NLM and the U.S.
# Government disclaim all warranties, express or implied, including
# warranties of performance, merchantability or fitness for any particular
# purpose.
#
# Please cite the author in any work or product based on this material.
#
#===========================================================================
#
import sys
import traceback

from ngs import NGS
from ngs.ErrorMsg import ErrorMsg
from ngs.ReadCollection import ReadCollection
from ngs.Alignment import Alignment
from ngs.AlignmentIterator import AlignmentIterator
from ngs.Reference import Reference

def run(acc, refName, start, stop): # this function doesn't release NGS objects however it might
    # open requested accession using SRA implementation of the API
    run = NGS.openReadCollection(acc)
    run_name = run.getName()
    
    # get requested reference
    ref = run.getReference(refName)

    # start iterator on requested range
    it = ref.getAlignmentSlice(start, stop-start+1, Alignment.primaryAlignment)
    i = 0
    while it.nextAlignment():
        print ("%s\t%s\t%d\t%s\t%s" % (
            it.getReadId(),
            it.getReferenceSpec(),
            it.getAlignmentPosition(),
            it.getLongCigar(False),
            it.getAlignedFragmentBases(),
            ))
        i += 1
    print ("Read %d alignments for %s" % (i, run_name))

if len(sys.argv) != 5:
    print ("Usage: AlignSliceTest accession reference start stop\n")
    exit(1)
else:
    try:
        run(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    except ErrorMsg, x:
        print (x)
        traceback.print_exc()
        # x.printStackTrace - not implemented
        exit(1)
    except BaseException, x:
        traceback.print_exc()
        exit(1)
