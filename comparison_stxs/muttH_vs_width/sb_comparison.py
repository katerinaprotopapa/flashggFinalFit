# Per-category expected ttH signal S and background B in a window m_H +- sigma_eff around the peak, from the fitted
# signal and background models in the combine workspaces (no data). Three groups at the 2022-2024 luminosity
# (172.26 fb-1) and ttH xs at 13.6 TeV: Run 2 STXS ttH categories, Run 3 STXS ttH categories (Sep26), Run 3 C1 binning (aug26).
# B = continuum background (multipdf at the pdf indices used in the stat-only fits) + other Higgs processes (non-ttH).
# Approximate stat-only sigma(mu_ttH) = 1/sqrt(sum_cat S^2/(S+B)) ("information" = sum S^2/(S+B)).
#
# Usage (flashggFinalFit env, from flashggFinalFit/):  python3 comparison_stxs/muttH_vs_width/sb_comparison.py
import ROOT, os, re, json, math

ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

base = os.path.dirname(os.path.abspath(__file__))
ff = os.path.abspath(os.path.join(base, "..", ".."))

MH = 125.38
DM = 0.01
GRID = [115. + DM * i for i in range(int(20. / DM) + 1)]  # 115-135 GeV

# (label, workspace, lumi_scale for 172.26 fb-1, pdfindex json, category regex, ttH process test, fitted sigma(mu_ttH))
# Run 2 card is 137.16 fb-1 -> 172.26/137.16 = 1.256; its fitted value is the 13.6 TeV scan x sqrt(137.16/172.26)
GROUPS = [
    ("Run 2 STXS", "comparison_stxs/Run2/Datacard_Run2_ttHCats_kl_STXScomparison_Run2.root", 1.256,
     "Combine/pdfindex_Run2_ttHCats.json", r"ch1_RECO_TTH_[A-Za-z0-9_]+?", lambda p: p.startswith("ttH_"), (0.236, 0.219)),
    ("Run 3 STXS", "comparison_stxs/Run3/Sep26/Datacard_ttHCats_Only_kl_STXScomparison.root", 1.0,
     "Combine/pdfindex_ttHCats_Only.json", r"ch1_RECO_TTH_[A-Za-z0-9_]+?", lambda p: p.startswith("TTH_"), (0.319, 0.297)),
    ("Run 3 C1 binning", "comparison_stxs/muttH_vs_width/Datacard_C1reco_2224_sigscale_muttH_klambda.root", 1.0,
     "Combine/pdfindex_C1reco_2224_sigscale.json", r"(?:hadr|lept)_C1_[A-Z0-9_]+", lambda p: p.startswith("TTH__"), (0.336, 0.314)),
]

def is_had(cat):
    return re.search(r"(?i)had", cat) is not None  # hadr_C1_*, *_HAD_*, *_ttH_had*; lep / semilep / lept -> leptonic

def sigma_eff(xs, ys, frac=0.6827):
    tot = sum(ys); cdf, c = [], 0.
    for y in ys:
        c += y; cdf.append(c / tot)
    best, j = None, 0
    for i in range(len(xs)):
        while j < len(xs) and cdf[j] - (cdf[i - 1] if i else 0.) < frac:
            j += 1
        if j == len(xs): break
        if best is None or xs[j] - xs[i] < best: best = xs[j] - xs[i]
    return 0.5 * best

