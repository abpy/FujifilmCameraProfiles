# Fujifilm Camera Profiles

This is a set of four camera profiles for use with raw images from digital cameras. They are made to match the film look profiles avalable in adobe cameraraw / lightroom for fuji X-cameras.

The Film Stocks are:
* Provia
* Velvia
* Astia
* Classic Chrome

## Technical Details
The profiles use a LookTable and ToneCuve.
Dcp profiles based on adobe standard are included as examples

Included for each film stock are:
* xml text files containing the LookTable and ToneCuve
* cube lut
* xml and dng profiles for the fuji xt-1 and panasonic gh3

I use dcpTool to convert between xml and dcp

To make a profile for a different camera: 
* take an existing profile for that camera
* convert it to xml
* replace the `<LookTable>` and `<ToneCuve>` xml tags with the ones from the film look text file
* `<DefaultBlackRender>` should be set to `1`
* for profiles 3.0, `<ProfileLookTableEncoding>` is now set to `1`
* change `<ProfileName>`
* convert back to dcp

### Licencing

These profiles are licenced as [cc-by-nc-sa 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
This means you may modify, make derivitives, or distribute them, eg; for another camera make and model. But you must attribute this source, share with same licence, and not sell them.

All Photographs produced with these profiles are entirely your own work, and not derivitives. The licence applies only to the profiles.

The Trademarks "Fujifilm", "Provia", "Velvia", "Astia", and "Adobe" are used for identification puposes only. No software from Fujifilm or Adobe are contained in this repository except for the included adobe standard camera profiles.
