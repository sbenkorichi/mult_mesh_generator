#!/usr/bin/python

#Salah Benkorichi
# 26-09-2017

from __future__ import division

from decimal import *
from math import sqrt
import string
import math
import cgi, sys

# Variables to script path and that gather form fields
SCRIPT_NAME = '/cgi-bin/mult_mesh.py'
form = cgi.FieldStorage()

global resolution
resolution = ''


# Groups integers into comma separated thousands
def group(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))
# Writes out html page templates and form fields
def print_html_header():
    HTML_TEMPLATE_HEAD = """<!DOCTYPE html>
    <html><head><title>Mult Mesh generator</title>
    <meta http-equiv="Content-Type" Content-type: text/html\r\n\r\n">
    <style>
    .button {
      border-radius: 17px;
      background-color: #f4511e;
      border: none;
      color: #FFFFFF;
      text-align: center;
      font-size: 20px;
      padding: 7px;
      width: 280px;
      transition: all 0.5s;
      cursor: pointer;
      margin: 7px;
    }
    
    .button span {
      cursor: pointer;
      display: inline-block;
      position: relative;
      transition: 0.5s;
    }
    
    .button span:after {
      content: '\00bb';
      position: absolute;
      opacity: 0;
      top: 0;
      right: -20px;
      transition: 0.5s;
    }
    
    .button:hover span {
      padding-right: 25px;
    }
    
    .button:hover span:after {
      opacity: 1;
      right: 0;
    }
    </style> 
    </head><body>

    <div class="container">

    <h3><FONT FACE="Arial, Helvetica, Geneva"><font color="blue">Enter Mult Mesh generator input data</font></h3>
    <form class="well" action="%(SCRIPT_NAME)s" method="POST" enctype="multipart/form-data">"""
    print "Content-type: text/html\n"
    print HTML_TEMPLATE_HEAD % {'SCRIPT_NAME':SCRIPT_NAME}


def print_html_body():   
    

    MULT_MESH_INPUT= """
	
    <form>
	  <pre class="tab">IJK   = single mesh equivalent IJK, exp: 221,221,241 </pre> 
	  <pre class="tab">XB    = single mesh equivalent XB,  exp: -1.5,1.5,-1.5,-3,3 </pre> 
	  <pre class="tab">MBLKS = mesh block arrangment,      exp: 5,5,5 </pre> 
    <br/><br/>
     
    <label margin-bottom: 20px>IJK</label> &emsp; &emsp; &emsp; &emsp; &emsp; 
    <input class="input-mini" name="I" type="text" size="5"/> 
	<input class="input-mini" name="J" type="text" size="5"/> 
	<input class="input-mini" name="K" type="text" size="5"/> 
    <br/><br/>
    <label>XB </label> 
    <input class="input-mini" name="x1" type="text" size="5"/>  
	<input class="input-mini" name="x2" type="text" size="5"/>
	<input class="input-mini" name="y1" type="text" size="5"/>
	<input class="input-mini" name="y2" type="text" size="5"/>
	<input class="input-mini" name="z1" type="text" size="5"/>
	<input class="input-mini" name="z2" type="text" size="5"/>
    <br/><br/>
    <label>MBLKS </label> &emsp; &emsp; &emsp; &nbsp; 
    <input class="input-mini" name="MBLKS_i" type="text" size="5"/>
    <input class="input-mini" name="MBLKS_j" type="text" size="5"/>	
	<input class="input-mini" name="MBLKS_k" type="text" size="5"/>
	<br/><br/>


    &emsp; &emsp; &emsp; &emsp; <button class="button" type="submit" value"Submit">Generate Mesh</button>
    </form>
    <br/><br/>
    """

    print MULT_MESH_INPUT

def print_html_footer():
    HTML_TEMPLATE_FOOT = """</font>
    </form>

    </div>
    </body>
    </html>"""
    print HTML_TEMPLATE_FOOT

