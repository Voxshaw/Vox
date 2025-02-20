This Python file is designed for processing information from yellowpages.com.

Before using this specialized program, you need to open the webpage's Developer Mode. After searching for the content you want, refresh the page while on the results list screen, and retrieve the document from the first GET request. Then, manually add a .txt extension to the document.

Since users typically process multiple pages at once, you can place all the files from different pages into the same folder. This script will process all .txt files within the folder and generate a file containing name, address, email, and phone number, separated by = to facilitate importing into Excel and splitting columns by this delimiter.

This code is written for yellowpages.com.au, but it should still work after removing .au from the domain.
