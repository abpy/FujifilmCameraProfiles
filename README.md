# Fujifilm Camera Profiles

This is a set of camera profiles for use with raw images from digital cameras. They are based on the camera matching profiles available in adobe cameraraw / lightroom for fuji X-cameras. This latest version is based on an x-trans 4 camera.

The Film Looks are:
* Provia
* Velvia
* Astia
* Classic Chrome
* Pro neg std
* Pro neg hi
* Eterna
* Reala Ace
* Classic Neg (lut only)
* Nostalgic Neg (lut only)
* Bleach Bypass (lut only)

## Update: Nov 22 2025. Improved luts
The luts now have improved accuracy and smoothness, especially for bright or saturated colors.

dcp profiles have increased precision and are now a more accurate match to the lut. I have found that there is still a small discrepancy in how adobe applies the tone curve. This only affects some very bright and saturated colors.

Added 'Reala Ace' film simulation (lut and profile) and direct luts for Nostalgic Neg and Bleach Bypass.

## Usage
Included for each profile are:
* text file containing the xml LookTable and ToneCurve for dcp profiles
* cube luts (3d rgb look-up-table)
  * .cube in both DisplayP3 and sRGB
  * .png lut (HaldCLUT) in sRGB

For more details on editing profiles and making a linear profile for use with the luts, see my blog post [Making Linear Camera Profiles with dcpTool](https://abpy.github.io/2023/05/20/linear-profiles.html)

The cube LUTs are intended to be applied to an image with linear contrast. A linear camera profile is required for a correct result. See below for details

#### Conversion luts for Classic Neg, Bleach Bypass, and Nostalgic Neg
These luts will convert images processed with Provia to the classic neg, bleach bypass, or nostalgic neg film simulations. They can be used with non fuji cameras using the the dng tables provided here, or with fuji x-trans cameras that don't come with these profiles using the Provia camera matching profile. They can also be applied directly to camera jpegs. The .cube files can be found in `provia conversion luts/` and are provided in both DisplayP3 and sRGB.

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

#### Using the cube luts in CameraRaw / Lightroom
You will need a [linear camera profile](https://abpy.github.io/2023/05/20/linear-profiles.html)
* Open an image with default settings (everything at 0, white balance: 'As Shot')
* Select the linear camera profile
* Option/Alt click the new preset button
* Change the profile name
* Select the Color Lookup Table checkbox
* Choose the cube file
* Set Space to Display P3
* Set Amount Min and Max to 100

![create profile dialog](/xmp_profile.png)

## Licensing

These profiles are licensed as [cc-by-nc-sa 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
This means you may modify, make derivatives, or distribute them, eg; for another camera make and model. But you must attribute this source, share with same license, and not sell them.

All Photographs produced with these profiles are entirely your own work, and not derivatives. The licence applies only to the profiles.

The Trademarks "Fujifilm", "Provia", "Velvia", "Astia", and "Adobe" are used for identification purposes only. No software from Fujifilm or Adobe are contained in this repository except for the included adobe standard camera profiles.

