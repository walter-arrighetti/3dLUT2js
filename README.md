# 3dLUT2js
3d ColorLUT converter from Nucoda CMS format to JavaScript multi-array for integration in WebGL based applications (e.g. 3D LUT cube visualisation)
<img src="pics/Kodak-Vision___Rec709___Nucoda66_4096_V3.png" />
Converts either a single 3d LUT or all the LUTs in a given folder, i.e. `.cms` file(s), into JavaScript multi-array(s) that can be embedded in XHTML or HTML5 code that is WebGL compatible.
Sample file provides a simple WebGL 3d cube visualizer that allows to navigate within the RGB cube representing the 3D LUT: each colour dot in the cube represents the position of target color (with respect to a regular-mesh cube that is the source RGB cube). The dot's colour is the original colour's hue.

In order to view the examples on your JavaScript/WebGL enabled browser, please make sure to have the `three.js` folder in the same path as the HTML files themselves. `three.js` can be retrieved at https://github.com/mrdoob/three.js
<img src="pics/ACES___DCI-XYZ___Nucoda66_4096_V3_RGBcube.png" width="869" />
