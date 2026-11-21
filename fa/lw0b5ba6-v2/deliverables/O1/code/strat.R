suppressMessages(library(survival))
T <- read.csv('/tmp/work/tidy/tte.csv', stringsAsFactors=FALSE)
T$time[T$block=='S03-J' & is.na(T$time)] <- 21
keep <- list(c('S03-I','PSLN-344','PSLN-212'),c('S03-J','PSLN-344','PSLN-212'),c('S06-A','PSLN-344','PSLN-212'),
 c('S06-B','PSLN-344','PSLN-212'),c('S06-C','PSLN-344','PSLN-212'),c('S06-E','PSLN-344','PSLN-212'),c('S06-F','PSLN-344','PSLN-212'),
 c('S06-G','PSLN-344','PSLN-212'),c('S06-E[imprint]','Naive+PSLN-344','Naive+PSLN-212'),c('S06-E[imprint]','Imprinting+PSLN-344','Imprinting+PSLN-212'),
 c('S06-F[imprint]','Naive+PSLN-344','Naive+PSLN-212'),c('S06-F[imprint]','Imprinting+PSLN-344','Imprinting+PSLN-212'),
 c('S15-L','PSLN-344','PSLN-212'),c('S15-N','PSLN-344','PSLN-212'))
D <- do.call(rbind, lapply(keep, function(k){ d <- T[T$block==k[1] & T$group %in% k[2:3],]; d$arm <- ifelse(d$group==k[2],'344','212'); d$stratum <- paste(k[1],k[2]); d}))
print(survdiff(Surv(time,event) ~ arm + strata(stratum), data=D))
fit <- coxph(Surv(time,event) ~ I(arm=='344') + strata(stratum), data=D)
print(summary(fit)$conf.int)
