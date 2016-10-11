# 3dLUT2js
3d ColorLUT converter from Nucoda CMS format to JavaScript multi-array for integration in WebGL based applications (e.g. 3D LUT cube visualisation)

Converts either a single 3d LUT .CMS file or all the LUTs in a given folder into JavaScript multi-arrays that can be embedded in XHTML or HTML5 code that is WebGL compatible.
Sample file provides a simple WebGL 3d cube visualizer that allows to navigate within the RGB cube representing the 3D LUT: each colour dot in the cube represents the position of target color (with respect to a regular-mesh cube that is the source RGB cube). The dot's colour is the original colour's hue.
