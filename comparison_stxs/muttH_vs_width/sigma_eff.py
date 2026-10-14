# sigma_eff (half-width of the narrowest m_gg window containing 68.27%) of the ttH signal, summed over all categories
# with each category weighted by its expected ttH yield, read from the combine workspaces. Also per category.
import ROOT, sys, re

ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

def sigma_eff(xs, ys, frac=0.6827):
    tot = sum(ys)
    cdf, c = [], 0.
    for y in ys:
        c += y
        cdf.append(c / tot)
    best, j = None, 0
    for i in range(len(xs)):
        while j < len(xs) and cdf[j] - (cdf[i - 1] if i else 0.) < frac:
            j += 1
        if j == len(xs): break
        w = xs[j] - xs[i]
        if best is None or w < best: best = w
    return 0.5 * best

def run(fn, procpat, catpat, label):
    w = ROOT.TFile.Open(fn).Get("w")
    if w.var("MH"): w.var("MH").setVal(125.)
    for p in ("lumi_scale", "mu_ttH", "mu_ttH_norm", "k_lambda"):
        if w.var(p): w.var(p).setVal(1.)
    m = w.var("CMS_hgg_mass")
    xs = [115. + 0.01 * i for i in range(2001)]  # 115-135 GeV
    tot = [0.] * len(xs)
    percat = {}
    for o in w.allPdfs():
        mm = re.match(r"shapeSig_(.+)_(" + catpat + ")$", o.GetName())
        if not mm or not re.match(procpat, mm.group(1)): continue
        proc, cat = mm.group(1), mm.group(2)
        n = w.function("n_exp_final_bin%s_proc_%s" % (cat, proc)).getVal()
        norm = ROOT.RooArgSet(m)
        ys = []
        for x in xs:
            m.setVal(x)
            ys.append(n * o.getVal(norm))
        tot = [a + b for a, b in zip(tot, ys)]
        pc = percat.setdefault(cat, [0.] * len(xs))
        percat[cat] = [a + b for a, b in zip(pc, ys)]
    nsig = sum(tot) * 0.01
    print("== %s: ttH yield %.2f (lumi_scale = 1), inclusive sigma_eff = %.3f GeV" % (label, nsig, sigma_eff(xs, tot)))
    for cat in sorted(percat, key=lambda c: -sum(percat[c])):
        print("   %-42s yield %6.2f  sigma_eff %.3f GeV" % (cat, sum(percat[cat]) * 0.01, sigma_eff(xs, percat[cat])))

run(sys.argv[1], r"TTH__", r"(?:hadr|lept)_C1_[A-Z0-9_]+", "Run 3 C1 binning (2022-2024)")
run(sys.argv[2], r"ttH_", r"ch1_RECO_TTH_[A-Za-z0-9_]+?", "Run 2 STXS")
