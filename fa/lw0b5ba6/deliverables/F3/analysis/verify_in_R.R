# Independent re-computation in R of a sample of the statistics used in the proposal (log-rank, CMH, exact CI, Fisher, Welch, two-way ANOVA interaction, Tukey).
# Run from this folder after psln_blocks.py has written tidy_all_observations.csv:  Rscript verify_in_R.R
suppressMessages(library(survival))
d <- read.csv('tidy_all_observations.csv', stringsAsFactors=FALSE)
s <- d[d$kind=="survival",]; s$time <- suppressWarnings(as.numeric(s$time)); s <- s[!is.na(s$time),]
s$group <- trimws(s$group)
chk <- function(b, g1, g2) {
  x <- s[s$block==b & s$group %in% c(g1,g2),]
  sd <- survdiff(Surv(time, event) ~ group, data=x)
  cat(sprintf('%-12s %s vs %s: chisq=%.3f p=%.4g\n', b, g1, g2, sd$chisq, 1-pchisq(sd$chisq,1)))
}
chk('S06-A','PSLN-344','PSLN-212'); chk('S15-N','PSLN-344','PSLN-212'); chk('S03-J','PSLN-344','PSLN-212'); chk('S15-H','3d Vaccine+PSLN-344','3d PSLN-344'); chk('S06-G','PSLN-344','Untreated')
blocks <- c('S03-I','S03-J','S06-A','S06-B','S06-D','S06-E(r34)','S06-F(r34)','S06-G','S15-L','S15-N')
sall <- d[d$kind=='survival',]; sall$group <- trimws(sall$group)
arr <- array(0, dim=c(2,2,length(blocks)))
for (i in seq_along(blocks)) { for (j in 1:2) { g <- c('PSLN-344','PSLN-212')[j]; x <- sall[sall$block==blocks[i] & sall$group==g,]; arr[j,1,i] <- sum(x$event==0); arr[j,2,i] <- sum(x$event==1) } }
mh <- mantelhaen.test(arr, correct=TRUE); cat(sprintf('CMH chisq=%.2f p=%.3g; pooled %d/%d vs %d/%d\n', mh$statistic, mh$p.value, sum(arr[1,1,]), sum(arr[1,,]), sum(arr[2,1,]), sum(arr[2,,])))
b <- binom.test(61,73); cat(sprintf('CP CI 61/73: %.1f-%.1f\n', 100*b$conf.int[1], 100*b$conf.int[2]))
cat(sprintf('Fisher 14/21 vs 41/45: p=%.4f\n', fisher.test(matrix(c(41,4,14,7),2,byrow=TRUE))$p.value))
# Welch on log10 Ifnb1 S01-A 16h 344 vs 212
a <- log10(c(44.31,32.58,36.61,33.21,38.82)); bb <- log10(c(13.39,17.55,19.01,16.11,17.16)); tt <- t.test(a,bb)
cat(sprintf('Ifnb1 ratio %.3f CI %.3f-%.3f p=%.3g\n', 10^(mean(a)-mean(bb)), 10^tt$conf.int[1], 10^tt$conf.int[2], tt$p.value))
# two-way ANOVA interaction for Ifnb1 16h
y <- log10(c(13.39,17.55,19.01,16.11,17.16, 44.31,32.58,36.61,33.21,38.82, 36.54,35.02,34.51,42.93,38.98, 60.02,52.51,46.93,54.02,40.04))
age <- factor(rep(c('aged','aged','young','young'), each=5)); mn <- factor(rep(c('none','Mn','none','Mn'), each=5))
print(anova(lm(y ~ age*mn))[3,])
# Tukey for S03-C HAI log2
h <- data.frame(g=rep(c('Sham','CMP','P212','P344','Y'),each=5), v=log2(c(10,10,10,5,5, 40,10,20,20,40, 40,80,40,40,40, 320,640,160,320,640, 640,640,640,320,320)))
tk <- TukeyHSD(aov(v ~ g, data=h)); print(round(tk$g[c('P344-P212','Y-P344'),],5))
