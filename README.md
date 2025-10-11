# Vibe Resizer

A tiny Flask app that batch-converts vertical 9:16 clips into square (1:1) and widescreen (16:9) exports.
Choose between a blurred background letterbox or a fill-and-crop look.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This project depends on FFmpeg. MoviePy will attempt to download a static build on first use, but
for best results install FFmpeg locally and make sure it is available on your `$PATH`.

## Running the app

```bash
flask --app app run --debug
```

## Step-by-step macOS setup (with Xcode)

The walkthrough below assumes you are starting from a fresh Mac and want to use Xcode as
your editor. Every command should be typed into the **Terminal** app unless noted
otherwise.

1. **Install Xcode** (if you have not already): open the Mac App Store, search for
   “Xcode”, click **Get**, and wait for the installation to finish. Launch Xcode once so
   it can finish installing extra components.
2. **Install the Xcode command-line tools**. Either let Xcode prompt you on first launch
   or run `xcode-select --install` in Terminal and accept the dialog. This gives you Git,
   compilers, and other utilities.
3. **Install Homebrew**, the package manager for macOS. In Terminal run:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

   Follow the on-screen prompts and then close/reopen Terminal so the new `brew` command
   is available.
4. **Install Python and FFmpeg** with Homebrew:

   ```bash
   brew install python@3.11 ffmpeg
   ```

   After the installation finishes, check that the commands are available:

   ```bash
   python3 --version
   ffmpeg -version
   ```

5. **Get the project files**. You can either:
   * **Clone with Git** (recommended):

     ```bash
     git clone https://github.com/<your-account>/<your-fork-or-repo>.git vibe-resizer
     ```

   * **Download a ZIP**: on GitHub, click **Code → Download ZIP**, unzip it in Finder,
     then in Terminal run `cd` followed by a space, drag the extracted folder into the
     window, and press **Enter** to move into it.
6. **Open the folder in Xcode** (optional but convenient): in Xcode choose
   **File → Open…**, navigate to the `vibe-resizer` folder, and click **Open**. Xcode
   treats the directory as a workspace so you can browse and edit files.
7. **Create and activate a Python virtual environment** inside the project folder:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Your prompt should now show `(.venv)` in front of it, indicating the environment is
   active.
8. **Install Python dependencies** listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

9. **Start the Flask development server**:

   ```bash
   flask --app app run --debug --port 5000 --host 127.0.0.1
   ```

   Leave this Terminal window open while you test. You can also run the same command from
   Xcode’s built-in terminal by choosing **View → Show Terminal** (Xcode 15+) and
   activating the virtual environment inside that panel.
10. **Try the app in your browser**: when the Terminal shows
    `Running on http://127.0.0.1:5000`, open that address in Safari or Chrome. Drag a few
    9:16 videos into the page, pick the export styles, and click **Start resizing**. A ZIP
    containing the 1:1 and 16:9 renders downloads automatically when processing completes.

If you want to stop the server, go back to the Terminal window where Flask is running and
press `Ctrl+C`. To reuse the project later, open Terminal, `cd` into the folder, run
`source .venv/bin/activate`, and start the Flask command again.

### Trying it in your browser

1. Wait for Flask to print `Running on http://127.0.0.1:5000` in the terminal.
2. Open that address in your browser on the same machine.
3. Drag one or more 9:16 clips into the upload dropzone.
4. Pick either **Blurred background** or **Fill and crop** for each export size.
5. Click **Start resizing** and let the progress bar finish. When the job completes
   your browser will download a ZIP containing both the 1:1 and 16:9 renders.

> Tip: if you need to test from another device on your network, start the server with
> `flask --app app run --host 0.0.0.0 --port 5000` and browse to `http://<your-ip>:5000`.

## Pricing

This utility is completely free to run locally. There are no usage caps or per-render fees—process
as many clips as your machine can handle.
