C     -*- fortran -*-
C     This file is autogenerated with f2py (version:2)
C     It contains Fortran 77 wrappers to fortran functions.

      subroutine f2pywrapvtst7 (vtst7f2pywrap, iyd, sec, glat, glo
     &ng, stl, f107a, f107, ap, ic)
      external vtst7
      integer iyd
      real sec
      real glat
      real glong
      real stl
      real f107a
      real f107
      integer ic
      real ap(7)
      real vtst7f2pywrap, vtst7
      vtst7f2pywrap = vtst7(iyd, sec, glat, glong, stl, f107a, f10
     &7, ap, ic)
      end


      subroutine f2pywrapscalh (scalhf2pywrap, alt, xm, temp)
      external scalh
      real alt
      real xm
      real temp
      real scalhf2pywrap, scalh
      scalhf2pywrap = scalh(alt, xm, temp)
      end


      subroutine f2pywrapglobe7 (globe7f2pywrap, yrd, sec, lat, lo
     &ng_bn, tloc, f107a, f107, ap, p)
      external globe7
      real yrd
      real sec
      real lat
      real long_bn
      real tloc
      real f107a
      real f107
      real ap(1)
      real p(1)
      real globe7f2pywrap, globe7
      globe7f2pywrap = globe7(yrd, sec, lat, long_bn, tloc, f107a,
     & f107, ap, p)
      end


      subroutine f2pywrapglob7s (glob7sf2pywrap, p)
      external glob7s
      real p(1)
      real glob7sf2pywrap, glob7s
      glob7sf2pywrap = glob7s(p)
      end


      subroutine f2pywrapdensu (densuf2pywrap, alt, dlb, tinf, tlb
     &, xm, alpha, tz, zlb, s2, mn1, zn1, tn1, tgn1)
      external densu
      real alt
      real dlb
      real tinf
      real tlb
      real xm
      real alpha
      real tz
      real zlb
      real s2
      integer mn1
      real zn1(mn1)
      real tn1(mn1)
      real tgn1(2)
      real densuf2pywrap, densu
      densuf2pywrap = densu(alt, dlb, tinf, tlb, xm, alpha, tz, zl
     &b, s2, mn1, zn1, tn1, tgn1)
      end


      subroutine f2pywrapdensm (densmf2pywrap, alt, d0, xm, tz, mn
     &3, zn3, tn3, tgn3, mn2, zn2, tn2, tgn2)
      external densm
      real alt
      real d0
      real xm
      real tz
      integer mn3
      integer mn2
      real zn3(mn3)
      real tn3(mn3)
      real tgn3(2)
      real zn2(mn2)
      real tn2(mn2)
      real tgn2(2)
      real densmf2pywrap, densm
      densmf2pywrap = densm(alt, d0, xm, tz, mn3, zn3, tn3, tgn3, 
     &mn2, zn2, tn2, tgn2)
      end


      subroutine f2pywrapdnet (dnetf2pywrap, dd, dm, zhm, xmm, xm)
      external dnet
      real dd
      real dm
      real zhm
      real xmm
      real xm
      real dnetf2pywrap, dnet
      dnetf2pywrap = dnet(dd, dm, zhm, xmm, xm)
      end


      subroutine f2pywrapccor (ccorf2pywrap, alt, r, h1, zh)
      external ccor
      real alt
      real r
      real h1
      real zh
      real ccorf2pywrap, ccor
      ccorf2pywrap = ccor(alt, r, h1, zh)
      end


      subroutine f2pywrapccor2 (ccor2f2pywrap, alt, r, h1, zh, h2)
      external ccor2
      real alt
      real r
      real h1
      real zh
      real h2
      real ccor2f2pywrap, ccor2
      ccor2f2pywrap = ccor2(alt, r, h1, zh, h2)
      end


      subroutine f2pyinitmeso7(setupfunc)
      external setupfunc
      real tn1(5)
      real tn2(4)
      real tn3(5)
      real tgn1(2)
      real tgn2(2)
      real tgn3(2)
      common /meso7/ tn1,tn2,tn3,tgn1,tgn2,tgn3
      call setupfunc(tn1,tn2,tn3,tgn1,tgn2,tgn3)
      end

      subroutine f2pyinitlower7(setupfunc)
      external setupfunc
      real ptm(10)
      real pdm(10,8)
      common /lower7/ ptm,pdm
      call setupfunc(ptm,pdm)
      end

      subroutine f2pyinitdatim7(setupfunc)
      external setupfunc
      integer isd(3)
      integer ist(2)
      integer nam(2)
      common /datim7/ isd,ist,nam
      call setupfunc(isd,ist,nam)
      end

      subroutine f2pyinitdmix(setupfunc)
      external setupfunc
      real dm04
      real dm16
      real dm28
      real dm32
      real dm40
      real dm01
      real dm14
      common /dmix/ dm04,dm16,dm28,dm32,dm40,dm01,dm14
      call setupfunc(dm04,dm16,dm28,dm32,dm40,dm01,dm14)
      end

      subroutine f2pyinitgts3c(setupfunc)
      external setupfunc
      real tlb
      real s
      real db04
      real db16
      real db28
      real db32
      real db40
      real db48
      real db01
      real za
      real t0
      real z0
      real g0
      real rl
      real dd
      real db14
      real tr12
      common /gts3c/ tlb,s,db04,db16,db28,db32,db40,db48,db01,za,t
     &0,z0,g0,rl,dd,db14,tr12
      call setupfunc(tlb,s,db04,db16,db28,db32,db40,db48,db01,za,t
     &0,z0,g0,rl,dd,db14,tr12)
      end

      subroutine f2pyinitmavg7(setupfunc)
      external setupfunc
      real pavgm(10)
      common /mavg7/ pavgm
      call setupfunc(pavgm)
      end

      subroutine f2pyinitdatime(setupfunc)
      external setupfunc
      integer isdate(3)
      integer istime(2)
      integer name(2)
      common /datime/ isdate,istime,name
      call setupfunc(isdate,istime,name)
      end

      subroutine f2pyinitparm7(setupfunc)
      external setupfunc
      real pt(150)
      real pd(150,9)
      real ps(150)
      real pdl(25,2)
      real ptl(100,4)
      real pma(100,10)
      real sam(100)
      common /parm7/ pt,pd,ps,pdl,ptl,pma,sam
      call setupfunc(pt,pd,ps,pdl,ptl,pma,sam)
      end

      subroutine f2pyinitmetsel(setupfunc)
      external setupfunc
      integer imr
      common /metsel/ imr
      call setupfunc(imr)
      end

      subroutine f2pyinitcsw(setupfunc)
      external setupfunc
      real sw(25)
      integer isw
      real swc(25)
      common /csw/ sw,isw,swc
      call setupfunc(sw,isw,swc)
      end

      subroutine f2pyinitparmb(setupfunc)
      external setupfunc
      real gsurf
      real re
      common /parmb/ gsurf,re
      call setupfunc(gsurf,re)
      end

      subroutine f2pyinitttest(setupfunc)
      external setupfunc
      real tinfg
      real gb
      real rout
      real tt(15)
      common /ttest/ tinfg,gb,rout,tt
      call setupfunc(tinfg,gb,rout,tt)
      end

      subroutine f2pyinitlpoly(setupfunc)
      external setupfunc
      real plg(9,4)
      real ctloc
      real stloc
      real c2tloc
      real s2tloc
      real c3tloc
      real s3tloc
      integer iyr
      real day
      real df
      real dfa
      real apd
      real apdf
      real apt(4)
      real xlong
      common /lpoly/ plg,ctloc,stloc,c2tloc,s2tloc,c3tloc,s3tloc,i
     &yr,day,df,dfa,apd,apdf,apt,xlong
      call setupfunc(plg,ctloc,stloc,c2tloc,s2tloc,c3tloc,s3tloc,i
     &yr,day,df,dfa,apd,apdf,apt,xlong)
      end

      subroutine f2pyinitlsqv(setupfunc)
      external setupfunc
      integer mp
      integer ii
      integer jg
      integer lt
      real qpb(50)
      integer ierr
      integer ifun
      integer n
      integer j
      real dv(60)
      common /lsqv/ mp,ii,jg,lt,qpb,ierr,ifun,n,j,dv
      call setupfunc(mp,ii,jg,lt,qpb,ierr,ifun,n,j,dv)
      end

      subroutine f2pyinitfit(setupfunc)
      external setupfunc
      real taf
      common /fit/ taf
      call setupfunc(taf)
      end


