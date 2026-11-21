# Cross-check of the Python log-rank implementation and stratified Cox models (R survival)
suppressMessages(library(survival))
d <- read.csv('tte_all.csv', stringsAsFactors=FALSE)
chk <- function(b, g1, g2){ x <- d[d$block==b & d$group %in% c(g1,g2),]; s <- survdiff(Surv(day,event)~group, data=x); data.frame(block=b, g1=g1, g2=g2, chisq=s$chisq, p=1-pchisq(s$chisq,1)) }
blocksA <- c('S03-I','S03-J','S06-A','S06-B','S06-C','S06-D','S06-E','S06-F','S06-G')
res <- do.call(rbind, lapply(c(blocksA,'S15-L','S15-N'), function(b) chk(b,'PSLN-344','PSLN-212')))
write.csv(res, 'r_logrank_check.csv', row.names=FALSE)
A <- d[d$block %in% blocksA & d$group %in% c('PSLN-344','PSLN-212'),]; A$g <- as.numeric(A$group=='PSLN-344')
B <- A[!(A$block %in% c('S03-I','S03-J','S06-C')),]
out <- list()
for (nm in c('A','B')) {
  X <- if (nm=='A') A else B
  s <- survdiff(Surv(day,event)~group+strata(block), data=X)
  cx <- summary(coxph(Surv(day,event)~g+strata(block), data=X))$conf.int
  out[[nm]] <- data.frame(set=nm, strat_logrank_chisq=s$chisq, p=1-pchisq(s$chisq,1), hr=cx[1,1], hr_lo=cx[1,3], hr_hi=cx[1,4])
}
o <- do.call(rbind, out); write.csv(o, 'cox_hr.csv', row.names=FALSE); print(o)
