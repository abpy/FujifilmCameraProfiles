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

## Updates

### Sep 2026: Automation scripts
Added interactive Python scripts (`create_profiles.py` and `create_linear.py`) to streamline camera profile generation and deployment.
* Automatically locates your camera's `Adobe Standard.dcp` profile.
* Batch compiles all native Fujifilm DCP profiles with correct tone curves and metadata.
* Creates linear base profiles required for working with 3D LUTs in Camera Raw.

### Nov 22 2025: Improved luts
The luts now have improved accuracy and smoothness, especially for bright or saturated colors.

dcp profiles have increased precision and are now a more accurate match to the lut. I have found that there is still a small discrepancy in how adobe applies the tone curve. This only affects some very bright and saturated colors.

Added 'Reala Ace' film simulation (lut and profile) and direct luts for Nostalgic Neg and Bleach Bypass.

## Usage
Included for each profile are:
* text file containing the xml LookTable and ToneCurve for dcp profiles
* cube luts (3d rgb look-up-table)
  * .cube in both DisplayP3 and sRGB
  * .png lut (HaldCLUT) in sRGB
* For icc profiles for use in Capture One, see: [onepill/FujifilmCameraProfiles](https://github.com/onepill/FujifilmCameraProfiles/), provided by Siyuan Zhang(onepill)

For more details on editing profiles and making a linear profile for use with the luts, see my blog post [Making Linear Camera Profiles with dcpTool](https://abpy.github.io/2023/05/20/linear-profiles.html)

The cube LUTs are intended to be applied to an image with linear contrast. A linear camera profile is required for a correct result. See below for details.

---

## Automation Scripts (Python)

Two interactive Python scripts are provided to automate profile generation and installation:

### Prerequisites
* **Python 3.8+**
* **[dcpTool](https://dcptool.sourceforge.net/)**: Recommended to add to your system `PATH`. If placed directly in the repository root directory instead, make sure to copy all accompanying `.dll` files alongside `dcptool.exe` into the folder (on Windows).
* **Adobe Lightroom Classic or Adobe Photoshop**: An active installation providing the base camera profiles (`Adobe Standard`).

---

### 1. Batch Generate Native DCP Profiles (`create_profiles.py`)

Automates batch-building all available Fujifilm DCP profiles for your specific camera model.

```bash
python create_profiles.py
```

* **Interactive Selection**: Prompts for your camera model (e.g. `d5300` or `Nikon D5300`) and locates the matching `Adobe Standard.dcp` automatically.
* **Batch Compilation**: Decompiles the base profile, strips existing LookTables, applies ToneCurves from `xml tables/`, sets metadata tags (`DefaultBlackRender=1`, `ProfileLookTableEncoding=1`), names profiles cleanly (e.g., `Fuji Classic Chrome`), and outputs compiled `.dcp` files into `output/`.
* **One-Click Install**: Prompts to directly copy the generated profiles into your system CameraRaw profile directory.

---

### 2. Generate Linear Base Profile (`create_linear.py`)

Creates the camera-specific linear base profile (`<Camera> Linear.dcp`) required for applying 3D LUTs in Adobe Camera Raw.

```bash
python create_linear.py
```

* **Linearization**: Strips original LookTables from your camera's `Adobe Standard.dcp`, inserts an exact 1:1 diagonal ToneCurve, sets `DefaultBlackRender=1`, and compiles the profile.
* **One-Click Install**: Prompts to copy the linear profile directly into `CameraProfiles/Linear Profiles` for immediate use in Camera Raw.

---

## Manual Workflow

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

*(Note: This process can be automated using `create_profiles.py`.)*

#### Using the cube luts in CameraRaw
You will need a [linear camera profile](https://abpy.github.io/2023/05/20/linear-profiles.html) (create one via `create_linear.py` or manually):
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
