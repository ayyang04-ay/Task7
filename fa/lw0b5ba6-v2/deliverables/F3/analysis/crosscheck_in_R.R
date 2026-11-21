# crosscheck_in_R.R - independent re-computation of three headline statistics in R (survival package, base stats).
# Input: /tmp/work/surv_long.csv written by the Python snippet in run_all.sh (one row per animal, 11 aged challenge blocks).
suppressMessages(library(survival))
d <- read.csv("/tmp/work/surv_long.csv")
d2 <- subset(d, group %in% c("PSLN-344", "PSLN-212")); d2$g <- as.integer(d2$group == "PSLN-344")
s <- survdiff(Surv(day, event) ~ g + strata(block), data = d2)
cat(sprintf("Stratified log-rank PSLN-344 vs PSLN-212: chi-square %.2f on 1 df (Z = %.2f)\n", s$chisq, sqrt(s$chisq)))
tab <- with(d2, table(g, event))
cat(sprintf("Pooled survivors: PSLN-344 %d/%d, PSLN-212 %d/%d; Fisher exact p = %.2e\n", tab["1", "0"], sum(tab["1", ]), tab["0", "0"], sum(tab["0", ]), fisher.test(tab)$p.value))
arr <- xtabs(~ g + event + block, data = transform(d2, event = factor(event)))
mh <- mantelhaen.test(arr, exact = TRUE)
cat(sprintf("Exact stratified (conditional) test: p = %.1e; common odds ratio of death %.3f (95%% CI %.3f-%.3f)\n", mh$p.value, mh$estimate, mh$conf.int[1], mh$conf.int[2]))
# HAI, H1N1 (S03-C): PSLN-344 vs PSLN-212 on the log scale
a <- log(c(320, 640, 160, 320, 640)); b <- log(c(40, 80, 40, 40, 40)); tt <- t.test(a, b)
cat(sprintf("HAI H1N1 GMT ratio PSLN-344/PSLN-212: %.2f (95%% CI %.2f-%.2f), Welch p = %.2g\n", exp(diff(rev(tt$estimate))), exp(tt$conf.int[1]), exp(tt$conf.int[2]), tt$p.value))
