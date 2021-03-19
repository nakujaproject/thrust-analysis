# Test-stand

What the program does:
- Read data from load cell
- Record the data to a file
- Upload the File to google drive folder
- Display a live graph of the data

## Usage
### Install requirements:
`pip install -r requirements.txt`

### Google Drive setup
Follow instructions in the file [file](https://d35mpxyw7m7k7g.cloudfront.net/bigdata_1/Get+Authentication+for+Google+Service+API+.pdf)

### Running:
`python measure.py`

without data spikes:\
`python spikeless_measure.py`
