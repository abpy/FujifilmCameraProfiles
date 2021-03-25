# Fujifilm Camera Profiles

This is a set of four camera profiles for use with raw images from digital cameras. They are made to match the film look profiles available in adobe cameraraw / lightroom for fuji X-cameras.

The Film Stocks are:
* Provia
* Velvia
* Astia
* Classic Chrome

## Technical Details
The profiles use a LookTable and ToneCurve.
Dng profiles based on adobe standard are included as examples

Included for each film stock are:
* text file containing the xml LookTable and ToneCurve for dcp profiles
* xml and dcp profiles for the fuji xt-1 and panasonic gh3
* cube lut
* the cube lut and csv tables can be used with adobe's look profiles (xmp preset)

I use dcpTool to convert between xml and dcp

To make a profile for a different camera: 
* take an existing profile for that camera
* convert it to xml
* replace the `<LookTable>` and `<ToneCurve>` xml tags with the ones from the film look text file
* `<DefaultBlackRender>` should be set to `1`
* `<ProfileLookTableEncoding>` should be set to `1`
* change `<ProfileName>`
* convert back to dcp

### Licensing

These profiles are licensed as [cc-by-nc-sa 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
This means you may modify, make derivatives, or distribute them, eg; for another camera make and model. But you must attribute this source, share with same license, and not sell them.

All Photographs produced with these profiles are entirely your own work, and not derivatives. The licence applies only to the profiles.

The Trademarks "Fujifilm", "Provia", "Velvia", "Astia", and "Adobe" are used for identification purposes only. No software from Fujifilm or Adobe are contained in this repository except for the included adobe standard camera profiles.