def analyse(label, ws_file, lumi_scale, pdfidx_json, catpat, is_tth):
    w = ROOT.TFile.Open(os.path.join(ff, ws_file)).Get("w")
    w.var("MH").setVal(MH)
    w.var("lumi_scale").setVal(lumi_scale)
    for p in ("mu_ttH", "mu_ttH_norm", "k_lambda"):
        if w.var(p): w.var(p).setVal(1.)
    for k, v in json.load(open(os.path.join(ff, pdfidx_json))).items():
        if w.cat(k): w.cat(k).setIndex(v)
    m = w.var("CMS_hgg_mass"); nset = ROOT.RooArgSet(m)

    def dist(pdf, norm):
        out = []
        for x in GRID:
            m.setVal(x); out.append(norm * pdf.getVal(nset) * DM)
        return out

    # Signal processes per category: ttH (S) and other Higgs (H, counted as background)
    cats = {}
    for o in w.allPdfs():
        mm = re.match(r"shapeSig_(.+)_(" + catpat + ")$", o.GetName())
        if not mm: continue
        proc, cat = mm.group(1), mm.group(2)
        n = w.function("n_exp_final_bin%s_proc_%s" % (cat, proc)).getVal()
        d = cats.setdefault(cat, {"S": [0.] * len(GRID), "H": [0.] * len(GRID)})
        key = "S" if is_tth(proc) else "H"
        d[key] = [a + b for a, b in zip(d[key], dist(o, n))]

    rows = []
    for cat, d in cats.items():
        # Continuum background: fitted multipdf x its expected yield (includes lumi_scale)
        nb = w.function("n_exp_final_bin%s_proc_bkg_mass" % cat)
        cont = dist(w.pdf("shapeBkg_bkg_mass_%s" % cat), nb.getVal())
        se = sigma_eff(GRID, d["S"])
        win = [MH - se <= x <= MH + se for x in GRID]
        S = sum(y for y, ok in zip(d["S"], win) if ok)
        C = sum(y for y, ok in zip(cont, win) if ok)
        H = sum(y for y, ok in zip(d["H"], win) if ok)
        rows.append({"cat": cat, "had": is_had(cat), "Stot": sum(d["S"]), "S": S, "C": C, "H": H, "B": C + H,
                     "seff": se, "dens": (C + H) / (2 * se), "F": S * S / (S + C + H)})
    rows.sort(key=lambda r: -r["F"])
    F = sum(r["F"] for r in rows)

    print("\n== %s (lumi_scale %.3f)" % (label, lumi_scale))
    print("   %-38s %6s %6s %7s %6s %7s %6s %6s %8s %7s" % ("category", "S_tot", "S_win", "B_cont", "B_H", "S/B", "S/rtB",
          "seff", "B/GeV", "info"))
    for r in rows:
        print("   %-38s %6.2f %6.2f %7.2f %6.2f %7.3f %6.2f %6.2f %8.2f %6.1f%%" % (
            r["cat"], r["Stot"], r["S"], r["C"], r["H"], r["S"] / r["B"], r["S"] / math.sqrt(r["B"]), r["seff"], r["dens"],
            100 * r["F"] / F))
    return rows

def info(rows, ks=1., sel=lambda r: True):
    return sum((ks * r["S"]) ** 2 / (ks * r["S"] + r["B"]) for r in rows if sel(r))

res = {g[0]: analyse(*g[:6]) for g in GROUPS}

# Summary
print("\n== Summary (172.26 fb-1, ttH xs at 13.6 TeV, window m_H +- sigma_eff per category)")
print("   %-18s %7s %7s %8s %7s %9s %8s %9s %12s" % ("", "S_tot", "S_win", "B_win", "S/B", "B/GeV", "info", "approx", "fitted"))
for label, *_, fitted in GROUPS:
    rows = res[label]
    St = sum(r["Stot"] for r in rows); Sw = sum(r["S"] for r in rows); Bw = sum(r["B"] for r in rows)
    F = info(rows)
    fit = "%.3f" % (0.5 * sum(fitted)) if fitted else "  -  "
    print("   %-18s %7.2f %7.2f %8.2f %7.3f %9.2f %8.2f %9.3f %12s" % (label, St, Sw, Bw, Sw / Bw, sum(r["dens"] for r in rows),
          F, F ** -0.5, fit))

print("\n   Split by channel (leptonic includes semileptonic):")
for label, *_ in GROUPS:
    rows = res[label]
    for ch, sel in (("hadronic", lambda r: r["had"]), ("leptonic", lambda r: not r["had"])):
        sub = [r for r in rows if sel(r)]
        print("   %-18s %-9s S_win %6.2f  B_win %7.2f  B/GeV %7.2f  info %5.2f (%4.1f%% of total)" % (
            label, ch, sum(r["S"] for r in sub), sum(r["B"] for r in sub), sum(r["dens"] for r in sub), info(sub),
            100 * info(sub) / info(rows)))

r2 = res["Run 2 STXS"]
S2 = sum(r["Stot"] for r in r2)
print("\n   Approx Run 3 / Run 2 sigma ratio, and with Run 2's total ttH yield (background unchanged):")
for label, *_ in GROUPS[1:]:
    rows = res[label]
    ks = S2 / sum(r["Stot"] for r in rows)
    print("   %-18s ratio %.3f  ->  x%.3f signal: ratio %.3f" % (label, (info(rows) / info(r2)) ** -0.5, ks,
          (info(rows, ks) / info(r2)) ** -0.5))