# Checks the form field for empty submission, otherwise sends the query to the execute_search() fucntion
def check_input_fields(I="", J="",K="",  x1="", x2="", y1="", y2="",z1="", z2="", MBLKS_i="", MBLKS_j="",  MBLKS_k=""):
     
    # Writes fields and values to lists for input looping
    global input_fields
    global input_values
    input_fields = ("I","J", "K", "x1", "x2","y1", "y2", "z1","z2","MBLKS_i", "MBLKS_j", "MBLKS_k",)
    input_values = (I,J, K, x1, x2,y1, y2, z1,z2,MBLKS_i, MBLKS_j, MBLKS_k)
  

    # Loops through input values to check for empty fields and returns an error if so
    count = 0
    for field in input_values:
        if field == "":
            print """<h2><font color="red">Please specify """ + input_fields[count] + """ value</font></h2><br/>"""
            fill_previous_values()
            print_html_footer()
            sys.exit()
        count += 1

    # Check to see if all inputs are valid numbers (by attempting to convert each one to a float)
    # If not, it will exit and fill the previous values
    count = 0
    # for field in input_values:
    try:
        for field in input_values:
            if field == "on":
                break          
            float(field)
            count += 1
    except:
        print """<h2><font color="red">""" + input_fields[count] + """ is not a valid number</font></h2><br/>"""
        fill_previous_values()
        sys.exit()
        count += 1 

    check_I=int(I)
    check_J=int(J)
    check_K=int(K)
    check_x1=float(x1)
    check_x2=float(x2)
    check_y1=float(y1)
    check_y2=float(y2)
    check_z1=float(z1)
    check_z2=float(z2)
    check_MBLKS_i=int(MBLKS_i)
    check_MBLKS_j=int(MBLKS_j)
    check_MBLKS_k=int(MBLKS_k)


    #### Add error checking for non-numbers


    if check_I  <= 0:
        print """<h3><font color="red">IJK: I value should be greater than 0 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()
    if check_J  <= 0:
        print """<h3><font color="red">IJK: J value should be greater than 0 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()
		
    if check_K <= 0:
        print """<h3><font color="red">IJK: K value should be greater than 0 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()		
		
    if check_x2 <= check_x1 :
        print """<h3><font color="red">XB: x2 should be greater than x1 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()  

    if check_y2 <= check_y1 :
        print """<h3><font color="red">XB: y2 should be greater than y1 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()  

    if check_z2 <= check_z1 :
        print """<h3><font color="red">XB: z2 should be greater than z1 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()  
		
    if check_MBLKS_i  <= 0:
        print """<h3><font color="red">MBLKS: I value should be greater than 0 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()
    if check_MBLKS_j  <= 0:
        print """<h3><font color="red">MBLKS: J value should be greater than 0 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()
		
    if check_MBLKS_k <= 0:
        print """<h3><font color="red">MBLKS: K value should be greater than 0 </font><h3/></b>"""
        fill_previous_values()
        print_html_footer()
        sys.exit()			
		 
	
    I=int(I)
    J=int(J)
    K=int(K)
    x1=float(x1)
    x2=float(x2)
    y1=float(y1)
    y2=float(y2)
    z1=float(z1)
    z2=float(z2)
    MBLKS_i=int(MBLKS_i)
    MBLKS_j=int(MBLKS_j)
    MBLKS_k=int(MBLKS_k)
    M0_i=MBLKS_i - 2
    M0_j=MBLKS_j - 2
    M0_k=MBLKS_k - 2

