# XPS Tools Extender
It contains some extra features that are added on top of the base xps tools addon.  

# installation
First You need to install the base [xps tools 2.0.2](https://github.com/johnzero7/XNALaraMesh/releases/tag/v2.0.2) addon.  
Install this addon next. (Edit > Preferences > Add-ons > install > Select the zipped file")  
A new "XPS Fixes" section will be added to the xps panel in the sidebar.

# Instructions
**XPS to Principled** > removes the xps node group from materials of all selected objects and replaces that with a principled bsdf node. this is useful if you want to make changes to materials without messing around with the node group and making it single user for each modification you make on a unique part of the model.  
- select all parts of the model in object mode (make sure armature is not selected) and click on the button  
___
**Non-Opaque to Hashed** > converts all non-opaque materials of selected selected objects to alpha hashed blend mode. usefull for changing the default "alpha blend" blending mode of hair cards to visually better looking "alpha hashed" blend mode.  
- select all parts of the model in object mode (make sure armature is not selected) and click on the button. it leaves the opaque materials and only converts alpha clip and alpha blend materials to alpha hashed
___
**"Opaque"** **"Alpha Blen"d** **"Alpha Hashed"** **"Alpha Clip"** > converts the blending mode of all selected objects to the selected blend mode. useful for batch fixing some messed up xps models that even their opaque parts use the wrong alpha blend blending mode.   
- select all parts of the model in object mode (make sure armature is not selected) and click on the button    
___
**_For bone fixes buttons to properly work, you have to press "XPS to Blender" button first in the XPS Bones section of the base xps addon_**  
**_These buttons may not work on all xps models with different bone names and extra bones_**
**_Currently works best with [Shuubaru's](https://www.deviantart.com/shuubaru/gallery/all) DOA models_**   

**Fix Bone Layers** > organizes the bones by putting different bones in different bone layers and hiding some bone layers.   
- select the armature in object mode and click on the button

**Add Custom Rig** > adds custom shapes to main bones
- select the armature in object mode and click on the button
