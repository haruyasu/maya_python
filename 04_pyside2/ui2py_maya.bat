cd /d D:\ProgramFiles\Autodesk\Maya2017\bin
for %%f in (%*) do (
  mayapy pyside2-uic -o %~dpn1_pyside2.py %%f 
)