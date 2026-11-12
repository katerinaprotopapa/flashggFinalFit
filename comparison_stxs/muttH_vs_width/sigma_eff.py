# sigma_eff (half-width of the narrowest m_gg window containing 68.27%) of the ttH signal, summed over all categories
# with each category weighted by its expected ttH yield, read from the combine workspaces. Also per category.
# Then a summary with the same quantity for all Higgs processes (each weighted by its expected yield), with the Run 2
# ttH xs at 13 TeV (ttH_xs_13p6_scale = 1) and at 13.6 TeV (workspace default 1.130): x-positions of the Run 2 points.
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

def run(fn, procpat, catpat, label, setvars=None, verbose=True):
    w = ROOT.TFile.Open(fn).Get("w")
    if w.var("MH"): w.var("MH").setVal(125.)
    for p in ("lumi_scale", "mu_ttH", "mu_ttH_norm", "k_lambda"):
        if w.var(p): w.var(p).setVal(1.)
    for p, v in (setvars or {}).items():
        if w.var(p): w.var(p).setVal(v)
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
    se = sigma_eff(xs, tot)
    print("== %s: yield %.2f (lumi_scale = 1), inclusive sigma_eff = %.3f GeV" % (label, nsig, se))
    if not verbose:
        return se
    for cat in sorted(percat, key=lambda c: -sum(percat[c])):
        print("   %-42s yield %6.2f  sigma_eff %.3f GeV" % (cat, sum(percat[cat]) * 0.01, sigma_eff(xs, percat[cat])))

C1CATS, R2CATS = r"(?:hadr|lept)_C1_[A-Z0-9_]+", r"ch1_RECO_TTH_[A-Za-z0-9_]+?"
run(sys.argv[1], r"TTH__", C1CATS, "Run 3 C1 binning (2022-2024), ttH")
run(sys.argv[2], r"ttH_", R2CATS, "Run 2 STXS, ttH")

# Summary: Run 2 / Run 3 sigma_eff ratio (x-position of the Run 2 point on the width plot), ttH only and all Higgs
print("\n== Summary (MH = 125 GeV)")
r3 = {"ttH": run(sys.argv[1], r"TTH__", C1CATS, "Run 3 C1, ttH", verbose=False),
      "all": run(sys.argv[1], r".+", C1CATS, "Run 3 C1, all Higgs", verbose=False)}
for e, v in (("13TeV", 1.0), ("13p6TeV", 1.1301410689449634)):
    for k, pat in (("ttH", r"ttH_"), ("all", r".+")):
        se = run(sys.argv[2], pat, R2CATS, "Run 2 STXS %s, %s" % (e, "ttH" if k == "ttH" else "all Higgs"),
                 setvars={"ttH_xs_13p6_scale": v}, verbose=False)
        print("   -> Run 2 %-7s %-3s sigma_eff %.3f / Run 3 %.3f = width scale %.3f" % (e, k, se, r3[k], se / r3[k]))
