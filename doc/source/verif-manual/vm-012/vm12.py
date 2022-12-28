"""VM12 COMBINED BENDING AND TORSION"""

"""
Problem Description:
    -
Reference:
    - C***      USING PIPE16     STR. OF MATL., TIMOSHENKO,
    PART 1, 3RD ED., PAGE 299, PROB. 2
"""

from ansys.mapdl.core import launch_mapdl

# start mapdl and clear it
mapdl = launch_mapdl(loglevel="WARNING", print_com=True)
mapdl.clear()  # optional as MAPDL just started

# enter verification example mode and the pre-processing routine
mapdl.verify("vm12")
mapdl.prep7()

mapdl.antype("STATIC")
mapdl.et(1, "PIPE16")
mapdl.r(1, 4.67017, 2.33508)  # REAL CONSTANTS FOR SOLID CROSS SECTION
mapdl.mp("EX", 1, 30e6)
mapdl.mp("NUXY", 1, 0.3)
mapdl.n(1)
mapdl.n(2, "", "", 300)
mapdl.e(1, 2)
mapdl.d(1, "ALL")
mapdl.f(2, "MZ", 9000)
mapdl.f(2, "FX", -250)
mapdl.finish()
mapdl.slashsolu()
mapdl.outpr("BASIC", 1)
with mapdl.non_interactive:
    mapdl.run("/OUT,SCRATCH")
    mapdl.solve()
    mapdl.finish()
    mapdl.post1()
    mapdl.etable("P_STRS", "NMISC", 86)
    mapdl.etable("SHR", "NMISC", 88)
    mapdl.run("/OUT")
    mapdl.run("/GOPR")
mapdl.last_response
mapdl.get("P_STRESS", "ELEM", 1, "ETAB", "P_STRS")
mapdl.get("SHEAR", "ELEM", 1, "ETAB", "SHR")
mapdl.dim("LABEL", "CHAR", 2, 2)
mapdl.dim("VALUE", "", 2, 3)
mapdl.run("LABEL(1,1) = 'MAX PRIN','MAX SH S'")
mapdl.run("LABEL(1,2) = 'STRS psi','TRS psi '")
mapdl.vfill("VALUE(1", "1)", "DATA", 7527, 3777)
mapdl.vfill("VALUE(1", "2)", "DATA", "P_STRESS", "(SHEAR/2)")
mapdl.vfill("VALUE(1", "3)", "DATA", "ABS(P_STRESS/7527 )", "ABS((SHEAR/2)/3777 )")
mapdl.save("TABLE_1")
mapdl.run("FINI")
mapdl.run("/CLEAR,NOSTART")

mapdl.prep7()
mapdl.run("C***     USING PIPE288")
mapdl.run("ANTYPE,STATIC")
mapdl.et(1, "PIPE288", "", "", "", 2)
mapdl.sectype(1, "PIPE")
mapdl.secdata(4.67017, 2.33508)
mapdl.keyopt(1, 3, 3)  # CUBIC SHAPE FUNCTION
mapdl.mp("EX", 1, 30e6)
mapdl.mp("NUXY", 1, 0.3)
mapdl.n(1)
mapdl.n(2, "", "", 300)
mapdl.e(1, 2)
mapdl.d(1, "ALL")
mapdl.f(2, "MZ", 9000)
mapdl.f(2, "FX", -250)
mapdl.finish()

mapdl.slashsolu()
mapdl.outpr("BASIC", 1)
with mapdl.non_interactive:
    mapdl.run("/OUT,SCRATCH")
    mapdl.solve()
    mapdl.finish()
    mapdl.post1()
    mapdl.set("LAST")
    mapdl.graphics("POWER")
    mapdl.eshape(1)
    mapdl.view(1, 1, 1, 1)
    mapdl.plesol("S", 1)
    mapdl.run("/OUT")
    mapdl.run("/GOPR")
mapdl.get("P_STRESS", "PLNSOL", 0, "MAX")
mapdl.plesol("S", "INT")
mapdl.get("SHEAR", "PLNSOL", 0, "MAX")
mapdl.dim("LABEL", "CHAR", 2, 2)
mapdl.dim("VALUE", "", 2, 3)
mapdl.run("LABEL(1,1) = 'MAX PRIN','MAX SH S'")
mapdl.run("LABEL(1,2) = 'STRS psi','TRS psi '")
mapdl.vfill("VALUE(1", "1)", "DATA", 7527, 3777)
mapdl.vfill("VALUE(1", "2)", "DATA", "P_STRESS", "(SHEAR/2)")
mapdl.vfill("VALUE(1", "3)", "DATA", "ABS(P_STRESS/7527 )", "ABS((SHEAR/2)/3777 )")
mapdl.save("TABLE_2")
mapdl.run("FINI")
mapdl.run("/CLEAR,NOSTART")
mapdl._run("/NOPR")  # It is not recommended to use '/NOPR' in a normal PyMAPDL session.
mapdl.com("")

with mapdl.non_interactive:
    mapdl.run("/OUT,vm12,vrt")
    mapdl.com("------------------- VM12 RESULTS COMPARISON ---------------------")
    mapdl.com("")
    mapdl.com("|   TARGET   |   Mechanical APDL   |   RATIO")
    mapdl.com("")
    mapdl.resume("TABLE_1")
    mapdl.com("USING PIPE16")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
    mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F12.0,'   ',1F15.3)")
    mapdl.com("")
    mapdl.resume("TABLE_2")
    mapdl.com("USING PIPE288")
    mapdl.com("")
    mapdl.run("*VWRITE,LABEL(1,1),LABEL(1,2),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
    mapdl.run("(1X,A8,A8,'   ',F10.0,'  ',F12.0,'   ',1F15.3)")
    mapdl.com("")
    mapdl.com("-----------------------------------------------------------------")
    mapdl.run("/OUT")
    mapdl.run("/GOPR")

mapdl.finish()
mapdl.starlist("vm12", "vrt")

mapdl.exit()
