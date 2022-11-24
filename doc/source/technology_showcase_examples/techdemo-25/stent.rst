Chapter 25: Cardiovascular Stent Simulation
-------------------------------------------

This example problem shows how to simulate stent-artery interaction during and after stent
placement in an occluded artery.

The analysis demonstrates advanced modeling techniques such as:

* Contact
* Element birth and death
* Mixed u-P formulation
* Nonlinear stabilization

The following topics are available:

*  `25.1. Introduction`_
*  `25.2. Problem Description`_
*  `25.3. Modeling`_
*  `25.4. Material Properties`_
*  `25.5. Boundary Conditions and Loading`_
*  `25.6. Analysis and Solution Controls`_
*  `25.7. Results and Discussion`_
*  `25.8. Recommendations`_
*  `25.9. References`_
*  `25.10. Input Files`_

25.1. Introduction
------------------

A bare metal stent is an effective device for opening atherosclerotic arteries and
other blockages:

.. figure:: graphics/gtecstent1.png
    :align: center
    :alt: Effect of Stent Placement in Increasing Blood FlowCourtesy of Lakeview Center
    :figclass: align-center
    
    **Figure 25.1: Effect of Stent Placement in Increasing Blood Flow(#ftn.d0e32563)]**

The success of stenting depends largely on how the stent and the artery interact
mechanically. In both the stent-design process and in pre-clinical patient-specific
evaluations, computer simulation using finite element analysis (FEA) has become an
accepted tool for studying stent-artery interaction. 

A viable stent-artery finite element model must properly reflect the nonlinear nature
of the phenomenon, such as the biological tissue properties, large arterial wall
deformation, and the sliding contact between the stent and the artery wall.


---

(#d0e32563)] Courtesy of [Lakeview
Center](http://www.elakeviewcenter.org)

25.2. Problem Description
-------------------------

A [Medtronic](http://www.medtronic.com/)
Driver® (formerly S7) coronary stent and a severely
occluded coronary artery are modeled.

The artery is simplified as a two-layered straight cylinder, with one layer
representing the artery wall and the other representing the calcified plaque. 

The following figure shows the general dimensions of the artery and stent:

.. figure:: graphics/gtecstent2.png
    :align: center
    :alt: Cross-sectional View of Unloaded Artery and Stent
> 
> 
> | Ra (inner artery radius) = 2.1 mm |
> | Rs (stent radius) = 1.75 mm |
> | Rp (inner plaque radius) = 1.6 mm |
> | Ro (outer artery radius) = 2.6 mm |
> 
>
    :figclass: align-center
    
    **Figure 25.2: Cross-sectional View of Unloaded Artery and Stent**

A nonlinear static analysis is performed to simulate the three-step stenting
procedure:

1. Expand the artery using elevated pressure (balloon angioplasty).
2. Place the stent.
3. Contract the artery using mean blood pressure and creating contact between the
   stent and the artery wall.

25.3. Modeling
--------------

Cardiovascular stent modeling involves three components:

* [Stent Modeling](tecstentmodel.html#d0e32632 "25.3.1. Stent Modeling")
*  `25.3.2. Artery and Plaque Modeling`_
*  `25.3.3. Stent-Plaque Contact Modeling`_
25.3.1. Stent Modeling
^^^^^^^^^^^^^^^^^^^^^^

A line model of the stent is created and then meshed with 1,760
BEAM189 beam elements, as shown in the following
figure:

.. figure:: graphics/gtecstent3.png
    :align: center
    :alt: Stent Model 3-D Expanded Solid Display
    :figclass: align-center
    
    **Figure 25.3: Stent Model 3-D Expanded Solid Display**

For modeling simplicity and computational efficiency, beam elements are preferred
over solid elements. 

The stent assembly has a 3.5 mm diameter, a 15 mm length, and 8 crowns. The wire
for constructing the stent has a circular cross-section with an outer diameter of
0.1 mm. 

Although Nitinol material is commonly used for the stent, the nonlinear material
behavior of Nitinol requires a separate discussion. For the purposes of this
problem, therefore, the model uses linear elastic 316L steel instead.

25.3.2. Artery and Plaque Modeling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The simplified two-layer artery and plaque model is meshed with 3-D solid
elements, as shown in this figure: 

.. figure:: graphics/gtecstent4.png
    :align: center
    :alt: Simplified Atherosclerotic Artery Model
    :figclass: align-center
    
    **Figure 25.4: Simplified Atherosclerotic Artery Model**

The artery layer is meshed with 9,000 SOLID185 layered
structural solid elements with the simplified enhanced strain formulation (KEYOPT(2)
= 3). Mixed u-P formulation (KEYOPT(6) = 1) is used to overcome the volumetric
locking typically associated with incompressible biological tissue. 

The plaque layer is also meshed with 9,000 SOLID185
elements. Full integration with the 

.. image:: graphics/eq3396db3e-75fc-4169-9bdf-6efc626a19f3.svg
    :align: center
    :alt: 

 method is used for the plaque elements, as the material of the
calcified plaque is considered to be linear elastic. 

A coincident mesh is created at the artery-plaque interface to enforce a secure
bond between the artery and the plaque.

Based on St. Venant’s principle, both the artery and plaque are extended by
3 mm to reduce end effects. Fine elements are used near the two ends to mitigate any
convergence difficulty caused by large localized deformation.

25.3.3. Stent-Plaque Contact Modeling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Contact between the inner plaque wall and stent from arterial contraction is
modeled as line-to-surface contact. 

The stent lines are meshed with CONTA177 contact
elements. 

A Lagrangian multiplier method on contact normals and penalty tangent method on
target normals is used (KEYOPT(2) = 3), along with automatic bisection (KEYOPT(7) =
1) and standard contact behavior (KEYOPT(12) = 0). 

The inner plaque wall surface is meshed with TARGE170
target elements. Zero-friction behavior is assumed.(tecstentrefs.html#tecstent_cit1)]

The following figure illustrates the stent-plaque contact:

.. figure:: graphics/gtecstent5.png
    :align: center
    :alt: Standard Line-to-Surface Contact Between Stent and Inner Plaque Wall
    :figclass: align-center
    
    **Figure 25.5: Standard Line-to-Surface Contact Between Stent and Inner Plaque Wall**

25.4. Material Properties
-------------------------

Material properties (tecstentrefs.html#tecstent_cit1)] for the stent, artery, and
plaque are as follows: 

|  | **Linear Elastic** | **[Mooney-Rivlin](../ans_mat/aQw8sq22dldm.html#moon "Mooney-Rivlin")
Hyperelastic**  |
| **EX (N/mm2)** | **PRXY** | **C10 (N/mm2)** | **C01 (N/mm2)** | **C20 (N/mm2)** | **C11 (N/mm2)** |
| **Stent** | 2.00E+05 | 0.3 |  |
| **Artery** |  | 1.89E-02 | 2.75E-03 | 5.90E-01 | 8.57E-01 |
| **Plaque** | 2.19 | 0.49 |  |

25.5. Boundary Conditions and Loading
-------------------------------------

The following topics concerning boundary conditions and loading for the
cardiovascular stent simulation are available:

*  `25.5.1. Artery Boundary Conditions`_
*  `25.5.2. Stent Boundary Conditions`_
*  `25.5.3. Plaque Wall Loading`_

25.5.1. Artery Boundary Conditions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A multipoint constraint(MPC), force-distributed constraint is applied to the proximal and
distal surfaces of the artery by specifying KEYOPT (2) = 2, KEYOPT(4) = 1 and
KEYOPT(12) = 5 for the CONTA174 elements, as shown in the
following figure:

.. figure:: graphics/gtecstent6a.png
    :align: center
    :alt: Artery Boundary Conditions
    :figclass: align-center
    
    **Figure 25.6: Artery Boundary Conditions**

MPC pilot nodes (TARGE170) are fixed in all six degrees
of freedom. The boundary conditions allow for radial arterial expansion, while
adequately preventing rigid body motion of the artery.

25.5.2. Stent Boundary Conditions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As with the artery, an MPC-based, force-distributed constraint is applied to
selected nodes on the proximal and distal ends of the stent
(CONTA175), as shown in this figure:

.. figure:: graphics/gtecstent6b.png
    :align: center
    :alt: Stent Boundary Conditions
    :figclass: align-center
    
    **Figure 25.7: Stent Boundary Conditions**

MPC pilot nodes (TARGE170) are fixed in all six degrees
of freedom. 

25.5.3. Plaque Wall Loading
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Surface pressure loads are applied to all nodes on the inner plaque wall,
representing the balloon expansion pressure in the first load step (0.1
N/mm2) and blood pressure in the fourth load step
(0.0133 N/mm2). 

The following figure illustrates the load surface and load history:

**Figure 25.8: Uniform Pressure Loading on the Inner Plaque Wall (a) and Load History
  (b)**

| Uniform Pressure Loading on the Inner Plaque Wall (a) and Load History (b) | Uniform Pressure Loading on the Inner Plaque Wall (a) and Load History (b) |
| (a) | (b) |


25.6. Analysis and Solution Controls
------------------------------------

A nonlinear static analysis ([**ANTYPE**],STATIC) with large-deflection
effects ([**NLGEOM**],ON) is specified. Contact parameters are optimized
([**CNCHECK**],AUTO) to achieve better convergence based on overall
contact-pair behaviors.
**Load Step 1**
During the first load step, an elevated blood pressure of 0.1
N/mm2 is applied to the inner surface of the plaque wall
to cause sufficient radial wall expansion for subsequent stent placement. 

Stent contact elements (CONTA177) are killed
([**EKILL**]) to remove the effects of the stent.

This load step uses a maximum of 20 substeps with 20 initial substeps
([**NSUBST**],20,20). 

The following figure shows the effects of the first load step:

.. figure:: graphics/gtecstent8.png
    :align: center
    :alt: Cross-Sectional View of Artery and Stent After Balloon Angioplasty (Load Step 1)
    :figclass: align-center
    
    **Figure 25.9: Cross-Sectional View of Artery and Stent After Balloon Angioplasty (Load Step 1)**

**Load Steps 2 and 3**
Load steps 2 and 3 use three total substeps to allow the Newton-Raphson residuals (from the nonlinear
expansion in load step 1) to equilibrate after the stent contact elements are
reactivated ([**EALIVE**]).
**Load Step 4**
In the fourth load step, blood pressure is ramped to a magnitude of 0.0133
N/mm2, which represents the mean arterial blood pressure
(100 mmHg). 

Under this reduced load, the atherosclerotic artery collapses onto the stent scaffold. 

This load step uses 200 initial substeps, 2000 maximum substeps, and 20 minimum
substeps to obtain contact convergence ([**NSUBST**],200,2000,20). 
Nonlinear stabilization
([**STABILIZE**],CONST,ENERGY,0.1) helps to achieve solution
convergence during this load step.
25.7. Results and Discussion
----------------------------

Proper element technologies and solution options allow a successful nonlinear
simulation of stent-artery interaction. The analysis generates detailed information
about the post-insertion artery wall deformation, wall stresses, and stent
retraction.

The positive effect of stenting is evident in the following figure, which shows the
artery wall configurations before and after stent placement:

**Figure 25.10: Arterial Wall Deformation During Balloon Angioplasty (a) and After Stent
  Placement (b)**

| Arterial Wall Deformation During Balloon Angioplasty (a) and After Stent Placement (b) | Arterial Wall Deformation During Balloon Angioplasty (a) and After Stent Placement (b) |
| (a) | (b) |


The following figure clearly shows the expected tissue prolapse (tissue extension into
the gaps in the stent):

.. figure:: graphics/gtecstent10.png
    :align: center
    :alt: Arterial Wall Displacement and Tissue Prolapse Results
    :figclass: align-center
    
    **Figure 25.11: Arterial Wall Displacement and Tissue Prolapse Results**

This figure shows the detailed stress distribution on the inner artery wall, with an
expected pattern matching the stent geometry: 

.. figure:: graphics/gtecstent11.png
    :align: center
    :alt: Arterial Wall von Mises Stress Results
    :figclass: align-center
    
    **Figure 25.12: Arterial Wall von Mises Stress Results**

Finally, the stent retraction under compressive load from the occluded artery wall is
shown in this figure:

.. figure:: graphics/gtecstent12.png
    :align: center
    :alt: Stent Retraction Resulting from Arterial Compression
    :figclass: align-center
    
    **Figure 25.13: Stent Retraction Resulting from Arterial Compression**

The simulation results agree well with those in the published literature.(tecstentrefs.html#tecstent_cit1)]

FEA-based simulation is capable of quickly generating accurate and detailed
information about stent-artery interaction. Finite element modeling is being used not
only to develop state-of-the-art stent innovations, but also for pre-clinical
patient-specific assessment and customization. 

25.8. Recommendations
---------------------

To perform a similar stent-artery interaction analysis, consider the following hints
and recommendations:

* Compared to surface-to-surface contact with a full solid model, line-to-surface contact can provide
  similar results using significantly less solution time.
* Multipoint constraints (MPCs) provide
  biologically accurate boundary conditions.
* The choice of units is critical for avoiding numerical difficulties. For
  biological problems, millimeters-micron units are preferred.
* To achieve faster solutions, coincident nodes and surfaces are preferred over
  bonded contact.
* Stabilization mitigates convergence
  issues in unstable nonlinear problems.

25.9. References
----------------

The following reference work is cited in this example problem:

1. Lally, C., Dolan, F, & Pendergrast, P. J. (2005). (http://www.jbiomech.com/article/S0021-9290(04)00375-6/abstract). *Journal of Biomechanics.* 38:
1574-1581.

25.10. Input Files
------------------

The following files were used in this problem:

* **stent.dat** -- Input file for the cardiovascular stent
  problem.
* **stent.cdb** -- The common database file containing the model
  information for this problem (called by **stent.dat**).

+-----------------------------------------------------------------------------------------------------------------------------------+
| [Download the zipped **td-25** file set for thisproblem](https://storage.ansys.com/doclinks/techdemos.html?code=td-25-DLU-N2a).   |
+===================================================================================================================================+
| For more information, see [Obtaining the Input  Files](tecintro.html "Obtaining the Input                     Files").            |
+-----------------------------------------------------------------------------------------------------------------------------------+
