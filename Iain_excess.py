#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:02:39 2023

@author: Iain McD
"""


  lastR=0; for (i=46;i<=78;i++) if ($i>0) {R+=$i;N++;Q+=$i>1?$i:1/$i;Rmax=$i>Rmax?$i:Rmax;Rmin=$i<Rmin?$i:Rmin;if (lastR>0) P+=$i>lastR?$i-lastR:lastR-$i;lastR=$i}; \
      lastR=0; for (i=46;i<=55;i++) if ($i>0) {Ropt+=$i;Nopt++;Qopt+=$i>1?$i:1/$i;Rmaxopt=$i>Rmaxopt?$i:Rmaxopt;Rminopt=$i<Rminopt?$i:Rminopt;if (lastR>0) Popt+=$i>lastR?$i-lastR:lastR-$i;lastR=$i}; \
      lastR=0; for (i=56;i<=64;i++) if ($i>0) {Rnir+=$i;Nnir++;Qnir+=$i>1?$i:1/$i;Rmaxnir=$i>Rmaxnir?$i:Rmaxnir;Rminnir=$i<Rminnir?$i:Rminnir;if (lastR>0) Pnir+=$i>lastR?$i-lastR:lastR-$i;lastR=$i}; \
      lastR=0; for (i=65;i<=78;i++) if ($i>0) {Rmir+=$i;Nmir++;Qmir+=$i>1?$i:1/$i;Rmaxmir=$i>Rmaxmir?$i:Rmaxmir;Rminmir=$i<Rminmir?$i:Rminmir;if (lastR>0) Pmir+=$i>lastR?$i-lastR:lastR-$i;lastR=$i}; \
      Rpmir=Nmir>1?(Rmir-Rmaxmir)/(Nmir-1):0; \
      Roptnir=Nopt>0||Nnir>0?(Ropt+Rnir)/(Nopt+Nnir):0; \
      R=N>0?R/N:0; Ropt=Nopt>0?Ropt/Nopt:0; Rnir=Nnir>0?Rnir/Nnir:0; Rmir=Nmir>0?Rmir/Nmir:0; \
      Q=N>0?Q/N-1:0; Qopt=Nopt>0?Qopt/Nopt-1:0; Qnir=Nnir>0?Qnir/Nnir-1:0; Qmir=Nmir>0?Qmir/Nmir-1:0; \
      P=N>0&&Rmax!=Rmin?P/N/(Rmax-Rmin):0; Popt=Nopt>0&&Rmaxopt!=Rminopt?Popt/Nopt/(Rmaxopt-Rminopt):0; Pnir=Nnir>0&&Rmaxnir!=Rminnir?Pnir/Nnir/(Rmaxnir-Rminnir):0; Pmir=Nmir>0&&Rmaxmir!=Rminmir?Pmir/Nmir/(Rmaxmir-Rminmir):0; \
      Pp=N>0&&Q>0?P/N/Q:0; Ppopt=Nopt>0&&Qopt>0?Popt/Nopt/Qopt:0; Ppnir=Nnir>0&&Qnir>0?Pnir/Nnir/Qnir:0; Ppmir=Nmir>0&&Qmir>0?Pmir/Nmir/Qmir:0; \
      Xmir=Roptnir>0?Rmir/Roptnir:0; Xpmir=Rnir>0?Rmir/Rnir:0; Smir=Qnir>0?Rmir*Nmir/Qnir:0; Bmir=Rmir!=1?(Rpmir-1)/(Rmir-1):0; \
      print $0,N,Nopt,Nnir,Nmir,R,Ropt,Rnir,Rmir,Q,Qopt,Qnir,Qmir,P,Popt,Pnir,Pmir,Pp,Ppopt,Ppnir,Ppmir,Xmir,Xpmir,Smir,Rpmir,Rmax,Rmaxopt,Rmaxnir,Rmaxmir,Bmir \
     } > hip_merge_xs_stats.dat

awk $4>0 {N=Nopt=Nnir=Nmir=R=Roptnir=Ropt=Rnir=Rmir=Q=Qopt=Qnir=Qmir=P=Popt=Pnir=Pmir=Pp=Ppopt=Ppnir=Ppmir=Xmir=Xpmir=Smir=Rpmir=Rmax=Rmaxopt=Rmaxnir=Rmaxmir=Bmir=0; \
      Rmin=Rminopt=Rminnir=Rminmir=999; \
      lastR=0; for (i=38;i<=61;i++) if ($i>0) {R+=$i;N++;Q+=$i>1?$i:1/$i;Rmax=$i>Rmax?$i:Rmax;Rmin=$i<Rmin?$i:Rmin;if (lastR>0) P+=$i>lastR?$i-lastR:lastR-$i;lastR=$i}; \
      lastR=0; for (i=38;i<=46;i++) if ($i>0) {Ropt+=$i;Nopt++;Qopt+=$i>1?$i:1/$i;Rmaxopt=$i>Rmaxopt?$i:Rmaxopt;Rminopt=$i<Rminopt?$i:Rminopt;if (lastR>0) Popt+=$i>lastR?$i-lastR:lastR-$i;lastR=$i}; \
      lastR=0; for (i=47;i<=54;i++) if ($i>0) {Rnir+=$i;Nnir++;Qnir+=$i>1?$i:1/$i;Rmaxnir=$i>Rmaxnir?$i:Rmaxnir;Rminnir=$i<Rminnir?$i:Rminnir;if (lastR>0) Pnir+=$i>lastR?$i-lastR:lastR-$i;lastR=$i}; \
      lastR=0; for (i=55;i<=61;i++) if ($i>0) {Rmir+=$i;Nmir++;Qmir+=$i>1?$i:1/$i;Rmaxmir=$i>Rmaxmir?$i:Rmaxmir;Rminmir=$i<Rminmir?$i:Rminmir;if (lastR>0) Pmir+=$i>lastR?$i-lastR:lastR-$i;lastR=$i}; \
      Rpmir=Nmir>1?(Rmir-Rmaxmir)/(Nmir-1):0; \
      Roptnir=Nopt>0||Nnir>0?(Ropt+Rnir)/(Nopt+Nnir):0; \
      R=N>0?R/N:0; Ropt=Nopt>0?Ropt/Nopt:0; Rnir=Nnir>0?Rnir/Nnir:0; Rmir=Nmir>0?Rmir/Nmir:0; \
      Q=N>0?Q/N-1:0; Qopt=Nopt>0?Qopt/Nopt-1:0; Qnir=Nnir>0?Qnir/Nnir-1:0; Qmir=Nmir>0?Qmir/Nmir-1:0; \
      P=N>0&&Rmax!=Rmin?P/N/(Rmax-Rmin):0; Popt=Nopt>0&&Rmaxopt!=Rminopt?Popt/Nopt/(Rmaxopt-Rminopt):0; Pnir=Nnir>0&&Rmaxnir!=Rminnir?Pnir/Nnir/(Rmaxnir-Rminnir):0; Pmir=Nmir>0&&Rmaxmir!=Rminmir?Pmir/Nmir/(Rmaxmir-Rminmir):0; \
      Pp=N>0&&Q>0?P/N/Q:0; Ppopt=Nopt>0&&Qopt>0?Popt/Nopt/Qopt:0; Ppnir=Nnir>0&&Qnir>0?Pnir/Nnir/Qnir:0; Ppmir=Nmir>0&&Qmir>0?Pmir/Nmir/Qmir:0; \
      Xmir=Roptnir>0?Rmir/Roptnir:0; Xpmir=Rnir>0?Rmir/Rnir:0; Smir=Qnir>0?Rmir*Nmir/Qnir:0; Bmir=Rmir!=1?(Rpmir-1)/(Rmir-1):0; \
      print $0,N,Nopt,Nnir,Nmir,R,Ropt,Rnir,Rmir,Q,Qopt,Qnir,Qmir,P,Popt,Pnir,Pmir,Pp,Ppopt,Ppnir,Ppmir,Xmir,Xpmir,Smir,Rpmir,Rmax,Rmaxopt,Rmaxnir,Rmaxmir,Bmir \
     } xsebverr-run12.dat > xsebverrstats-run12.dat

#N Nopt Nnir Nmir R Ropt Rnir Rmir Q Qopt Qnir Qmir P Popt Pnir Pmir Pp Ppopt Ppnir Ppmir Xmir Xpmir Smir Rpmir Rmax Rmaxopt Rmaxnir Rmaxmir Bmir
#87 88  89   90   91 92  93   94   95  96  97   98  99 100 101  102  103 104  105   106   107  108   109   110  111  112     113     114     115
#71 72  73   74   75 76  77   78   79  80  81   82  83  84  85   86   87  88   89    90    91   92    93    94   95   96      97      98      99
#N Nopt Nnir Nmir R Ropt Rnir Rmir Q Qopt Qnir Qmir P Popt Pnir Pmir Pp Ppopt Ppnir Ppmir Xmir Xpmir Smir Rpmir Rmax Rmaxopt Rmaxnir Rmaxmir Bmir

# sdu U  BT B sdg VH VT V sdr R sdi Ig sdz viy J  H  K  W1 1  mb1 mb2 2 W2 ma s9 W3 i12 mc md l18 me W4 i25
# 13  14 15 16 17 18 19 20 21 22 23 24 25  26  27 28 29 30 31 32  33 34 35 36 37 38 39  40 41 42  43 44 45
# 46  47 48 49 50 51 52 53 54 55 56 57 58  59  60 61 62 63 64 65  66 67 68 69 70 71 72  73 74 75  76 77 78

# 354.3 365 420 440.7 477 526.5 532 553.7 623.1 700 762.5 786 913.4 1021 1250 1650 2200 3353 3600 4290 4350 4500 4603 8280 8610 11561 12000 12130 14650 18390 21300 22088 25000
# 150 218 354.3 420 440.7 477 532 553.7 623.1 762.5 786 913.4 1021 1250 1650 2200 3353 4603 8610 11561 12000 18390 22088 25000 

# g15 g23 sdu BT B sdg VT V sdr sdi Ig sdz viy J H K W1 W2 s9 W3 i12 l18 W4 i25
#  16 17  18  1920 21  2223 24  25  26  27  28 29303132 33 34 35  36  37 38 39
#  40 41  42  4344 45  4647 48  49  50  51  52 53545556 57 58 59  60  61 62 63

source uncertainties.scr

awk NR==1 {split(wave,w," ")} \
    $89>0 && $90>1 {Rnir=$93; 
                    if (Rnir+0==0) 
                    Rnir=1; d=$3*1000; n=1; lumdust=0; sumfdust=0; fdustmax=0; maxw=0; 
                    for (i=56;i<=64;i++) if ($i>0) {filt[1]=i; wl[1]=w[i-45]; f[1]=$(i-33); fstar[1]=$(i-33)}; lastnu=3e17/wl[1]; \
        for (i=65;i<=78;i++) if ($i+0>0) {n++; filt[n]=i; xs[n]=$i/Rnir-1; wl[n]=w[i-45]; fstar[n]=$(i-33)/$i; f[n]=$(i-33)}; \
        filter[n+1]=0; wl[n+1]=1e6; fstar[n+1]=(wl[n]/1e6)**2*fstar[n]; f[n+1]=(wl[n]/1e6)**2*f[n]; \
        for (i=1;i<=n;i++) {lognu1=log(3e17/wl[i]); lognu2=log(3e17/wl[i+1]); logfstar1=log(fstar[i]); logfstar2=log(fstar[i+1]); logf1=log(f[i]); logf2=log(f[i+1]); \
            for (j=wl[i];j<=wl[i+1];j*=1+step) {nu=3e17/j; dnu=lastnu-nu; lastnu=nu; logfstar=(logfstar1-logfstar2)*(log(nu)-lognu2)/(lognu1-lognu2)+logfstar2; logf=(logf1-logf2)*(log(nu)-lognu2)/(lognu1-lognu2)+logf2; \
                fdust=exp(logf)-exp(logfstar); sumfdust+=fdust*dnu; if (fdust>fdustmax) {fdustmax=fdust; maxw=j}}}; \
        lumdust=sumfdust/1e29*(d*3.086e16)**2/3.828e26; if (d<0) maxw=0; if (d<0 || lumdust<0) lumdust=0} \
    $89<=0 || $90<=1 {lumdust=0; maxw=0} \
    {print $0,lumdust,lumdust/$10,int(maxw/100+.5)/10} \
    step=0.001 wave="354.3 365 420 440.7 477 526.5 532 553.7 623.1 700 762.5 786 913.4 1021 1250 1650 2200 3353 3600 4290 4350 4500 4603 8280 8610 11561 12000 12130 14650 18390 21300 22088 25000" hip_merge_xs_stats_err.dat > hip_merge_xs_stats_err_int.dat

awk NR==1 {split(wave,w," ")} \
    $73>0 && $74>1 {Rnir=$77; d=$4*1000; n=1; lumdust=0; sumfdust=0; fdustmax=0; maxw=0; for (i=47;i<=54;i++) if ($i>0) {filt[1]=i; wl[1]=w[i-39]; f[1]=$(i-24); fstar[1]=$(i-24)}; lastnu=3e17/wl[1]; \
        for (i=55;i<=61;i++) if ($i>0) {n++; filt[n]=i; xs[n]=$i/Rnir-1; wl[n]=w[i-39]; fstar[n]=$(i-24)/$i; f[n]=$(i-24)}; \
        filter[n+1]=0; wl[n+1]=1e6; fstar[n+1]=(wl[n]/1e6)**2*fstar[n]; f[n+1]=(wl[n]/1e6)**2*f[n]; \
        for (i=1;i<=n;i++) {lognu1=log(3e17/wl[i]); lognu2=log(3e17/wl[i+1]); logfstar1=log(fstar[i]); logfstar2=log(fstar[i+1]); logf1=log(f[i]); logf2=log(f[i+1]); \
            for (j=wl[i];j<=wl[i+1];j*=1+step) {nu=3e17/j; dnu=lastnu-nu; lastnu=nu; logfstar=(logfstar1-logfstar2)*(log(nu)-lognu2)/(lognu1-lognu2)+logfstar2; logf=(logf1-logf2)*(log(nu)-lognu2)/(lognu1-lognu2)+logf2; \
                fdust=exp(logf)-exp(logfstar); sumfdust+=fdust*dnu; if (fdust>fdustmax) {fdustmax=fdust; maxw=j}}}; \
        lumdust=sumfdust/1e29*(d*3.086e16)**2/3.828e26; if (d<0) maxw=0; if (d<0 || lumdust<0) lumdust=0} \
    $73<=0 || $74<=1 {lumdust=0; maxw=0} \
    {print $0,lumdust,lumdust/$11,int(maxw/100+.5)/10} \
    step=0.001 wave="150 218 354.3 420 440.7 477 532 553.7 623.1 762.5 786 913.4 1021 1250 1650 2200 3353 4603 8610 11561 12000 18390 22088 25000" xsebverrstatserr-run12.dat > xsebverrstatserrint-run12.dat
