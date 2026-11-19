# a06c_cox.R -- (1) independent check of the Python log-rank code against survival::survdiff
#                (2) stratified Cox model for the pooled hazard ratio  -> tables/T7b_stratified_cox.csv
# Run from the analysis folder:  Rscript a06c_cox.R
suppressMessages(library(survival))
d <- read.csv('tables/surv_long.csv', stringsAsFactors = FALSE)
aged <- c('S03-I','S03-J','S06-A','S06-B','S06-C','S06-D','S06-E (rows 34-68)','S06-F (rows 34-68)','S06-G','S15-L','S15-N')
clean8 <- setdiff(aged, c('S06-D','S03-I','S03-J'))
out <- data.frame()
for (nm in c('all11','clean8')) {
  bl <- if (nm == 'all11') aged else clean8
  for (cmp in c('PSLN-212','Sham','PSLN-212(Y)')) {
    x <- d[d$block %in% bl & d$group %in% c('PSLN-344', cmp), ]
    x$trt <- as.integer(x$group == 'PSLN-344')
    cx <- tryCatch(coxph(Surv(day, event) ~ trt + strata(block), data = x), warning = function(w) NULL, error = function(e) NULL)
    sd <- survdiff(Surv(day, event) ~ trt + strata(block), data = x)
    if (!is.null(cx)) { ci <- summary(cx)$conf.int; hr <- ci[1]; lo <- ci[3]; hi <- ci[4] } else { hr <- NA; lo <- NA; hi <- NA }
    out <- rbind(out, data.frame(set = nm, contrast = paste('PSLN-344 vs', cmp), n_expts = length(unique(x$block)), HR_death = hr, lo = lo, hi = hi,
                                 strat_logrank_chisq = sd$chisq, p = 1 - pchisq(sd$chisq, 1)))
  }
}
write.csv(out, 'tables/T7b_stratified_cox.csv', row.names = FALSE)
# cross-check of single-experiment log-rank statistics (compare with T6, column logrank_chi2)
chk <- data.frame()
for (blk in aged) for (cmp in c('PSLN-212', 'Sham')) {
  x <- d[d$block == blk & d$group %in% c('PSLN-344', cmp), ]
  if (length(unique(x$group)) == 2) {
    sd <- survdiff(Surv(day, event) ~ group, data = x)
    chk <- rbind(chk, data.frame(block = blk, contrast = paste('PSLN-344 vs', cmp), R_chisq = sd$chisq))
  }
}
py <- read.csv('tables/T6_survival_contrasts.csv', stringsAsFactors = FALSE)
m <- merge(chk, py[, c('block', 'contrast', 'logrank_chi2')], by = c('block', 'contrast'))
m$abs_diff <- abs(m$R_chisq - m$logrank_chi2)
write.csv(m, 'tables/T6b_logrank_R_check.csv', row.names = FALSE)
cat(sprintf('log-rank cross-check: %d contrasts, max |R - Python| = %.2e\n', nrow(m), max(m$abs_diff)))
print(out)
