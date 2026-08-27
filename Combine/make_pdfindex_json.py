import ROOT
import json
import sys

infile, ext = sys.argv[1], sys.argv[2]

f = ROOT.TFile.Open(infile)
w = f.Get("w")
w.loadSnapshot("MultiDimFit")

result = {}
for c in w.allCats():
    if c.GetName().startswith("pdfindex"):
        result[c.GetName()] = c.getIndex()

outname = "pdfindex%s.json" % ext
with open(outname, "w") as fout:
    json.dump(result, fout, indent=4)
print("wrote %s with %d categories" % (outname, len(result)))
