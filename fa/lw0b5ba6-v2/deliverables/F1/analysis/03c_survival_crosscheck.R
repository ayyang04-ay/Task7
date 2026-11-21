# Cross-check of the Python log-rank results with R survival::survdiff (independent implementation)
suppressMessages(library(survival))
t <- read.csv('../data_tidy/psln_tidy_all_blocks.csv', check.names = FALSE)
s <- t[t$kind == 'surv', ]
chk <- function(b, g1, g0) {
  d <- s[s$block == b & s$group %in% c(g1, g0), ]
  d$time[is.na(d$time)] <- max(d$time, na.rm = TRUE)
  f <- survdiff(Surv(time, event) ~ group, data = d)
  p <- 1 - pchisq(f$chisq, 1)
  cat(sprintf('%-11s %-22s vs %-22s chisq = %7.4f  p = %.5f\n', b, g1, g0, f$chisq, p))
}
chk('S03-I', 'PSLN-344', 'PSLN-212'); chk('S03-J', 'PSLN-344', 'PSLN-212'); chk('S06-A', 'PSLN-344', 'PSLN-212')
chk('S06-B', 'PSLN-344', 'PSLN-212'); chk('S06-C', 'PSLN-344', 'PSLN-212'); chk('S06-E', 'PSLN-344', 'PSLN-212')
chk('S06-F', 'PSLN-344', 'PSLN-212'); chk('S06-G', 'PSLN-344', 'PSLN-212'); chk('S06-G', 'PSLN-344', 'Untreated')
chk('S15-H', '3d Vaccine+PSLN-344', '3d PSLN-344'); chk('S15-H', '3d PSLN-344', '3d Vaccine'); chk('S15-N', 'PSLN-344', 'PSLN-212')
# stratified log-rank, aged BALB/c, PSLN-344 vs PSLN-212
for (set in list(c('S03-I','S03-J','S06-A','S06-B','S06-C','S06-D'), c('S06-A','S06-B','S06-C'), c('S06-E','S06-F','S06-G'))) {
  d <- s[s$block %in% set & s$group %in% c('PSLN-344', 'PSLN-212'), ]
  for (b in unique(d$block)) d$time[d$block == b & is.na(d$time)] <- max(d$time[d$block == b], na.rm = TRUE)
  f <- survdiff(Surv(time, event) ~ group + strata(block), data = d)
  cat(sprintf('stratified %s: chisq = %.4f p = %.3g\n', paste(set, collapse = '+'), f$chisq, 1 - pchisq(f$chisq, 1)))
}
