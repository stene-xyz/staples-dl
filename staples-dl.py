#!/usr/bin/env python3
# staples-dl
# Version 1.0
# Copyright 2023 Johnny Stene
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys # Used for getting arguments and exiting with a code
import json # Used for parsing the website to find the model URL
import urllib.request # Used for downloading the page contents and the model

# Make sure we have an acceptable amount of parameters
if not(len(sys.argv) in [2, 3]):
    print("Usage: staples-dl <URL> [glb/usdz]")
    sys.exit(-1)

# Make sure we are downloading from a staples.ca product link
if not(sys.argv[1].split("/")[2].endswith("staples.ca") and sys.argv[1].split("/")[3] == "products"):
    print("URL must be a staples.ca product link!")
    sys.exit(-2)

# Do the actual downloading
try:
    with urllib.request.urlopen(sys.argv[1]) as f: # Download the page
        html = f.read().decode("utf-8") # Decode to a string

        # Find the line containing the boldTempProduct variable
        for line in html.split("\n"):
            if(line.lstrip().startswith("var boldTempProduct")):
                foundJSON = line.lstrip()[21:-1] # Remove the leading whitespace + variable declaration, and the trailing semicolon

                # Parse the JSON and find the contents of the "media" tag
                for mediaObject in json.loads(foundJSON)["media"]:
                    # Find the 3D model
                    if(mediaObject["media_type"] == "model"):
                        # Find a source for our model
                        source = mediaObject["sources"][0] # By default just grab the first in the list

                        if(len(sys.argv) == 3): # If user specified a filetype,
                            foundSource = False
                            for possibleSource in mediaObject["sources"]: # Search the source list for that filetype
                                if(possibleSource["format"] == sys.argv[2]):
                                    source = possibleSource
                                    foundSource = True
                                    break
                            if not foundSource: # If we can't find it, let the user know
                                print("Failed to find source for format " + sys.argv[2] + ", going with default...")

                        modelFormat = source["format"] # The file format we found
                        modelURL = source["url"] # The URL of that file

                        # Print some friendly text telling the user we found it
                        print("Found " + modelFormat + " file at " + modelURL)
                        print("Downloading...")

                        # Download the file
                        localFilename = sys.argv[1].split("/").pop() + "." + modelFormat
                        returned = urllib.request.urlretrieve(modelURL, localFilename)
                        print("File saved as " + returned[0])

                        sys.exit(0) # Exit with a 0 (success) code
                
                # No model was found
                print("I couldn't find a 3D model at that URL!")
                sys.exit(-3)
except Exception as e:
    print("ERROR:")
    print(e)