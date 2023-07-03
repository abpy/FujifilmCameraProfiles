# Fujifilm Camera Profiles

This is a set of camera profiles for use with raw images from digital cameras. They are based on the camera matching profiles available in adobe cameraraw / lightroom for fuji X-cameras. This latest version is based on a more recent camera model: the x-pro3.

The Film Looks are:
* Provia
* Velvia
* Astia
* Classic Chrome
* Pro neg std
* Pro neg hi
* Eterna
* Classic Neg

## Usage
Included for each profile are:
* text file containing the xml LookTable and ToneCurve for dcp profiles
* cube luts (3d rgb look-up-table)
  * .cube in both DisplayP3 and sRGB
  * .png CLUT in sRGB
* xml and dcp profiles as examples

For more details on editing profiles and making a linear profile for use with the luts, see my blog post [Making Linear Camera Profiles with dcpTool](https://abpy.github.io/2023/05/20/linear-profiles.html)

#### cube lut
The cube LUTs are intended to be applied to an image with linear contrast. A linear camera profile is required for a correct result.

The Classic Neg profile is only available as a cube lut.

#### dcp camera profile
The dcp profiles use a LookTable and ToneCurve.

To make a profile, use [dcptool](https://dcptool.sourceforge.net/Introduction.html) to convert between xml and dcp.

To make a profile for your camera:
* find an existing dcp profile for that camera. ex. Adobe Standard
* convert it to xml
* replace the `<LookTable>` and `<ToneCurve>` xml tags with the ones from the film look text file
* set `<DefaultBlackRender>` to `1`
* set `<ProfileLookTableEncoding>` to `1`
* change `<ProfileName>`
* convert back to dcp

### Licensing

These profiles are licensed as [cc-by-nc-sa 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
This means you may modify, make derivatives, or distribute them, eg; for another camera make and model. But you must attribute this source, share with same license, and not sell them.

All Photographs produced with these profiles are entirely your own work, and not derivatives. The licence applies only to the profiles.

The Trademarks "Fujifilm", "Provia", "Velvia", "Astia", and "Adobe" are used for identification purposes only. No software from Fujifilm or Adobe are contained in this repository except for the included adobe standard camera profiles.