# this line to calculate the flame length 
    # write out mesh block M0
	
    IJK=[I,J,K]
    XB=[x1,x2,y1,y2,z1,z2]
    MBLKS=[MBLKS_i,MBLKS_j,MBLKS_k]
    M0 = [M0_i,M0_j,M0_k]
    I_LOWER = M0[0] - MBLKS[0] + 2
    I_UPPER = I_LOWER + MBLKS[0] - 1
    J_LOWER = M0[1] - MBLKS[1] + 2
    J_UPPER = J_LOWER + MBLKS[1] - 1
    K_LOWER = M0[2]	- MBLKS[2] + 2
    K_UPPER = K_LOWER + MBLKS[2] - 1

    DX=((XB[1]-XB[0])/IJK[0])
    DY=((XB[3]-XB[2])/IJK[1])
    DZ=((XB[5]-XB[4])/IJK[2])

	# # write out mesh block M0

    NX = math.ceil(IJK[0]/MBLKS[0])
    NY = math.ceil(IJK[1]/MBLKS[1])
    NZ = math.ceil(IJK[2]/MBLKS[2])
	
    NX = int(NX)
    NY = int(NY)
    NZ = int(NZ)
    LX = NX*DX
    LY = NY*DY
    LZ = NZ*DZ

    #print "DX= %s, DY= %s, DZ= %s" % (DX,DY,DZ)
    #print "LX= %s, LY= %s, LZ= %s" % (LX,LY,LZ)

    #XB0 = (-0.5*LX, 0.5*LX, -0.5*LY, 0.5*LY, XB[4], XB[4]+LZ)
    XB0 = (XB[0], XB[0]+LX, XB[2], XB[2]+LY, XB[4], XB[4]+LZ)
    IJK_LOC=str((NX,NY,NZ))
    XB_LOC=str(XB0)
	
	# This is estimates the meshes nbr
    line = (MBLKS_i* MBLKS_j * MBLKS_k)
    line = str(line)
    # print "<h3>"
    # print "<hr>"
    # print 'DX= %s, DY= %s, DZ= %s' % (DX,DY,DZ) 
    # print "</h3><hr>"
    # print "<h3>"
    # print "<hr>"
    # print 'LX= %s, LY= %s, LZ= %s' % (LX,LY,LZ) 
    # print "</h3><hr>"	
    print "<h4><hr>"
    MULT ='&MULT ID="m1",'+'DX=%s, DY=%s, DZ=%s,' %(LX,LY,LZ) + ' I_UPPER=%s, J_UPPER=%s, K_UPPER=%s ' %(I_UPPER,J_UPPER,K_UPPER) +' /'
    print MULT 
    print "</h4><hr>"
    print "<h4><hr>"
    mesh ='&MESH IJK='+ IJK_LOC[1:-1] + ', XB='+XB_LOC[1:-1]+ ', MULT_ID="m1" ' +'/ ' + line+ ' Mesh' 
    print mesh 
    print "</h4><hr>"	



def fill_previous_values():
    js_form_fill = """<script type="text/javascript">
          document.forms[0].%(FORM_ELEMENT_NAME)s.value = '%(FORM_VALUE)s';
          </script>"""
    form_field_names = ("I","J", "K", "x1", "x2","y1", "y2", "z1","z2","MBLKS_i", "MBLKS_j", "MBLKS_k")
    # Loops through form fields and writes out a custom javascript line for each element
    # to keep the previously typed number in the form
    form_count = 0
    for field in input_values:
        print js_form_fill % {'FORM_ELEMENT_NAME':form_field_names[form_count], 'FORM_VALUE':field}
        form_count += 1

###############################################################
#  Actual start of execution of script using above functions  #
###############################################################
print_html_header()

print_html_body()

try:
    I     	 = form["I"].value
    J     	 = form["J"].value
    K     	 = form["K"].value
    x1    	 = form["x1"].value
    x2    	 = form["x2"].value
    y1    	 = form["y1"].value
    y2    	 = form["y2"].value
    z1    	 = form["z1"].value
    z2    	 = form["z2"].value
    MBLKS_i  = form["MBLKS_i"].value
    MBLKS_j  = form["MBLKS_j"].value
    MBLKS_k  = form["MBLKS_k"].value
	


	
except:
    print_html_footer()
    sys.exit()
	
check_input_fields(I,J, K, x1, x2,y1, y2, z1,z2,MBLKS_i, MBLKS_j, MBLKS_k)

fill_previous_values()
	
js_form_textbox_red = """<script type="text/javascript">
document.getElementById("t_inf").style.color="red";
</script>"""

js_form_textbox_red_2 = """<script type="text/javascript">
t_inf.style.backgroundColor = "#FF0000";
</script>"""

print js_form_textbox_red_2	
	
print_html_footer()
